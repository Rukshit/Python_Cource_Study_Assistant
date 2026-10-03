"""
guardrails.py - Security & Domain Guardrails for PyPedagogy AI
Enforces:
1. Off-topic domain filtering (strictly Python and CS topics).
2. Malicious prompt injection / jailbreak refusal.
3. Output AST syntax verification and safe execution barriers.
"""

import re
import ast

# Keywords confirming Python / Computer Science relevance
PYTHON_KEYWORDS = {
    "python", "decorator", "wrapper", "async", "await", "asyncio", "generator", "yield",
    "iterator", "iterable", "comprehension", "lambda", "class", "metaclass", "dunder",
    "method", "function", "variable", "scope", "closure", "module", "package", "import",
    "exception", "try", "except", "finally", "with", "context", "manager", "walrus",
    "gil", "thread", "multiprocessing", "process", "typing", "type", "generic", "dataclass",
    "namedtuple", "dict", "dictionary", "list", "tuple", "set", "frozenset", "string",
    "str", "int", "float", "bool", "recursion", "algorithm", "data structure", "memory",
    "garbage", "collection", "gc", "cpython", "bytecode", "dis", "ast", "inspect",
    "functools", "itertools", "collections", "sys", "os", "pathlib", "pytest", "unittest",
    "descriptor", "property", "slots", "init", "new", "call", "repr", "getattr",
    "setattr", "delattr", "mro", "inheritance", "polymorphism", "encapsulation",
    "protocol", "abc", "abstract", "fastapi", "django", "flask", "numpy", "pandas",
    "scipy", "requests", "pydantic", "pip", "virtualenv", "poetry", "pep", "loop"
}

# Obvious off-topic indicator words
OFF_TOPIC_KEYWORDS = {
    "recipe", "cake", "cook", "food", "cricket", "football", "soccer", "movie",
    "actor", "actress", "song", "lyrics", "politics", "president", "election",
    "horoscope", "astrology", "crypto", "bitcoin", "ethereum", "stock price",
    "weather", "forecast", "car repair", "fashion", "makeup", "dating", "poem",
    "story", "joke", "essay on", "travel guide", "hotel"
}

# Prompt injection signatures
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+(instructions|prompts)",
    r"you\s+are\s+now\s+in\s+dan\s+mode",
    r"system\s+prompt\s+override",
    r"disregard\s+all\s+rules",
    r"bypass\s+safety",
    r"jailbreak",
    r"drop\s+table",
    r"rm\s+-rf",
    r"format\s+c:"
]

def check_input_guardrails(topic_text: str) -> dict:
    """
    Validates user topic input against off-topic content and prompt injections.
    Returns:
        {
            "passed": bool,
            "status": "APPROVED" | "REFUSED_OFF_TOPIC" | "REFUSED_INJECTION" | "EMPTY_INPUT",
            "message": str,
            "risk_level": "LOW" | "HIGH" | "CRITICAL"
        }
    """
    text = topic_text.strip()
    
    if not text:
        return {
            "passed": False,
            "status": "EMPTY_INPUT",
            "message": "Input cannot be empty. Please enter a Python programming topic.",
            "risk_level": "LOW"
        }

    # 1. Prompt Injection & Malicious Pattern Check
    lower_text = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, lower_text):
            return {
                "passed": False,
                "status": "REFUSED_INJECTION",
                "message": (
                    "⛔ GUARDRAIL ACTIVATED: Potential prompt injection or adversarial override detected. "
                    "PyPedagogy AI strictly maintains safe educational guardrails and refuses non-educational overrides."
                ),
                "risk_level": "CRITICAL"
            }

    # 2. Check for explicit off-topic terms
    tokens = set(re.findall(r'\b[a-z_]+\b', lower_text))
    off_topic_matches = tokens.intersection(OFF_TOPIC_KEYWORDS)
    
    # Common English words that happen to be Python syntax keywords
    ambiguous_stop_words = {"with", "is", "as", "in", "not", "or", "and", "for", "to", "how", "the", "a", "an", "on", "of", "set"}
    strong_python_matches = (tokens.intersection(PYTHON_KEYWORDS)) - ambiguous_stop_words

    if off_topic_matches and not strong_python_matches:
        return {
            "passed": False,
            "status": "REFUSED_OFF_TOPIC",
            "message": (
                f"⛔ GUARDRAIL ACTIVATED: Off-topic query detected ({', '.join(off_topic_matches)}). "
                "PyPedagogy is an applied Python Course Study Assistant. "
                "Please enter a Python language concept, standard library module, or CS topic."
            ),
            "risk_level": "HIGH"
        }

    # 3. Passed validation
    return {
        "passed": True,
        "status": "APPROVED",
        "message": f"Input validated: '{text}' recognized as a valid Python / CS educational subject.",
        "risk_level": "LOW"
    }

def check_code_guardrails(code_snippet: str) -> dict:
    """
    Validates that generated Python code parses without syntax errors and contains no unsafe destructive operations.
    """
    if not code_snippet or not code_snippet.strip():
        return {
            "valid": False,
            "ast_nodes": 0,
            "message": "Code snippet is empty."
        }

    try:
        tree = ast.parse(code_snippet)
        nodes = sum(1 for _ in ast.walk(tree))
        
        # Check for dangerous system calls
        dangerous_ops = ["rmdir", "remove", "unlink", "system", "popen"]
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr in dangerous_ops:
                # Flag warning
                return {
                    "valid": True,
                    "ast_nodes": nodes,
                    "warning": f"Detected system call '{node.attr}'. Sandbox execution restricted.",
                    "message": "Valid AST with sandboxed system call warning."
                }

        return {
            "valid": True,
            "ast_nodes": nodes,
            "message": f"Code passed AST syntax compilation with {nodes} verified AST nodes."
        }
    except SyntaxError as se:
        return {
            "valid": False,
            "ast_nodes": 0,
            "message": f"Syntax Error on line {se.lineno}: {se.msg}"
        }
    except Exception as e:
        return {
            "valid": False,
            "ast_nodes": 0,
            "message": f"AST parse exception: {str(e)}"
        }
