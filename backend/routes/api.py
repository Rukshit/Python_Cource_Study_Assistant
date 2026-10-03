"""
backend/routes/api.py - REST API Route Definitions
Exposes all endpoints required by the Master Prompt specification.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import json
from pathlib import Path
from datetime import datetime

from backend.models.schemas import (
    LearnRequest,
    LearnResponse,
    QuizGenerateRequest,
    QuizGenerateResponse,
    QuizEvaluateRequest,
    QuizEvaluateResponse,
    FlashcardsRequest,
    FlashcardsResponse,
    DiagnosticEvaluateRequest,
    DiagnosticEvaluateResponse,
    LearningPathRequest,
    LearningPathResponse,
    RevisionPlanRequest,
    RevisionPlanResponse,
    PromptLabCompareRequest,
    PromptLabCompareResponse,
    EvaluationRunResponse
)
from backend.services.study_service import study_service
from backend.evaluation.evaluator import evaluator

router = APIRouter(prefix="/api", tags=["Study Assistant API"])

LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Python Course Study Assistant",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0-Engineered"
    }

@router.get("/topics")
def get_topics():
    return {"topics": study_service.topics_data}

@router.post("/learn", response_model=LearnResponse)
def explain_topic(req: LearnRequest):
    return study_service.explain_topic(req.topic, req.difficulty)

@router.post("/quiz/generate", response_model=QuizGenerateResponse)
def generate_quiz(req: QuizGenerateRequest):
    questions = study_service.generate_quiz(req.topic, req.difficulty)
    return QuizGenerateResponse(
        topic=req.topic,
        difficulty=req.difficulty,
        total_items=len(questions),
        questions=questions
    )

@router.post("/quiz/evaluate", response_model=QuizEvaluateResponse)
def evaluate_quiz(req: QuizEvaluateRequest):
    return study_service.evaluate_quiz(
        topic=req.topic,
        difficulty=req.difficulty,
        answers=req.answers,
        questions=req.questions
    )

@router.post("/flashcards", response_model=FlashcardsResponse)
def get_flashcards(req: FlashcardsRequest):
    cards = study_service.generate_flashcards(req.topic, req.difficulty)
    return FlashcardsResponse(
        topic=req.topic,
        difficulty=req.difficulty,
        total_cards=len(cards),
        flashcards=cards
    )

@router.post("/diagnostic/generate")
def get_diagnostic_quiz():
    questions = study_service.get_diagnostic_questions()
    return {
        "total_items": len(questions),
        "questions": [q.model_dump() for q in questions]
    }

@router.post("/diagnostic/evaluate", response_model=DiagnosticEvaluateResponse)
def evaluate_diagnostic(req: DiagnosticEvaluateRequest):
    return study_service.evaluate_diagnostic(req.answers)

@router.post("/learning-path", response_model=LearningPathResponse)
def generate_learning_path(req: LearningPathRequest):
    return study_service.generate_learning_path(
        topic=req.topic,
        difficulty=req.difficulty,
        weak_topics=req.weak_topics
    )

@router.post("/revision-plan", response_model=RevisionPlanResponse)
def generate_revision_plan(req: RevisionPlanRequest):
    return study_service.generate_revision_plan(
        topic=req.topic,
        difficulty=req.difficulty,
        weak_topics=req.weak_topics
    )

@router.post("/prompt-lab/compare", response_model=PromptLabCompareResponse)
def compare_prompts(req: PromptLabCompareRequest):
    return study_service.get_prompt_lab_comparison(req.topic, req.difficulty)

@router.post("/evaluation/run", response_model=EvaluationRunResponse)
def run_evaluation():
    return evaluator.run_evaluation()

@router.get("/history")
def get_prompt_history():
    history_file = LOGS_DIR / "prompt_history.md"
    content = ""
    if history_file.exists():
        with open(history_file, "r", encoding="utf-8") as f:
            content = f.read()
    return {
        "format": "markdown",
        "content": content
    }
