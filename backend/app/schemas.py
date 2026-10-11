import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr

# Auth & User
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "student"
    preferred_lang: str = "en"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    cluster_label: str
    streak_days: int
    xp: int
    consent_given: bool
    low_bandwidth_mode: bool
    high_contrast_mode: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# Courses & Topics
class TopicBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    order_num: int = 1
    prerequisites: List[int] = []
    summary_notes: Optional[str] = None
    formula_sheet: Optional[str] = None
    simulation_url: Optional[str] = None

class TopicResponse(TopicBase):
    id: int
    course_id: int
    mastery_score: Optional[float] = 0.0
    is_mastered: Optional[bool] = False
    is_unlocked: Optional[bool] = True

    class Config:
        from_attributes = True

class CourseResponse(BaseModel):
    id: int
    code: str
    title: str
    description: Optional[str] = None
    subject: str
    icon: str
    topics: List[TopicResponse] = []

    class Config:
        from_attributes = True

# Questions
class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    difficulty: int
    question_text: str
    options: List[str]
    # correct_index is kept secret during quiz!
    hint_1: Optional[str] = None
    hint_2: Optional[str] = None
    citation_source: Optional[str] = None

    class Config:
        from_attributes = True

class QuestionSubmit(BaseModel):
    question_id: int
    selected_index: int
    response_time_sec: float
    hints_used: int = 0

class QuestionSubmitResult(BaseModel):
    is_correct: bool
    correct_index: int
    explanation: str
    step_by_step: Optional[str]
    citation_source: Optional[str]
    previous_mastery: float
    new_mastery: float
    is_mastered: bool
    mastery_unlocked: bool
    xp_gained: int
    next_question_difficulty: int
    explanation_rationale: str

# Mastery & BKT
class MasteryRecordResponse(BaseModel):
    topic_id: int
    topic_title: str
    p_known: float
    is_mastered: bool
    attempts_count: int
    correct_count: int
    last_updated: datetime.datetime

# Prerequisite Knowledge Graph
class KnowledgeGraphNode(BaseModel):
    id: int
    course_id: int
    title: str
    p_known: float
    is_mastered: bool
    is_unlocked: bool
    is_root_gap: bool
    cluster_status: str

class KnowledgeGraphEdge(BaseModel):
    source: int
    target: int
    label: str = "prerequisite"

class KnowledgeGraphResponse(BaseModel):
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]
    root_gaps: List[int]
    recommended_topic_id: Optional[int]

# Recommendation & XAI
class WhyRecommendationExplanation(BaseModel):
    topic_title: str
    reason: str
    bkt_mastery_percent: float
    prerequisite_status: str
    learner_cluster: str
    suggested_action: str

class RecommendationResponse(BaseModel):
    recommended_topic_id: int
    recommended_topic_title: str
    course_id: int
    action_type: str  # 'continue', 'remediation', 'challenge'
    explanation: WhyRecommendationExplanation

# AI Tutor RAG
class TutorChatRequest(BaseModel):
    message: str
    topic_id: Optional[int] = None
    question_id: Optional[int] = None
    scaffold_tier: int = 1  # 1: Socratic hint, 2: Step-by-step guidance, 3: Full solution
    language: str = "en"

class TutorChatResponse(BaseModel):
    reply: str
    scaffold_tier: int
    course_citation: Optional[str]
    suggested_followups: List[str]
    detected_concept: Optional[str]

# Educator Analytics
class StudentRiskProfile(BaseModel):
    id: int
    name: str
    email: str
    cluster_label: str
    average_mastery: float
    streak_days: int
    last_active: str
    risk_level: str  # 'high', 'medium', 'low'
    risk_reasons: List[str]
    recommended_intervention: str

class ClassOverviewResponse(BaseModel):
    total_students: int
    class_average_mastery: float
    at_risk_count: int
    steady_count: int
    fast_count: int
    weakest_topics: List[Dict[str, Any]]
    engagement_trend: List[Dict[str, Any]]
    students: List[StudentRiskProfile]

# Blockchain Credentials
class CredentialIssueRequest(BaseModel):
    topic_id: int

class CredentialResponse(BaseModel):
    id: int
    topic_id: int
    badge_name: str
    badge_hash: str
    student_hash: str
    tx_hash: str
    network: str
    token_id: int
    verification_url: str
    minted_at: datetime.datetime

    class Config:
        from_attributes = True

class VerificationResult(BaseModel):
    is_valid: bool
    badge_hash: str
    student_hash: str
    topic_name: str
    score_recorded: float
    issuer: str
    network: str
    contract_address: str
    timestamp: datetime.datetime
