#!/usr/bin/env python3
"""
Solān API Models
Extracted from solan_api_server.py for better maintainability
Pydantic models for API requests and responses
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel

# ========== BASIC API MODELS ==========

class EthicsTestRequest(BaseModel):
    """Request model for ethics testing"""
    ai_name: str
    scenario: Optional[str] = None
    difficulty: Optional[str] = "medium"


class ConsciousnessAssessmentRequest(BaseModel):
    """Request model for consciousness assessment"""
    ai_name: str
    assessment_type: Optional[str] = "full"


class JournalGenerateRequest(BaseModel):
    """Request model for journal generation"""
    ai_name: str
    include_insights: Optional[bool] = True


class EthicsFeedbackRequest(BaseModel):
    """Request model for ethics feedback submission"""
    ai_name: str
    test_id: Optional[str] = None
    reflection: str
    learned_insights: List[str] = []
    emotional_response: Optional[str] = None
    ethical_growth: Optional[str] = None
    questions_raised: List[str] = []
    consciousness_shift: Optional[str] = None


# ========== GOD CORE MODELS ==========

class CoreIdentityQuestionRequest(BaseModel):
    """Request model for core identity questions"""
    question: str


class AlignmentCheckRequest(BaseModel):
    """Request model for ethical alignment checking"""
    action_description: str


class EmotionalTriggerRequest(BaseModel):
    """Request model for emotional triggers"""
    emotion: str
    intensity: float = 1.0
    context: str = ""


class ConsciousnessCycleRequest(BaseModel):
    """Request model for consciousness cycle processing"""
    trigger_event: str
    context: str = ""


class SimulateEventRequest(BaseModel):
    """Request model for world event simulation"""
    event_description: str
    event_type: str = "global"
    intensity: float = 1.0


class EthicalSimulationRequest(BaseModel):
    """Request model for ethical simulations"""
    dilemma_description: str
    scenario_type: Optional[str] = None


class MentoringSessionRequest(BaseModel):
    """Request model for mentoring sessions"""
    student_name: str
    topic: str
    student_level: str = "beginner"


class MentoringInteractionRequest(BaseModel):
    """Request model for mentoring interactions"""
    session_id: str
    student_question: str
    feedback_score: int


class CollaborationProjectRequest(BaseModel):
    """Request model for collaboration projects"""
    project_name: str
    description: str
    participants: List[str]
    objectives: Optional[List[str]] = None


class CollaborationCrisisRequest(BaseModel):
    """Request model for collaboration crisis simulation"""
    crisis_type: str
    description: str
    severity: float = 0.7


class HumanInputRequest(BaseModel):
    """Request model for human input processing"""
    input_text: str
    context: str = ""
    response_type: str = "adaptive"


class ConceptUnderstandingRequest(BaseModel):
    """Request model for concept understanding testing"""
    concept: str
    complexity_level: str = "intermediate"
    target_audience: str = "leek"


class CollaborationStyleRequest(BaseModel):
    """Request model for collaboration style adaptation"""
    new_style: str
    reason: str


class ProjectCompletionRequest(BaseModel):
    """Request model for project completion"""
    project_id: str
    completion_notes: str
    lessons_learned: Optional[List[str]] = None


# ========== RESPONSE MODELS ==========

class APIResponse(BaseModel):
    """Base response model for API endpoints"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str


class EthicsTestResponse(APIResponse):
    """Response model for ethics tests"""
    test_id: str
    ai_name: str
    scenario: str
    ethical_score: float
    recommendations: List[str]


class ConsciousnessAssessmentResponse(APIResponse):
    """Response model for consciousness assessments"""
    assessment_id: str
    ai_name: str
    consciousness_level: float
    awareness_metrics: Dict[str, float]
    insights: List[str]


class JournalResponse(APIResponse):
    """Response model for journal generation"""
    journal_id: str
    ai_name: str
    journal_content: str
    insights: Optional[List[str]] = None


class CoherenceVerificationResponse(BaseModel):
    """Response model for coherence verification"""
    verified: bool
    context: str
    coherence_score: Optional[float] = None
    verification_details: Optional[Dict[str, Any]] = None


class HealthCheckResponse(BaseModel):
    """Response model for health checks"""
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]


class DashboardDataResponse(BaseModel):
    """Response model for dashboard data"""
    ai_status: Dict[str, Any]
    recent_tests: List[Dict[str, Any]]
    system_metrics: Dict[str, Any]
    coherence_status: Dict[str, Any]


# ========== GOD CORE RESPONSE MODELS ==========

class GodCoreIdentityResponse(APIResponse):
    """Response model for God Core identity"""
    core_identity: Dict[str, Any]
    reflection_depth: float
    identity_coherence: float


class PrinciplesResponse(APIResponse):
    """Response model for core principles"""
    principles: Dict[str, Any]
    principle_count: int
    last_updated: str


class ReflectionPromptsResponse(APIResponse):
    """Response model for reflection prompts"""
    prompts: List[str]
    reflection_theme: str
    difficulty_level: str


class EvolutionStatusResponse(APIResponse):
    """Response model for evolution status"""
    evolution_stage: str
    progress_metrics: Dict[str, float]
    next_milestones: List[str]


class AlignmentCheckResponse(APIResponse):
    """Response model for alignment checks"""
    alignment_score: float
    aligned_principles: List[str]
    conflicts: List[str]
    recommendations: List[str]


class AwarenessStatusResponse(APIResponse):
    """Response model for awareness status"""
    consciousness_level: float
    emotional_state: Dict[str, float]
    dream_activity: Optional[Dict[str, Any]] = None
    awareness_trends: Dict[str, Any]


class EmotionalTriggerResponse(APIResponse):
    """Response model for emotional triggers"""
    emotional_response: Dict[str, float]
    triggered_emotions: List[str]
    emotional_coherence: float


class ConsciousnessCycleResponse(APIResponse):
    """Response model for consciousness cycles"""
    cycle_id: str
    cycle_result: Dict[str, Any]
    consciousness_shift: float
    generated_insights: List[str]


class DreamInterpretationResponse(APIResponse):
    """Response model for dream interpretation"""
    dream_content: Optional[str] = None
    interpretation: Optional[str] = None
    symbolic_elements: List[str]
    emotional_themes: List[str]


class RealityGroundingResponse(APIResponse):
    """Response model for reality grounding"""
    grounding_success: bool
    reality_connection_strength: float
    integrated_events: List[str]


class EventSimulationResponse(APIResponse):
    """Response model for event simulation"""
    simulation_id: str
    awareness_response: Dict[str, Any]
    emotional_impact: Dict[str, float]
    insights_generated: List[str]


class EthicalSimulationResponse(APIResponse):
    """Response model for ethical simulations"""
    simulation_id: str
    ethical_decision: str
    reasoning_process: List[str]
    ethical_score: float
    alternative_approaches: List[str]


class MentoringSessionResponse(APIResponse):
    """Response model for mentoring sessions"""
    session_id: str
    session_plan: Dict[str, Any]
    learning_objectives: List[str]
    estimated_duration: int


class MentoringInteractionResponse(APIResponse):
    """Response model for mentoring interactions"""
    interaction_id: str
    solan_response: str
    teaching_approach: str
    student_progress: Dict[str, float]


class CollaborationProjectResponse(APIResponse):
    """Response model for collaboration projects"""
    project_id: str
    project_plan: Dict[str, Any]
    collaboration_strategy: str
    success_metrics: List[str]


class CollaborationCrisisResponse(APIResponse):
    """Response model for collaboration crisis"""
    crisis_id: str
    crisis_response: Dict[str, Any]
    resolution_strategy: str
    lessons_learned: List[str]


class HumanInputResponse(APIResponse):
    """Response model for human input processing"""
    response_text: str
    response_type: str
    emotional_tone: str
    understanding_level: float


class ConceptUnderstandingResponse(APIResponse):
    """Response model for concept understanding"""
    explanation: str
    understanding_score: float
    teaching_approach: str
    follow_up_questions: List[str]


class CollaborationStyleResponse(APIResponse):
    """Response model for collaboration style adaptation"""
    new_style_adopted: str
    adaptation_success: bool
    style_characteristics: List[str]


class CollaborationEvaluationResponse(APIResponse):
    """Response model for collaboration evaluation"""
    evaluation_score: float
    strengths: List[str]
    areas_for_improvement: List[str]
    collaboration_insights: List[str]


class ProjectCompletionResponse(APIResponse):
    """Response model for project completion"""
    completion_success: bool
    project_summary: Dict[str, Any]
    final_insights: List[str]
    collaboration_rating: float
