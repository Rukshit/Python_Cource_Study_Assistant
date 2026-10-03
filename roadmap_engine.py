"""
roadmap_engine.py - Personalized Learning Path and Spaced Repetition Revision Plan
Generates customized educational roadmaps and structured revision schedules based on diagnostic findings.
"""

def generate_personalized_roadmap(topic: str, difficulty: str, diagnostic_data: dict) -> dict:
    """
    Creates a tailored 4-phase learning roadmap targeting identified weak areas.
    """
    topic_clean = topic.strip().title()
    weak_subtopics = []
    if diagnostic_data and "weak_topic_items" in diagnostic_data:
        weak_subtopics = [item["subtopic"] for item in diagnostic_data["weak_topic_items"]]

    # Phase 1: Foundational Mental Model
    phase1_tasks = [
        f"Study the internal execution model of {topic_clean} in CPython.",
        "Sketch the runtime object diagram and frame execution sequence.",
        "Write 3 minimal working examples demonstrating default syntax."
    ]

    # Phase 2: Targeted Weak-Spot Remediation
    if weak_subtopics:
        phase2_focus = f"Targeted remediation on: {', '.join(weak_subtopics[:2])}"
        phase2_tasks = [
            f"Solve 2 guided debugging exercises focused on '{weak_subtopics[0]}'.",
            f"Analyze step-by-step trace of common anti-patterns in '{weak_subtopics[-1]}'.",
            "Write negative unit tests that intentionally trigger and catch expected exceptions."
        ]
    else:
        phase2_focus = f"Deepening Idiomatic Implementation for {topic_clean}"
        phase2_tasks = [
            "Refactor a naive implementation into an idiomatic, PEP-compliant version.",
            "Add robust type annotations with typing/collections.abc protocols.",
            "Write comprehensive docstrings adhering to Google or NumPy style."
        ]

    # Phase 3: Edge Cases & Production Resilience
    phase3_tasks = [
        f"Implement error recovery and defensive guards around {topic_clean}.",
        "Profile memory consumption and execution latency using 'cProfile' or 'tracemalloc'.",
        "Test behavior under high-concurrency or edge-boundary inputs."
    ]

    # Phase 4: Capstone Integration Project
    phase4_tasks = [
        f"Build an end-to-end production utility leveraging {topic_clean} (e.g. rate-limiter, pipeline processor, or plugin loader).",
        "Package the utility with a pyproject.toml and automated pytest suite.",
        "Perform a simulated code review against Python Software Foundation best practices."
    ]

    phases = [
        {
            "phase": "Phase 1: Conceptual Foundations & Mental Models",
            "duration": "Est. 2-3 Hours",
            "focus": "Core semantics, scoping, and runtime memory architecture",
            "tasks": phase1_tasks,
            "badge": "Foundational"
        },
        {
            "phase": f"Phase 2: Targeted Practice & Weak-Spot Remediation",
            "duration": "Est. 3-4 Hours",
            "focus": phase2_focus,
            "tasks": phase2_tasks,
            "badge": "High Priority"
        },
        {
            "phase": "Phase 3: Edge Cases, Resilience & Performance",
            "duration": "Est. 3-5 Hours",
            "focus": "Exception safety, concurrency safety, and runtime benchmarking",
            "tasks": phase3_tasks,
            "badge": "Intermediate"
        },
        {
            "phase": "Phase 4: Production Architecture & Capstone",
            "duration": "Est. 4-6 Hours",
            "focus": "Modular system design, unit testing, and real-world deployment",
            "tasks": phase4_tasks,
            "badge": "Advanced"
        }
    ]

    return {
        "topic": topic_clean,
        "difficulty": difficulty,
        "target_weak_areas": weak_subtopics,
        "phases": phases,
        "recommended_tools": ["pytest", "mypy", "ruff", "cProfile", "tracemalloc"],
        "estimated_total_hours": "12 - 18 Hours to Full Mastery"
    }

def generate_revision_plan(topic: str, difficulty: str) -> dict:
    """
    Creates a scientific spaced repetition revision schedule (Ebbinghaus forgetting curve).
    """
    topic_clean = topic.strip().title()

    schedule = [
        {
            "day": "Day 1",
            "interval": "24 Hours After Learning",
            "goal": "Immediate Consolidation & Active Retrieval",
            "exercise": f"Re-read the {topic_clean} Mental Model. Close your editor and write a minimal implementation entirely from memory.",
            "checklist": ["Trace execution flow on paper", "Run self-quiz without hints", "Validate syntax in REPL"]
        },
        {
            "day": "Day 3",
            "interval": "72 Hours After Learning",
            "goal": "First Retrieval Spike & Edge Case Testing",
            "exercise": f"Take 15 minutes to write 3 edge cases that break standard implementations of {topic_clean}.",
            "checklist": ["Test exception handling path", "Verify cleanup / resource release", "Review flashcards #1-4"]
        },
        {
            "day": "Day 7",
            "interval": "1 Week After Learning",
            "goal": "Interleaved Practice & Pattern Fusion",
            "exercise": f"Combine {topic_clean} with another Python paradigm (e.g. Combine with context managers or type generics).",
            "checklist": ["Complete an integrated mini-project", "Check PEP style guide compliance", "Review flashcards #5-8"]
        },
        {
            "day": "Day 14",
            "interval": "2 Weeks After Learning",
            "goal": "Mastery Validation & Long-Term Retention",
            "exercise": f"Teach {topic_clean} aloud using the Feynman Technique. Explain both the 'why' and internal CPython mechanics.",
            "checklist": ["Conduct a mock technical interview explanation", "Perform final speed drill", "Mark topic as Mastered"]
        }
    ]

    cheat_sheet = {
        "golden_rule": f"Always adhere to Python's principle of least surprise when implementing {topic_clean}.",
        "common_trap": "Premature complexity—strive for the simplest pattern that achieves correctness and maintainability.",
        "quick_test": f"import unittest; test both happy paths and boundary conditions before deploying {topic_clean}.",
        "pro_tip": "Pair with modern type annotations (PEP 484) to eliminate runtime surprises."
    }

    return {
        "topic": topic_clean,
        "difficulty": difficulty,
        "schedule": schedule,
        "cheat_sheet": cheat_sheet
    }
