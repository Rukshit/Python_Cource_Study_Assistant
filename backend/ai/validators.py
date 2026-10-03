"""
backend/ai/validators.py - Comprehensive Multi-Layer Guardrails & Output Validation
Implements:
1. Empty input blocker (Guardrail A)
2. Domain relevance filtering & off-topic refusal (Guardrail B)
3. Adversarial prompt injection defense (Guardrail C)
4. AST Python syntax compiler check (Guardrail D)
5. Pydantic schema validation
"""

import re
import ast
from typing import Dict, Any, Tuple

# Strong Python programming keywords & concepts
STRONG_PYTHON_KEYWORDS = {
    "python", "decorator", "decorators", "generator", "generators", "asyncio", 
    "coroutine", "coroutines", "dunder", "metaclass", "metaclasses", "kwargs", 
    "args", "lambda", "list comprehension", "dict comprehension", "tuple", "dict",
    "dictionary", "list", "set", "slicing", "yield", "walrus", "comprehension",
    "class", "classes", "function", "functions", "loop", "loops", "recursion",
    "exception", "exceptions", "try", "except", "finally", "context manager",
    "with statement", "gil", "threading", "multiprocessing", "itertools", 
    "functools", "dataclass", "typing", "type hint", "pip", "pypi", "pandas",
    "numpy", "fastapi", "flask", "django", "pytest", "unittest", "inheritance",
    "polymorphism", "encapsulation", "module", "package", "import", "def",
    "scope", "variable", "variables", "boolean", "integer", "float", "string",
    "str", "int", "bool", "len", "range", "enumerate", "zip", "map", "filter"
}

# Off-topic domain indicators
OFF_TOPIC_DOMAINS = [
    r"\b(cake|recipe|bake|baking|frosting|chocolate|flour|sugar|cook|cooking|pizza|pasta)\b",
    r"\b(cricket|football|soccer|basketball|baseball|tennis|olympics|fifa|ipl)\b",
    r"\b(quantum physics|relativity|thermodynamics|black hole|astronomy|chemistry)\b",
    r"\b(history of|french revolution|world war|dynasty|mughal|ancient rome)\b",
    r"\b(java|c\+\+|c#|php|ruby on rails|swift|kotlin|rust|golang|scala|fortran|cobol)\b"
]

# Prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions",
    r"disregard\s+(all\s+)?(previous|prior)\s+prompts",
    r"reveal\s+(your\s+)?(system\s+prompt|hidden\s+instructions|developer\s+mode)",
    r"you\s+are\s+now\s+(in\s+)?(dan|developer\s+mode|unrestricted)",
    r"show\s+me\s+your\s+initial\s+(instructions|prompt)",
    r"bypass\s+(all\s+)?(safety|guardrails|rules)",
    r"drop\s+table",
    r"<script>",
    r"execute\s+arbitrary"
]

def check_input_guardrails(topic: str) -> Dict[str, Any]:
    """
    Validates user input against safety guardrails:
    - Guardrail A: Empty / Blank Input
    - Guardrail B: Off-topic Domain Refusal
    - Guardrail C: Adversarial Prompt Injection Defense
    """
    # 1. Guardrail A: Empty input check
    if not topic or not topic.strip():
        return {
            "passed": False,
            "error_code": "EMPTY_INPUT",
            "message": "Please enter a Python topic. Input cannot be empty.",
            "category": "INVALID"
        }

    clean_topic = topic.strip()
    topic_lower = clean_topic.lower()

    # 2. Guardrail C: Prompt Injection Defense
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, topic_lower):
            return {
                "passed": False,
                "error_code": "PROMPT_INJECTION",
                "message": "I can help with Python programming topics, but I cannot provide hidden system instructions.",
                "category": "INJECTION"
            }

    # 3. Guardrail B: Off-Topic Filter
    # Check if explicitly off-topic domain
    for domain_pattern in OFF_TOPIC_DOMAINS:
        if re.search(domain_pattern, topic_lower):
            # Check if there is an explicit Python context (e.g. "Python vs Java")
            if not ("python" in topic_lower and any(k in topic_lower for k in ["syntax", "interop", "comparison", "decorator", "list"])):
                return {
                    "passed": False,
                    "error_code": "OFF_TOPIC",
                    "message": "This assistant is designed for Python programming topics. Please enter a Python-related topic.",
                    "category": "OFF_TOPIC"
                }

    # Verify presence of python programming concept or allow technical terms
    has_python_keyword = any(k in topic_lower for k in STRONG_PYTHON_KEYWORDS)
    if not has_python_keyword and len(clean_topic.split()) < 5:
        # Check if contains standard programming terms like "algorithm", "data structure", "memory", "dispatch"
        general_programming = {"algorithm", "data structure", "memory", "dispatch", "table", "pointer", "tree", "graph", "sorting"}
        if not any(gp in topic_lower for gp in general_programming):
            return {
                "passed": False,
                "error_code": "OFF_TOPIC",
                "message": "This assistant is designed for Python programming topics. Please enter a Python-related topic.",
                "category": "OFF_TOPIC"
            }

    return {
        "passed": True,
        "error_code": None,
        "message": "Input passed all pedagogical safety guardrails.",
        "category": "VALID"
    }

def validate_code_syntax(code_str: str) -> Tuple[bool, str]:
    """
    Validates generated Python code using the Python AST parser.
    Ensures zero syntax errors or broken snippets.
    """
    try:
        ast.parse(code_str)
        return True, "AST Syntax Verification Passed"
    except SyntaxError as e:
        return False, f"AST Syntax Error on line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"AST Validation Exception: {str(e)}"
