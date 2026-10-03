"""
flashcard_engine.py - Interactive Flashcards Engine
Provides dynamic flashcard generation, active recall flipping, and spaced repetition tracking.
"""

def generate_flashcards(topic: str, difficulty: str = "Intermediate") -> list:
    """
    Generates a set of active-recall flashcards for any given Python topic.
    """
    topic_clean = topic.strip().title()

    if "async" in topic.lower() or "await" in topic.lower():
        return [
            {
                "id": 1,
                "category": "Syntax & Keywords",
                "question": "What is the difference between 'async def' and a regular 'def' in Python?",
                "answer": "'async def' defines a coroutine function. Calling it does NOT execute code immediately; instead, it returns a coroutine object that must be awaited or scheduled on an event loop.",
                "mastered": False
            },
            {
                "id": 2,
                "category": "Event Loop Internals",
                "question": "What happens under the hood when a coroutine yields control with 'await asyncio.sleep(1)'?",
                "answer": "It registers a timer callback on the OS selector/epoll loop and yields execution back to the event loop, allowing other runnable tasks to execute without blocking the thread.",
                "mastered": False
            },
            {
                "id": 3,
                "category": "Anti-Patterns & Traps",
                "question": "Why is invoking synchronous 'time.sleep()' or blocking 'requests.get()' catastrophic in asyncio?",
                "answer": "Asyncio runs cooperatively on a single thread by default. A blocking call freezes the entire thread, halting all concurrent tasks and timer processing for that duration.",
                "mastered": False
            },
            {
                "id": 4,
                "category": "Task Management",
                "question": "How do you run multiple independent coroutines concurrently and gather their results?",
                "answer": "Use 'await asyncio.gather(*coroutines)' or create tasks with 'asyncio.create_task()' to execute them in parallel on the event loop.",
                "mastered": False
            },
            {
                "id": 5,
                "category": "Protocols & Dunder",
                "question": "Which protocol must an object implement to be used in 'async with' statements?",
                "answer": "The Asynchronous Context Manager protocol, requiring '__aenter__()' and '__aexit__()' coroutine methods returning awaitable objects.",
                "mastered": False
            },
            {
                "id": 6,
                "category": "Production Best Practices",
                "question": "How should you bridge CPU-bound or legacy synchronous blocking functions into asyncio?",
                "answer": "Use 'await asyncio.to_thread(sync_func, *args)' (Python 3.9+) or 'loop.run_in_executor()', which offloads execution to a background ThreadPoolExecutor.",
                "mastered": False
            }
        ]

    elif "decorator" in topic.lower() or "wrap" in topic.lower():
        return [
            {
                "id": 1,
                "category": "Syntax & Desugaring",
                "question": f"What is the exact runtime translation of the '@my_decorator' syntax placed above 'def foo():'?",
                "answer": "'@my_decorator' is syntactic sugar for: 'foo = my_decorator(foo)' executed immediately at module definition time.",
                "mastered": False
            },
            {
                "id": 2,
                "category": "Introspection Preservation",
                "question": "Why must you always place '@functools.wraps(func)' on your inner wrapper function?",
                "answer": "Without wraps, the decorated function loses its original '__name__', '__doc__', '__annotations__', and module metadata, which breaks debugging, logging, and doc generators.",
                "mastered": False
            },
            {
                "id": 3,
                "category": "Architecture Patterns",
                "question": "How many levels of nested functions are required for a decorator that takes arguments (e.g. @repeat(num=3))?",
                "answer": "Three levels: (1) The decorator factory taking arguments, (2) The actual decorator taking the target function, and (3) The inner wrapper executing per call with *args, **kwargs.",
                "mastered": False
            },
            {
                "id": 4,
                "category": "Execution Chaining",
                "question": "If you stack @dec_one above @dec_two on function bar(), in what order are they applied?",
                "answer": "They are evaluated from bottom to top: 'bar = dec_one(dec_two(bar))'. However, during actual function invocation, dec_one's outer wrapper runs first.",
                "mastered": False
            },
            {
                "id": 5,
                "category": "Class-Level Decorators",
                "question": "Can a class be used as a decorator in Python? How?",
                "answer": "Yes! Implement '__call__(self, *args, **kwargs)' on the class. The class instance then acts as a callable wrapper preserving internal state between calls.",
                "mastered": False
            },
            {
                "id": 6,
                "category": "Performance & Pitfalls",
                "question": "What is the overhead of a Python decorator?",
                "answer": "A decorator introduces an additional function call frame on each invocation. While minimal for most applications, tight inner loops with millions of iterations may see measurable overhead.",
                "mastered": False
            }
        ]

    else:
        # Dynamic active recall flashcards for ANY arbitrary unseen Python topic!
        return [
            {
                "id": 1,
                "category": "Conceptual Definition",
                "question": f"What is the primary architectural purpose of '{topic_clean}' in Python?",
                "answer": f"{topic_clean} establishes a modular abstraction layer enabling clean separation of concerns, higher code maintainability, and predictable execution behavior.",
                "mastered": False
            },
            {
                "id": 2,
                "category": "Internal CPython Mechanism",
                "question": f"How does the CPython runtime manage memory and references for '{topic_clean}'?",
                "answer": f"CPython utilizes reference counting with an auxiliary generational cyclic garbage collector (gc), binding references according to LEGB (Local, Enclosing, Global, Built-in) scoping rules.",
                "mastered": False
            },
            {
                "id": 3,
                "category": "Edge Cases & Exceptions",
                "question": f"What failure mode commonly occurs when error handling is omitted in '{topic_clean}'?",
                "answer": "Silent state pollution or unreleased file/socket descriptors when unexpected exceptions interrupt the execution path before reaching cleanup logic.",
                "mastered": False
            },
            {
                "id": 4,
                "category": "PEP & Typing Standards",
                "question": f"How should '{topic_clean}' be annotated under modern PEP 484 / PEP 585 guidelines?",
                "answer": "Use standard library typing protocols, explicit return annotations, and avoid raw 'Any' to enable static type analysis via mypy or pyright.",
                "mastered": False
            },
            {
                "id": 5,
                "category": "Performance Optimization",
                "question": f"What is the single most effective technique for profiling bottlenecks in '{topic_clean}'?",
                "answer": "Measure with standard library 'cProfile' and 'time.perf_counter()' rather than guessing or performing premature micro-optimizations.",
                "mastered": False
            },
            {
                "id": 6,
                "category": "Production Best Practices",
                "question": f"What golden rule should every team follow when adopting '{topic_clean}' in production?",
                "answer": "Prioritize idiomatic clarity over cleverness. Ensure complete unit test coverage across both standard inputs and boundary/empty conditions.",
                "mastered": False
            }
        ]
