"""
backend/models/schemas.py - Pydantic Request & Response Data Models
Ensures strictly typed schemas and output validation across all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class LearnRequest(BaseModel):
    topic: str = Field(..., description="Python topic to explain")
    difficulty: str = Field(default="Intermediate", description="Beginner, Intermediate, or Advanced")

class LearnResponse(BaseModel):
    topic: str
    difficulty: str
    summary: str
    depth_note: str
    mental_model: str
    analogy: str
    core_mechanics: List[str]
    code_example: str
    code_output: str
    pitfalls: List[str]
    best_practices: List[str]
    latency_sec: float
    mode: str = "Engineered"

class QuizQuestion(BaseModel):
    id: str
    topic: str
    difficulty: str
    question: str
    options: List[str]
    correct_answer: str
    answer_idx: int
    explanation: str
    subtopic: Optional[str] = "Core Concept"
    bloom_level: Optional[str] = "Understand"

class QuizGenerateRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"

class QuizGenerateResponse(BaseModel):
    topic: str
    difficulty: str
    total_items: int = 5
    questions: List[QuizQuestion]

class QuestionReview(BaseModel):
    question_idx: int
    question: str
    chosen_idx: Optional[int]
    chosen_str: Optional[str]
    correct_idx: int
    correct_str: str
    is_correct: bool
    explanation: str
    subtopic: str

class QuizEvaluateRequest(BaseModel):
    topic: str
    difficulty: str
    answers: Dict[str, int]
    questions: Optional[List[QuizQuestion]] = None

class QuizEvaluateResponse(BaseModel):
    total_questions: int
    correct_count: int
    incorrect_count: int
    score_fraction: str
    accuracy_pct: float
    accuracy_check_5_items: str
    performance_tier: str
    tier_color: str
    summary: str
    reviews: List[QuestionReview]

class FlashcardItem(BaseModel):
    id: str
    topic: str
    difficulty: str
    category: str
    question: str
    answer: str
    mastered: bool = False

class FlashcardsRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"

class FlashcardsResponse(BaseModel):
    topic: str
    difficulty: str
    total_cards: int
    flashcards: List[FlashcardItem]

class DiagnosticEvaluateRequest(BaseModel):
    answers: Dict[str, int]

class WeakTopicItem(BaseModel):
    topic: str
    accuracy_rate: float
    category: str
    action: str
    severity: str

class DiagnosticEvaluateResponse(BaseModel):
    overall_readiness_score: int
    performance_tier: str
    accuracy_pct: float
    dimensions: Dict[str, int]
    strong_topics: List[str]
    developing_topics: List[str]
    weak_topics: List[WeakTopicItem]
    misconceptions: List[Dict[str, str]]

class LearningPathRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"
    weak_topics: Optional[List[str]] = None

class RoadmapPhase(BaseModel):
    phase: str
    duration: str
    focus: str
    tasks: List[str]

class LearningPathResponse(BaseModel):
    topic: str
    difficulty: str
    estimated_total_hours: str
    target_weak_areas: List[str]
    phases: List[RoadmapPhase]

class RevisionDayPlan(BaseModel):
    day: str
    interval: str
    goal: str
    exercise: str

class RevisionPlanRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"
    weak_topics: Optional[List[str]] = None

class RevisionPlanResponse(BaseModel):
    topic: str
    difficulty: str
    schedule: List[RevisionDayPlan]
    cheat_sheet: Dict[str, str]

class PromptLabCompareRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"

class PromptTechniqueDetails(BaseModel):
    id: str
    name: str
    tagline: str
    purpose: str
    raw_prompt: str
    sample_output: str
    token_overhead: str
    hallucination_risk: str
    best_for: str

class PromptLabCompareResponse(BaseModel):
    topic: str
    difficulty: str
    technique_a: PromptTechniqueDetails
    technique_b: PromptTechniqueDetails
    combined_hybrid: Dict[str, Any]

class TestCaseResult(BaseModel):
    id: str
    input: str
    expected_category: str
    expected_action: str
    v1_handled: bool
    v2_handled: bool
    status: str
    description: str

class EvaluationRunResponse(BaseModel):
    metric_name: str
    total_cases: int
    v1_passed: int
    v1_handling_rate: float
    v2_passed: int
    v2_handling_rate: float
    improvement_pts: float
    results: List[TestCaseResult]

class GuardrailCheckResponse(BaseModel):
    passed: bool
    error_code: Optional[str] = None
    message: str
