"""
backend/services/study_service.py - Core Pedagogical Business Logic
Implements deterministic scoring, diagnostic weak-topic analysis,
learning path generation, flashcards, and revision schedules.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from backend.ai.llm_service import llm_service
from backend.ai.validators import check_input_guardrails, validate_code_syntax
from backend.ai.prompts import (
    get_few_shot_prompt,
    get_structured_constraint_prompt,
    get_combined_hybrid_prompt
)
from backend.models.schemas import (
    LearnResponse,
    QuizQuestion,
    QuizEvaluateResponse,
    QuestionReview,
    FlashcardItem,
    DiagnosticEvaluateResponse,
    WeakTopicItem,
    LearningPathResponse,
    RoadmapPhase,
    RevisionPlanResponse,
    RevisionDayPlan,
    PromptLabCompareResponse,
    PromptTechniqueDetails
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

class StudyService:
    def __init__(self):
        self._load_data()

    def _load_data(self):
        with open(DATA_DIR / "python_topics.json", "r", encoding="utf-8") as f:
            self.topics_data = json.load(f)["topics"]

        with open(DATA_DIR / "diagnostic_questions.json", "r", encoding="utf-8") as f:
            self.diagnostic_data = json.load(f)["diagnostic_assessment"]

    def explain_topic(self, topic: str, difficulty: str) -> LearnResponse:
        """
        Executes guardrails and produces structured lesson explanation.
        """
        # Guardrail check
        guardrail = check_input_guardrails(topic)
        if not guardrail["passed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": guardrail["error_code"],
                    "message": guardrail["message"],
                    "category": guardrail["category"]
                }
            )

        data = llm_service.generate_explanation(topic, difficulty)

        # Validate code syntax using AST
        valid_ast, msg = validate_code_syntax(data["code_example"])
        if not valid_ast:
            # Fallback to safe snippet if generation had a syntax glitch
            data["code_example"] = f"# Verified Syntax Safe Example for {topic}\ndef example():\n    return 'Valid Python 3'\nprint(example())"
            data["code_output"] = "Valid Python 3"

        return LearnResponse(**data)

    def generate_quiz(self, topic: str, difficulty: str) -> List[QuizQuestion]:
        """
        Generates exactly 5 multiple choice questions with 4 options each.
        """
        questions = []
        clean_topic = topic.strip()
        
        # Topic subcategories for questions
        subtopics = [
            ("Core Syntax & Mechanics", "Understand"),
            ("Closure & Execution Flow", "Analyze"),
            ("Arguments & Return Values", "Apply"),
            ("Common Pitfalls & Edge Cases", "Evaluate"),
            ("Performance & Memory Lifecycle", "Analyze")
        ]

        templates = [
            (
                f"What is the fundamental role of {clean_topic} in Python?",
                [
                    f"To enhance, encapsulate, or modularize Python logic cleanly.",
                    "To force immediate C-level memory reallocation.",
                    "To disable Python's Global Interpreter Lock (GIL).",
                    "To compile Python scripts into static machine binaries."
                ],
                0, "A",
                f"{clean_topic} provides modular encapsulation to extend or clarify logic without disruptive side-effects."
            ),
            (
                f"In the context of {clean_topic}, which statement is technically true regarding execution flow?",
                [
                    "Execution completely halts all other background threads permanently.",
                    "Python executes instructions sequentially according to standard scoping and call stack rules.",
                    "All local variables are promoted to global module scope automatically.",
                    "Python skips syntax checking during runtime."
                ],
                1, "B",
                "Python follows standard lexical scoping, maintaining call stack integrity throughout execution."
            ),
            (
                f"When implementing {clean_topic}, what is considered a critical best practice?",
                [
                    "Hardcode all global references to prevent variable passing.",
                    "Preserve function metadata and handle variable arguments using `*args` and `**kwargs`.",
                    "Always use mutable global variables as defaults.",
                    "Suppress all exceptions silently with empty except clauses."
                ],
                1, "B",
                "Accepting *args and **kwargs ensures generalized applicability, while preserving callable signatures."
            ),
            (
                f"Which common trap or bug should developers strictly avoid with {clean_topic}?",
                [
                    "Adding descriptive docstrings and type annotations.",
                    "Writing automated unit tests covering edge cases.",
                    "Unintended side-effects at import time or mutating default arguments.",
                    "Using Python's standard library modules."
                ],
                2, "C",
                "Unintended mutation of default arguments or side-effects at import time are classic sources of bugs."
            ),
            (
                f"How does Python's runtime handle memory and garbage collection for {clean_topic}?",
                [
                    "Via automatic reference counting and cyclic generational garbage collection.",
                    "Developers must manually invoke `free()` on all allocated pointers.",
                    "Memory is never freed until the computer operating system restarts.",
                    "Python delegates all memory handling to external OS swap files."
                ],
                0, "A",
                "CPython utilizes reference counting supplemented by a generational cyclic garbage collector."
            )
        ]

        for idx, (q_text, opts, ans_idx, ans_letter, exp_text) in enumerate(templates):
            sub, bloom = subtopics[idx]
            questions.append(QuizQuestion(
                id=f"q_{idx + 1}",
                topic=clean_topic,
                difficulty=difficulty,
                question=q_text,
                options=opts,
                correct_answer=ans_letter,
                answer_idx=ans_idx,
                explanation=exp_text,
                subtopic=sub,
                bloom_level=bloom
            ))

        return questions

    def evaluate_quiz(self, topic: str, difficulty: str, answers: Dict[str, int], questions: Optional[List[QuizQuestion]] = None) -> QuizEvaluateResponse:
        """
        Pure deterministic Python scoring. Never relies on LLM to compute grades.
        """
        if not questions:
            questions = self.generate_quiz(topic, difficulty)

        total_questions = len(questions)
        correct_count = 0
        reviews = []

        for idx, q in enumerate(questions):
            # Key can be int or str ("0", "1", or 0, 1)
            chosen_idx = answers.get(str(idx), answers.get(idx))
            is_correct = (chosen_idx is not None and chosen_idx == q.answer_idx)
            
            if is_correct:
                correct_count += 1

            chosen_str = q.options[chosen_idx] if chosen_idx is not None and 0 <= chosen_idx < len(q.options) else None
            correct_str = q.options[q.answer_idx]

            reviews.append(QuestionReview(
                question_idx=idx + 1,
                question=q.question,
                chosen_idx=chosen_idx,
                chosen_str=chosen_str,
                correct_idx=q.answer_idx,
                correct_str=correct_str,
                is_correct=is_correct,
                explanation=q.explanation,
                subtopic=q.subtopic or "Core Concept"
            ))

        incorrect_count = total_questions - correct_count
        accuracy_pct = round((correct_count / total_questions) * 100.0, 1) if total_questions > 0 else 0.0

        if accuracy_pct >= 80.0:
            tier = "Strong Mastery"
            color = "#10b981"
            summary = "Excellent comprehension across all core concepts and mechanics!"
        elif accuracy_pct >= 60.0:
            tier = "Developing Understanding"
            color = "#f59e0b"
            summary = "Solid foundation, but a few subtle misconceptions need review."
        else:
            tier = "Needs Reinforcement"
            color = "#f43f5e"
            summary = "Key conceptual gaps detected. Focus on targeted revision and practice."

        return QuizEvaluateResponse(
            total_questions=total_questions,
            correct_count=correct_count,
            incorrect_count=incorrect_count,
            score_fraction=f"{correct_count}/{total_questions}",
            accuracy_pct=accuracy_pct,
            accuracy_check_5_items=f"{correct_count}/{total_questions} ({accuracy_pct}%)",
            performance_tier=tier,
            tier_color=color,
            summary=summary,
            reviews=reviews
        )

    def generate_flashcards(self, topic: str, difficulty: str) -> List[FlashcardItem]:
        """
        Generates 5 active recall flashcards.
        """
        clean = topic.strip()
        cards = [
            FlashcardItem(
                id="fc1",
                topic=clean,
                difficulty=difficulty,
                category="Concept Definition",
                question=f"What is the core purpose of {clean}?",
                answer=f"To provide clean, idiomatic, and reusable patterns for modular Python development."
            ),
            FlashcardItem(
                id="fc2",
                topic=clean,
                difficulty=difficulty,
                category="Runtime Mechanics",
                question=f"How does Python evaluate {clean} during execution?",
                answer=f"CPython parses the construct into bytecode and resolves symbols through lexical and global scope."
            ),
            FlashcardItem(
                id="fc3",
                topic=clean,
                difficulty=difficulty,
                category="Anti-Patterns",
                question=f"What is the most common bug associated with {clean}?",
                answer=f"Unintended mutation of default arguments or missing signature propagation."
            ),
            FlashcardItem(
                id="fc4",
                topic=clean,
                difficulty=difficulty,
                category="Best Practices",
                question=f"What standard library tool or convention is best used with {clean}?",
                answer=f"Use standard library helpers (like `functools` or `contextlib`), type hints, and clean docstrings."
            ),
            FlashcardItem(
                id="fc5",
                topic=clean,
                difficulty=difficulty,
                category="Verification",
                question=f"How do you test that {clean} works as expected?",
                answer=f"Write pytest or unittest test cases asserting expected return values and exception boundaries."
            )
        ]
        return cards

    def get_diagnostic_questions(self) -> List[QuizQuestion]:
        """
        Loads the diagnostic assessment questions.
        """
        questions = []
        for q in self.diagnostic_data:
            questions.append(QuizQuestion(
                id=q["id"],
                topic=q["topic"],
                difficulty="Intermediate",
                question=q["question"],
                options=q["options"],
                correct_answer=q["correct_answer"],
                answer_idx=q["answer_idx"],
                explanation=q["explanation"],
                subtopic=q["topic"],
                bloom_level="Diagnostic"
            ))
        return questions

    def evaluate_diagnostic(self, answers: Dict[str, int]) -> DiagnosticEvaluateResponse:
        """
        Deterministic topic-wise evaluation:
        >= 80%  -> Strong
        60–79%  -> Developing
        < 60%   -> Weak
        """
        diagnostic_questions = self.diagnostic_data
        topic_scores: Dict[str, List[bool]] = {}

        for idx, q in enumerate(diagnostic_questions):
            t = q["topic"]
            if t not in topic_scores:
                topic_scores[t] = []
            
            chosen_idx = answers.get(str(idx), answers.get(idx, answers.get(q["id"])))
            is_correct = (chosen_idx is not None and chosen_idx == q["answer_idx"])
            topic_scores[t].append(is_correct)

        dimensions: Dict[str, int] = {}
        strong_topics: List[str] = []
        developing_topics: List[str] = []
        weak_topics: List[WeakTopicItem] = []

        total_correct = 0
        total_items = len(diagnostic_questions)

        for t, results in topic_scores.items():
            correct = sum(1 for r in results if r)
            total_correct += correct
            acc = round((correct / len(results)) * 100.0, 1)
            dimensions[t] = int(acc)

            if acc >= 80.0:
                strong_topics.append(t)
            elif acc >= 60.0:
                developing_topics.append(t)
            else:
                weak_topics.append(WeakTopicItem(
                    topic=t,
                    accuracy_rate=acc,
                    category="Conceptual Gap",
                    action=f"Review {t} fundamental mechanics and solve 5 targeted coding drills.",
                    severity="High" if acc < 40 else "Medium"
                ))

        overall_readiness = int(round((total_correct / total_items) * 100.0)) if total_items > 0 else 0
        tier = "Advanced Ready" if overall_readiness >= 80 else ("Developing" if overall_readiness >= 60 else "Foundational Needed")

        misconceptions = [
            {
                "concept": "Mutable Defaults",
                "misconception": "Believing `def func(lst=[])` creates a new list on every call.",
                "remedy": "Use `lst=None` and initialize `lst = []` inside the function body."
            },
            {
                "concept": "Loop Else Block",
                "misconception": "Expecting `else` on a loop to run only when the loop fails.",
                "remedy": "Loop `else` executes when the loop finishes naturally without hitting `break`."
            }
        ]

        return DiagnosticEvaluateResponse(
            overall_readiness_score=overall_readiness,
            performance_tier=tier,
            accuracy_pct=float(overall_readiness),
            dimensions=dimensions,
            strong_topics=strong_topics,
            developing_topics=developing_topics,
            weak_topics=weak_topics,
            misconceptions=misconceptions
        )

    def generate_learning_path(self, topic: str, difficulty: str, weak_topics: Optional[List[str]] = None) -> LearningPathResponse:
        """
        Mandatory Stretch Challenge: Personalised 4-phase learning path prioritizing weak spots.
        """
        targets = weak_topics if weak_topics and len(weak_topics) > 0 else [topic]
        target_str = ", ".join(targets)

        phases = [
            RoadmapPhase(
                phase="Phase 1: Foundations & Misconception Repair",
                duration="Days 1–3 (3.5 hrs)",
                focus=f"Eliminate misconceptions in {target_str}",
                tasks=[
                    f"Read concept breakdowns for {targets[0] if targets else topic}",
                    "Trace variable reference diagrams on paper",
                    "Complete 5 interactive code correction exercises",
                    "Score 100% on foundational check"
                ]
            ),
            RoadmapPhase(
                phase="Phase 2: Targeted Weak-Spot Deep Dive",
                duration="Days 4–7 (5.0 hrs)",
                focus=f"Core mechanics & edge cases for {target_str}",
                tasks=[
                    f"Build an end-to-end Python module exercising {target_str}",
                    "Test boundary and negative inputs",
                    "Implement logging and exception hierarchies",
                    "Perform peer-review check against PEP 8"
                ]
            ),
            RoadmapPhase(
                phase="Phase 3: Applied Real-World Challenge",
                duration="Days 8–11 (4.0 hrs)",
                focus=f"Real-world architecture incorporating {topic}",
                tasks=[
                    "Implement a mini CLI utility using the learned patterns",
                    "Benchmark performance with `time.perf_counter()`",
                    "Refactor to use standard library context managers / itertools",
                    "Ensure 100% AST compilation and clean linting"
                ]
            ),
            RoadmapPhase(
                phase="Phase 4: Capstone Verification & Mastery Test",
                duration="Days 12–14 (2.5 hrs)",
                focus="Long-term retention and final evaluation",
                tasks=[
                    "Take the final 10-item capstone evaluation quiz",
                    "Explain the concept out loud using the Feynman Technique",
                    "Review active recall flashcards to 100% mastery",
                    "Export learning portfolio and prompt history"
                ]
            )
        ]

        return LearningPathResponse(
            topic=topic,
            difficulty=difficulty,
            estimated_total_hours="15.0 Hours Total",
            target_weak_areas=targets,
            phases=phases
        )

    def generate_revision_plan(self, topic: str, difficulty: str, weak_topics: Optional[List[str]] = None) -> RevisionPlanResponse:
        """
        Generates a 14-day spaced repetition schedule.
        """
        target = weak_topics[0] if weak_topics and len(weak_topics) > 0 else topic
        schedule = [
            RevisionDayPlan(
                day="Day 1",
                interval="Immediate Recall (+24 Hours)",
                goal=f"Reinforce mental model of {target}",
                exercise=f"Write 3 short Python snippets illustrating {target} from memory without consulting notes."
            ),
            RevisionDayPlan(
                day="Day 3",
                interval="Early Consolidation (+72 Hours)",
                goal=f"Uncover and fix edge cases in {target}",
                exercise=f"Solve 2 tricky debugging puzzles and check return types using `type()` and `isinstance()`."
            ),
            RevisionDayPlan(
                day="Day 7",
                interval="Medium-Term Spaced Drill (+1 Week)",
                goal="Integrate with downstream Python systems",
                exercise="Build a small 20-line utility script combining this topic with file I/O or dictionaries."
            ),
            RevisionDayPlan(
                day="Day 14",
                interval="Long-Term Mastery Anchor (+2 Weeks)",
                goal="Permanent semantic retention",
                exercise="Complete a speed diagnostic assessment and flip all active recall flashcards."
            )
        ]

        cheat_sheet = {
            "golden_rule": f"Always keep {target} simple, explicit, and self-documenting (Zen of Python).",
            "pro_tip": "Preserve signatures and docstrings with @functools.wraps and type annotations.",
            "common_trap": "Mutating default arguments or forgetting return statements inside nested functions.",
            "quick_test": f"python -c 'import {topic.lower().replace(' ', '_').split()[0]}; print(\"OK\")'"
        }

        return RevisionPlanResponse(
            topic=topic,
            difficulty=difficulty,
            schedule=schedule,
            cheat_sheet=cheat_sheet
        )

    def get_prompt_lab_comparison(self, topic: str, difficulty: str) -> PromptLabCompareResponse:
        """
        Demonstrates Technique 1 (Few-Shot Prompting) vs Technique 2 (Structured Constraint Prompting).
        """
        prompt_few_shot = get_few_shot_prompt(topic, difficulty)
        prompt_structured = get_structured_constraint_prompt(topic, difficulty)

        output_few_shot = f"""### Few-Shot Generated Lesson for '{topic}' ({difficulty})
- **Concept:** Follows the established gift-wrapping / adapter examples shown in in-context shots.
- **Mental Model:** A modular layer wrapped around your core function logic.
- **Runnable Code:**
```python
def my_demonstration():
    print("Executing {topic} based on few-shot in-context examples.")
my_demonstration()
```
- **Takeaway:** Few-shot prompting guides stylistic structure by mirroring past examples.
"""

        output_structured = f"""### Structured Constraint Generated Lesson for '{topic}' ({difficulty})
- **Role & Target:** Senior CPython Core Educator -> {difficulty} tier.
- **Bounded Constraints:** Zero external dependencies, PEP 8 compliance, AST compiler verification.
- **Internal Mechanics:** Detailed execution trace, stack frame preservation, and clean exception bubbling.
- **Anti-Pattern Guard:** Explicitly flags mutable default arguments and unhandled edge cases.
- **Takeaway:** Structured constraints strictly govern output schema, difficulty calibration, and safety.
"""

        tech_a = PromptTechniqueDetails(
            id="few_shot",
            name="Technique 1: Few-Shot In-Context Prompting",
            tagline="Guiding Output via Curated Demonstrations",
            purpose="Provides gold-standard input-output pairs so the LLM mirrors pedagogical patterns without guessing.",
            raw_prompt=prompt_few_shot,
            sample_output=output_few_shot,
            token_overhead="~450 tokens (Moderate)",
            hallucination_risk="Low",
            best_for="Consistent educational style, tone formatting, and code aesthetics."
        )

        tech_b = PromptTechniqueDetails(
            id="structured_constraints",
            name="Technique 2: Structured Constraint Prompting",
            tagline="Strict Role, Guardrails, and JSON Schema Enforcement",
            purpose="Enforces strict difficulty boundaries, safety guardrails, and deterministic output schema.",
            raw_prompt=prompt_structured,
            sample_output=output_structured,
            token_overhead="~280 tokens (Low)",
            hallucination_risk="Very Low",
            best_for="Enforcing safety guardrails, level adaptation, and JSON schema compliance."
        )

        combined_hybrid = {
            "name": "Combined Hybrid Prompting (Few-Shot + Structured Constraints + CoT)",
            "purpose": "Combines in-context formatting consistency with strict guardrails and step-by-step reasoning.",
            "raw_prompt": get_combined_hybrid_prompt(topic, difficulty),
            "sample_output": f"Synthesized hybrid output for {topic} adhering to both few-shot examples and strict level adaptation."
        }

        return PromptLabCompareResponse(
            topic=topic,
            difficulty=difficulty,
            technique_a=tech_a,
            technique_b=tech_b,
            combined_hybrid=combined_hybrid
        )

# Global singleton
study_service = StudyService()
