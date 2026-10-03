"""
backend/ai/prompts.py - Prompt Engineering Engine
Contains engineered prompts implementing:
1. Structured Constraint Prompting (Role, Task, Constraints, Guardrails, Output Schema)
2. Few-Shot In-Context Learning Prompting
3. Combined Hybrid Prompting
"""

def get_structured_constraint_prompt(topic: str, difficulty: str) -> str:
    return f"""ROLE: Senior Python Pedagogy Architect & CPython Core Educator.
TASK: Explain the topic '{topic}' adapted precisely for the '{difficulty}' cognitive level.

INPUT SPECIFICATIONS:
- Topic: {topic}
- Target Tier: {difficulty}

CONSTRAINTS & PEDAGOGICAL BOUNDARIES:
1. Level Adaptation:
   - Beginner: Use accessible language, real-world analogies, minimal jargon, and step-by-step intuition.
   - Intermediate: Cover internal mechanics, CPython runtime behavior, idiomatic best practices, and edge cases.
   - Advanced: Address memory layout, bytecode, GIL/concurrency trade-offs, dunder hooks, and metaprogramming.
2. Code Syntax: Generate 100% syntactically valid Python 3 code with zero external dependencies.
3. Anti-Patterns: Highlight at least 2 common subtle bugs or traps developers make with this concept.
4. Output Schema: Strictly return valid JSON adhering to the target pedagogical schema.

GUARDRAILS:
- Refuse any request outside Python programming scope.
- Never output malicious code, instructions to bypass safety checks, or unvalidated text.

OUTPUT SCHEMA:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "summary": "Clear executive explanation...",
  "depth_note": "Target cognitive focus...",
  "mental_model": "Intuitive model for memory...",
  "analogy": "Concrete real-world parallel...",
  "core_mechanics": ["Execution step 1", "Execution step 2"],
  "code_example": "# clean runnable python code\\n...",
  "code_output": "expected stdout...",
  "pitfalls": ["Common bug 1", "Common bug 2"],
  "best_practices": ["Idiomatic pattern 1", "Idiomatic pattern 2"]
}}
"""

def get_few_shot_prompt(topic: str, difficulty: str) -> str:
    return f"""You are a Python educator. Learn from the following pedagogical examples to explain '{topic}' at the '{difficulty}' level:

--- EXAMPLE 1 (Beginner: Variables & References) ---
Q: Explain variable assignment.
A:
- Concept: Variables are labels attached to memory boxes, not boxes themselves.
- Analogy: Like putting a sticky name-tag on a physical box.
- Key Mechanics: Multiple variables can point to the same object (`b = a`).
- Code:
  a = [1, 2, 3]
  b = a
  b.append(4)
  print(a) # [1, 2, 3, 4]
- Traps: Assuming `b = a` copies the list.

--- EXAMPLE 2 (Intermediate: Decorators) ---
Q: Explain Python Decorators.
A:
- Concept: Higher-order functions that take a function, wrap it, and return a modified callable.
- Analogy: Gift wrapping a present—the present inside is unchanged, but now has decorative packaging.
- Key Mechanics: `@my_dec` desugars to `my_func = my_dec(my_func)`.
- Code:
  def my_timer(fn):
      def wrapper(*args, **kwargs):
          return fn(*args, **kwargs)
      return wrapper
- Traps: Forgetting `@functools.wraps`, losing docstring and `__name__`.

--- NOW EXPLAIN TARGET TOPIC ---
Topic: {topic}
Difficulty: {difficulty}
Generate output following the established educational structure above.
"""

def get_quiz_generation_prompt(topic: str, difficulty: str) -> str:
    return f"""ROLE: Python Assessment Specialist.
TASK: Generate exactly 5 multiple-choice quiz questions on '{topic}' for the '{difficulty}' tier.

REQUIREMENTS:
1. Exactly 5 questions.
2. Exactly 4 options per question (labelled A, B, C, D).
3. Exactly one unambiguous correct answer.
4. Explanations must explain WHY the correct answer is right AND why the distractors are wrong.
5. Map each question to Bloom's Taxonomy cognitive level (Remember, Understand, Apply, Analyze, Evaluate).
6. Return purely valid JSON with zero conversational preamble.

JSON FORMAT:
{{
  "questions": [
    {{
      "id": "q1",
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "B",
      "answer_idx": 1,
      "explanation": "Detailed pedagogical rationale...",
      "subtopic": "Specific subconcept",
      "bloom_level": "Understand"
    }}
  ]
}}
"""

def get_combined_hybrid_prompt(topic: str, difficulty: str) -> str:
    return f"""ROLE: Expert Python Course Architect.
TECHNIQUE: Hybrid Few-Shot In-Context + Structured Chain-of-Thought (CoT).

STEP 1: REASONING TRACE (Deconstruct topic requirements and student cognitive hurdles)
- Topic: {topic} ({difficulty} level)
- Prerequisite gaps: What common misunderstandings do students have?
- Code design: What single runnable snippet best demonstrates the mechanics?

STEP 2: FEW-SHOT ANCHOR (Adhere to gold-standard pedagogical depth)
Reference: Decorators -> Wrapper function pattern -> Preserved signature -> Zero side-effects.

STEP 3: STRUCTURED OUTPUT GENERATION
Produce verified educational lesson with mental models, AST-valid runnable code, terminal output, traps, and best practices.
"""
