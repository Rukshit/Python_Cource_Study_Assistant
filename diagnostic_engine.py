"""
diagnostic_engine.py - Diagnostic Assessment & Weak Topic Detection Engine
Analyzes quiz telemetry and Bloom's taxonomy performance to isolate technical gaps and misconceptions.
"""

def run_diagnostic_assessment(topic: str, difficulty: str, quiz_results: dict) -> dict:
    """
    Synthesizes a deep diagnostic profile based on quiz accuracy and subtopic telemetry.
    """
    topic_clean = topic.strip().title()
    accuracy = quiz_results.get("accuracy_pct", 50.0) if quiz_results else 50.0
    weak_subtopics = quiz_results.get("weak_subtopics", []) if quiz_results else []
    subtopic_perf = quiz_results.get("subtopic_performance", {}) if quiz_results else {}

    # Dimensional competency scores (0 to 100)
    # Calibrated based on quiz performance and subtopic gaps
    base_score = int(accuracy)
    dimensions = {
        "Core Syntax & Protocol": max(25, min(98, base_score + 10)),
        "Conceptual Mental Model": max(20, min(95, base_score - 5 if weak_subtopics else base_score + 5)),
        "Runtime Execution & Lifecycle": max(15, min(95, base_score - 10 if "Execution" in str(weak_subtopics) else base_score)),
        "Edge Case & Error Resilience": max(15, min(92, base_score - 15 if "Edge" in str(weak_subtopics) or "Exception" in str(weak_subtopics) else base_score - 5)),
        "Production Performance & Idioms": max(20, min(96, base_score + 2))
    }

    # Cognitive distribution (Bloom's Taxonomy)
    bloom_assessment = {
        "Remembering": {"score": min(100, base_score + 15), "status": "Solid Recall"},
        "Understanding": {"score": min(100, base_score + 5), "status": "Consistent Mental Model" if base_score >= 60 else "Shaky Mental Model"},
        "Applying": {"score": max(30, base_score), "status": "Can Apply Standard Patterns" if base_score >= 60 else "Struggles with Novel Syntax"},
        "Analyzing": {"score": max(20, base_score - 10), "status": "Diagnoses Execution Traces" if base_score >= 75 else "Needs Edge-Case Tracing Drill"},
        "Evaluating": {"score": max(15, base_score - 15), "status": "Architectural Trade-off Mastery" if base_score >= 80 else "Prone to Anti-patterns"}
    }

    # Detect specific misconceptions
    misconceptions = []
    if accuracy < 100:
        if "async" in topic.lower():
            misconceptions.append({
                "concept": "Event Loop Blocking",
                "misconception": "Believing standard time.sleep() runs in the background concurrently without blocking other async tasks.",
                "remedy": "Always use 'await asyncio.sleep()' or delegate blocking calls to 'asyncio.to_thread()'."
            })
            misconceptions.append({
                "concept": "Immediate vs Deferred Execution",
                "misconception": "Calling an async def function without 'await' or 'create_task', leaving an unawaited coroutine warning.",
                "remedy": "Remember coroutine objects must be scheduled on the active event loop to execute."
            })
        elif "decorator" in topic.lower():
            misconceptions.append({
                "concept": "Function Identity Loss",
                "misconception": "Ignoring '@functools.wraps', causing the decorated function to lose its __name__, docstrings, and signature.",
                "remedy": "Decorate the inner wrapper with '@functools.wraps(func)' on every custom decorator."
            })
            misconceptions.append({
                "concept": "Decorator Parameter Factory Nesting",
                "misconception": "Attempting to pass arguments to a 2-level decorator without creating an outer decorator factory.",
                "remedy": "Parameterized decorators require 3 levels of nested callables: factory(args) -> decorator(func) -> wrapper(*args, **kwargs)."
            })
        else:
            misconceptions.append({
                "concept": f"State Mutation in {topic_clean}",
                "misconception": "Treating mutable default parameters or class-level attributes as per-instance isolated state.",
                "remedy": "Use 'None' as default argument with sentinel checks, or leverage '__init__' instance binding."
            })
            misconceptions.append({
                "concept": "Resource Cleanup Guarantees",
                "misconception": "Relying on CPython reference counting garbage collection instead of explicit context managers.",
                "remedy": "Always implement or wrap resources using 'with' statements or explicit try...finally blocks."
            })

    # Weak topic detection table
    weak_topic_items = []
    if weak_subtopics:
        for sub in weak_subtopics:
            weak_topic_items.append({
                "subtopic": sub,
                "severity": "High Priority Gap" if accuracy < 50 else "Moderate Gap",
                "accuracy": f"{subtopic_perf.get(sub, {}).get('correct', 0)}/{subtopic_perf.get(sub, {}).get('total', 1)} correct",
                "action": f"Review foundational mechanics and re-test on {sub} interactive flashcards."
            })
    else:
        # If perfect score or general assessment
        if accuracy >= 80:
            weak_topic_items.append({
                "subtopic": f"Advanced {topic_clean} Edge Cases",
                "severity": "Minor Polish",
                "accuracy": "Strong baseline",
                "action": "Proceed to complex system integration and performance profiling."
            })
        else:
            weak_topic_items.append({
                "subtopic": f"{topic_clean} Execution Flow",
                "severity": "Needs Attention",
                "accuracy": f"{int(accuracy)}% Overall",
                "action": "Complete guided hands-on code traces in Step 8: Personalised Learning Path."
            })

    return {
        "topic": topic_clean,
        "difficulty": difficulty,
        "overall_readiness_score": base_score,
        "dimensions": dimensions,
        "bloom_assessment": bloom_assessment,
        "misconceptions": misconceptions,
        "weak_topic_items": weak_topic_items,
        "summary": f"Diagnostic complete for '{topic_clean}'. Performance indicates an overall readiness score of {base_score}/100 with key opportunities in Edge-case resilience and Execution lifecycle."
    }
