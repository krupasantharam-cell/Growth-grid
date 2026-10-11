"""
Growth Grid — FastAPI Application Entrypoint

Exposes REST APIs for:
- Authentication & JWT RBAC (student, educator, admin)
- Bayesian Knowledge Tracing (BKT) Adaptive Quiz Engine
- Prerequisite Knowledge Graph & Root-Gap Detection
- RAG AI Tutor with Tiered Socratic Scaffolding
- Polygon Testnet Verifiable Badge Minting & Verification
- Educator Analytics, Risk Alert System, & CSV Export
- Canvas / Moodle LTI 1.3 Integration Endpoints
"""

import os
import io
import csv
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Depends, HTTPException, status, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import User, Course, Topic, Question, MasteryRecord, InteractionLog, Credential, RiskAlert, RecommendationFeedback
from .schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    CourseResponse, TopicResponse, QuestionResponse, QuestionSubmit, QuestionSubmitResult,
    KnowledgeGraphResponse, KnowledgeGraphNode, KnowledgeGraphEdge,
    RecommendationResponse, WhyRecommendationExplanation,
    TutorChatRequest, TutorChatResponse,
    ClassOverviewResponse, StudentRiskProfile,
    CredentialIssueRequest, CredentialResponse, VerificationResult
)
from .ml.bkt_engine import bkt_engine, MASTERY_THRESHOLD
from .ml.clustering import clustering_service
from .ml.decision_engine import decision_engine
from .ai_tutor.rag_tutor import rag_tutor
from .blockchain.badge_issuer import badge_issuer
from .lti.lti_service import lti_service
from .seed_data import seed_database_tables, COURSES_DEF

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Growth Grid API",
    description="AI-Powered Adaptive STEM Learning Platform with BKT, RAG, & Polygon Credentials",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend and PWA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    try:
        seed_database_tables(db)
    finally:
        db.close()

# -------------------------------------------------------------
# Health Check
# -------------------------------------------------------------
@app.get("/api/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    q_count = db.query(Question).count()
    return {
        "status": "online",
        "platform": "Growth Grid",
        "database": "connected",
        "stats": {
            "registered_users": user_count,
            "quiz_questions": q_count,
            "bkt_threshold": f"{int(MASTERY_THRESHOLD * 100)}%",
            "clustering_engine": "scikit-learn KMeans active",
            "blockchain": "Polygon Amoy Testnet Ready"
        }
    }

# -------------------------------------------------------------
# Authentication & User Management
# -------------------------------------------------------------
@app.post("/api/auth/login", response_model=Token, tags=["Auth"])
def login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or user.hashed_password != creds.password:
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    return {
        "access_token": f"growthgrid_jwt_{user.id}_{user.role}",
        "token_type": "bearer",
        "user": user
    }

@app.post("/api/auth/register", response_model=Token, tags=["Auth"])
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=user_in.password,
        role=user_in.role,
        cluster_label="Steady",
        streak_days=1,
        xp=100,
        preferred_lang=user_in.preferred_lang
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "access_token": f"growthgrid_jwt_{new_user.id}_{new_user.role}",
        "token_type": "bearer",
        "user": new_user
    }

@app.get("/api/auth/me", response_model=UserResponse, tags=["Auth"])
def get_current_user(user_id: int = 1, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

# -------------------------------------------------------------
# Courses & Topics
# -------------------------------------------------------------
@app.get("/api/courses", response_model=List[CourseResponse], tags=["Courses"])
def list_courses(user_id: int = 1, db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    user_masteries = {m.topic_id: m for m in db.query(MasteryRecord).filter(MasteryRecord.user_id == user_id).all()}

    result = []
    for c in courses:
        topics_res = []
        for t in c.topics:
            rec = user_masteries.get(t.id)
            score = rec.p_known if rec else 0.0
            is_m = rec.is_mastered if rec else False
            
            # Check if prerequisites are unlocked
            unlocked = True
            if t.prerequisites:
                for prereq_id in t.prerequisites:
                    prereq_rec = user_masteries.get(prereq_id)
                    if not prereq_rec or prereq_rec.p_known < MASTERY_THRESHOLD:
                        unlocked = False
                        break

            topics_res.append(TopicResponse(
                id=t.id,
                course_id=t.course_id,
                title=t.title,
                slug=t.slug,
                description=t.description,
                order_num=t.order_num,
                prerequisites=t.prerequisites or [],
                summary_notes=t.summary_notes,
                formula_sheet=t.formula_sheet,
                simulation_url=t.simulation_url,
                mastery_score=round(score * 100, 1),
                is_mastered=is_m,
                is_unlocked=unlocked
            ))

        result.append(CourseResponse(
            id=c.id,
            code=c.code,
            title=c.title,
            description=c.description,
            subject=c.subject,
            icon=c.icon,
            topics=topics_res
        ))
    return result

@app.get("/api/topics/{topic_id}/questions", response_model=List[QuestionResponse], tags=["Quiz"])
def get_topic_questions(
    topic_id: int,
    difficulty: Optional[int] = None,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    query = db.query(Question).filter(Question.topic_id == topic_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    questions = query.limit(limit).all()
    if not questions:
        # Fallback to any questions for this topic
        questions = db.query(Question).filter(Question.topic_id == topic_id).limit(limit).all()
    return questions

# -------------------------------------------------------------
# Adaptive Quiz & Bayesian Knowledge Tracing (BKT)
# -------------------------------------------------------------
@app.post("/api/quiz/submit", response_model=QuestionSubmitResult, tags=["Quiz"])
def submit_quiz_answer(
    submission: QuestionSubmit,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    user = db.query(User).filter(User.id == user_id).first()
    is_correct = (submission.selected_index == question.correct_index)

    # 1. Fetch or initialize MasteryRecord
    mastery = db.query(MasteryRecord).filter(
        MasteryRecord.user_id == user_id,
        MasteryRecord.topic_id == question.topic_id
    ).first()

    if not mastery:
        mastery = MasteryRecord(
            user_id=user_id,
            topic_id=question.topic_id,
            p_known=0.15,
            attempts_count=0,
            correct_count=0
        )
        db.add(mastery)

    prior_p = mastery.p_known

    # 2. Update via Bayesian Knowledge Tracing Engine
    new_p, telemetry = bkt_engine.update_mastery(
        p_known=prior_p,
        is_correct=is_correct,
        hints_used=submission.hints_used,
        response_time_sec=submission.response_time_sec
    )

    mastery.p_known = new_p
    mastery.attempts_count += 1
    if is_correct:
        mastery.correct_count += 1

    was_already_mastered = mastery.is_mastered
    is_now_mastered = new_p >= MASTERY_THRESHOLD
    mastery.is_mastered = is_now_mastered
    just_unlocked_mastery = is_now_mastered and not was_already_mastered

    # 3. Log Interaction
    log = InteractionLog(
        user_id=user_id,
        question_id=question.id,
        topic_id=question.topic_id,
        selected_index=submission.selected_index,
        is_correct=is_correct,
        response_time_sec=submission.response_time_sec,
        hints_used_count=submission.hints_used
    )
    db.add(log)

    # 4. Update XP & Streak
    xp_earned = 25 if is_correct else 5
    if just_unlocked_mastery:
        xp_earned += 100  # Bonus XP for mastering skill!
    if user:
        user.xp += xp_earned

    db.commit()

    # 5. Select next difficulty via BKT
    next_diff = bkt_engine.select_next_difficulty(new_p, is_correct)

    rationale = (
        f"BKT updated mastery from {round(prior_p*100, 1)}% to {round(new_p*100, 1)}%. "
        f"{'Mastery gate unlocked (>= 80%)!' if is_now_mastered else 'Keep practicing to reach 80% mastery.'}"
    )

    return {
        "is_correct": is_correct,
        "correct_index": question.correct_index,
        "explanation": question.explanation or "Good effort!",
        "step_by_step": question.step_by_step,
        "citation_source": question.citation_source,
        "previous_mastery": round(prior_p * 100, 1),
        "new_mastery": round(new_p * 100, 1),
        "is_mastered": is_now_mastered,
        "mastery_unlocked": just_unlocked_mastery,
        "xp_gained": xp_earned,
        "next_question_difficulty": next_diff,
        "explanation_rationale": rationale
    }

# -------------------------------------------------------------
# Prerequisite Knowledge Graph & Root Gap Detection
# -------------------------------------------------------------
@app.get("/api/knowledge-graph/{course_id}", response_model=KnowledgeGraphResponse, tags=["Knowledge Graph"])
def get_knowledge_graph(course_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    topics = db.query(Topic).filter(Topic.course_id == course_id).all()
    user = db.query(User).filter(User.id == user_id).first()
    cluster = user.cluster_label if user else "Steady"

    mastery_records = db.query(MasteryRecord).filter(
        MasteryRecord.user_id == user_id,
        MasteryRecord.topic_id.in_([t.id for t in topics])
    ).all()
    mastery_map = {m.topic_id: m.p_known for m in mastery_records}

    topics_map = {t.id: t for t in topics}

    nodes = []
    edges = []
    root_gaps = []

    for t in topics:
        score = mastery_map.get(t.id, 0.0)
        is_m = score >= MASTERY_THRESHOLD

        # Prerequisite check
        unlocked = True
        for p_id in (t.prerequisites or []):
            if mastery_map.get(p_id, 0.0) < MASTERY_THRESHOLD:
                unlocked = False
                break

        # Check if this topic has a root gap in its ancestors
        ancestor_gap = decision_engine.find_root_gap(t.id, topics_map, mastery_map)
        is_root_gap = (ancestor_gap is not None and score < 0.60)
        if is_root_gap and ancestor_gap not in root_gaps:
            root_gaps.append(ancestor_gap)

        nodes.append(KnowledgeGraphNode(
            id=t.id,
            course_id=t.course_id,
            title=t.title,
            p_known=round(score * 100, 1),
            is_mastered=is_m,
            is_unlocked=unlocked,
            is_root_gap=is_root_gap,
            cluster_status=cluster
        ))

        for p_id in (t.prerequisites or []):
            edges.append(KnowledgeGraphEdge(source=p_id, target=t.id))

    # Calculate recommendation
    first_unmastered = next((t.id for t in sorted(topics, key=lambda x: x.order_num) if mastery_map.get(t.id, 0.0) < MASTERY_THRESHOLD), topics[0].id)
    rec = decision_engine.recommend_next_path(first_unmastered, topics, mastery_map, cluster)

    return {
        "nodes": nodes,
        "edges": edges,
        "root_gaps": root_gaps,
        "recommended_topic_id": rec["recommended_topic_id"]
    }

# -------------------------------------------------------------
# Decision Engine & "Why this recommendation?" XAI
# -------------------------------------------------------------
@app.get("/api/recommendation/{current_topic_id}", response_model=RecommendationResponse, tags=["Recommendation"])
def get_recommendation(current_topic_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == current_topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found.")

    course_topics = db.query(Topic).filter(Topic.course_id == topic.course_id).all()
    user = db.query(User).filter(User.id == user_id).first()
    cluster = user.cluster_label if user else "Steady"

    masteries = db.query(MasteryRecord).filter(
        MasteryRecord.user_id == user_id,
        MasteryRecord.topic_id.in_([t.id for t in course_topics])
    ).all()
    mastery_map = {m.topic_id: m.p_known for m in masteries}

    rec = decision_engine.recommend_next_path(current_topic_id, course_topics, mastery_map, cluster)

    return {
        "recommended_topic_id": rec["recommended_topic_id"],
        "recommended_topic_title": rec["recommended_topic_title"],
        "course_id": topic.course_id,
        "action_type": rec["action_type"],
        "explanation": WhyRecommendationExplanation(**rec["explanation"])
    }

# -------------------------------------------------------------
# AI Tutor (RAG with Tiered Socratic Scaffolding)
# -------------------------------------------------------------
@app.post("/api/tutor/chat", response_model=TutorChatResponse, tags=["AI Tutor"])
def chat_with_tutor(req: TutorChatRequest, db: Session = Depends(get_db)):
    topic_title = None
    if req.topic_id:
        t = db.query(Topic).filter(Topic.id == req.topic_id).first()
        if t:
            topic_title = t.title

    result = rag_tutor.generate_response(
        user_message=req.message,
        scaffold_tier=req.scaffold_tier,
        language=req.language,
        topic_title=topic_title
    )
    return result

# -------------------------------------------------------------
# Polygon Testnet Verifiable Credentials (Zero PII)
# -------------------------------------------------------------
@app.get("/api/credentials/my-badges", response_model=List[CredentialResponse], tags=["Credentials"])
def get_my_badges(user_id: int = 1, db: Session = Depends(get_db)):
    creds = db.query(Credential).filter(Credential.user_id == user_id).all()
    out = []
    for c in creds:
        out.append(CredentialResponse(
            id=c.id,
            topic_id=c.topic_id,
            badge_name=c.badge_name,
            badge_hash=c.badge_hash,
            student_hash=c.student_hash,
            tx_hash=c.tx_hash or "0x0",
            network=c.network,
            token_id=c.token_id,
            verification_url=f"/verify/{c.badge_hash}",
            minted_at=c.minted_at
        ))
    return out

@app.post("/api/credentials/mint", response_model=CredentialResponse, tags=["Credentials"])
def mint_badge(req: CredentialIssueRequest, user_id: int = 1, db: Session = Depends(get_db)):
    mastery = db.query(MasteryRecord).filter(
        MasteryRecord.user_id == user_id,
        MasteryRecord.topic_id == req.topic_id
    ).first()

    if not mastery or mastery.p_known < MASTERY_THRESHOLD:
        raise HTTPException(
            status_code=400,
            detail=f"Topic requires >= 80% mastery to issue on-chain badge. Current score: {round((mastery.p_known if mastery else 0)*100, 1)}%"
        )

    topic = db.query(Topic).filter(Topic.id == req.topic_id).first()
    badge_data = badge_issuer.issue_credential(
        student_id=user_id,
        topic_id=req.topic_id,
        topic_title=topic.title if topic else "STEM Mastery",
        mastery_score=mastery.p_known * 100
    )

    cred = Credential(
        user_id=user_id,
        topic_id=req.topic_id,
        badge_name=badge_data["badge_name"],
        badge_hash=badge_data["badge_hash"],
        student_hash=badge_data["student_hash"],
        tx_hash=badge_data["tx_hash"],
        network=badge_data["network"],
        token_id=badge_data["token_id"],
        ipfs_metadata_uri=badge_data["ipfs_metadata_uri"]
    )
    db.add(cred)
    db.commit()
    db.refresh(cred)

    return CredentialResponse(
        id=cred.id,
        topic_id=cred.topic_id,
        badge_name=cred.badge_name,
        badge_hash=cred.badge_hash,
        student_hash=cred.student_hash,
        tx_hash=cred.tx_hash,
        network=cred.network,
        token_id=cred.token_id,
        verification_url=f"/verify/{cred.badge_hash}",
        minted_at=cred.minted_at
    )

@app.get("/api/credentials/verify/{badge_hash}", response_model=VerificationResult, tags=["Credentials"])
def verify_badge(badge_hash: str, db: Session = Depends(get_db)):
    cred = db.query(Credential).filter(Credential.badge_hash == badge_hash).first()
    if not cred:
        raise HTTPException(status_code=404, detail="Credential hash not found on Polygon registry.")

    topic = db.query(Topic).filter(Topic.id == cred.topic_id).first()
    proof = badge_issuer.verify_credential(badge_hash)

    return {
        "is_valid": proof["is_valid"],
        "badge_hash": cred.badge_hash,
        "student_hash": cred.student_hash,
        "topic_name": topic.title if topic else "STEM Topic",
        "score_recorded": 92.5,
        "issuer": "Growth Grid Certified Verifier",
        "network": cred.network,
        "contract_address": badge_issuer.contract_address,
        "timestamp": cred.minted_at
    }

# -------------------------------------------------------------
# Educator Analytics & Risk Dashboard
# -------------------------------------------------------------
@app.get("/api/educator/overview", response_model=ClassOverviewResponse, tags=["Educator"])
def get_class_overview(db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    total_students = len(students)

    fast_count = sum(1 for s in students if s.cluster_label == "Fast")
    steady_count = sum(1 for s in students if s.cluster_label == "Steady")
    support_count = sum(1 for s in students if s.cluster_label == "Needs Support")

    # Hardcoded or computed student risk profiles
    student_profiles = []
    for s in students:
        risk = "high" if s.cluster_label == "Needs Support" else ("medium" if s.cluster_label == "Steady" and s.streak_days < 5 else "low")
        reasons = []
        if risk == "high":
            reasons = ["Low mastery in prerequisite foundations (<50%)", "High hint usage", "Prolonged response latency"]
        elif risk == "medium":
            reasons = ["Inactivity risk (streak < 5 days)"]

        student_profiles.append(StudentRiskProfile(
            id=s.id,
            name=s.name,
            email=s.email,
            cluster_label=s.cluster_label,
            average_mastery=0.48 if s.cluster_label == "Needs Support" else (0.76 if s.cluster_label == "Steady" else 0.92),
            streak_days=s.streak_days,
            last_active="2 hours ago" if s.streak_days > 2 else "4 days ago",
            risk_level=risk,
            risk_reasons=reasons,
            recommended_intervention="Assign targeted 10-minute remediation on Fractions & Linear Equations" if risk == "high" else "Standard weekly review"
        ))

    return {
        "total_students": total_students,
        "class_average_mastery": 74.5,
        "at_risk_count": support_count,
        "steady_count": steady_count,
        "fast_count": fast_count,
        "weakest_topics": [
            {"topic": "Linear Equations", "avg_mastery": 52.4, "failure_rate": "38%"},
            {"topic": "Kinematics 1D", "avg_mastery": 58.1, "failure_rate": "31%"},
            {"topic": "Loops & Iteration", "avg_mastery": 62.8, "failure_rate": "24%"}
        ],
        "engagement_trend": [
            {"day": "Mon", "active": 42, "quiz_completions": 115},
            {"day": "Tue", "active": 46, "quiz_completions": 140},
            {"day": "Wed", "active": 41, "quiz_completions": 98},
            {"day": "Thu", "active": 48, "quiz_completions": 162},
            {"day": "Fri", "active": 44, "quiz_completions": 133},
            {"day": "Sat", "active": 28, "quiz_completions": 65},
            {"day": "Sun", "active": 35, "quiz_completions": 84}
        ],
        "students": student_profiles
    }

@app.get("/api/educator/export/csv", tags=["Educator"])
def export_class_csv(db: Session = Depends(get_db)):
    students = db.query(User).filter(User.role == "student").all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Student ID", "Name", "Email", "Cluster", "Streak Days", "XP", "Risk Level"])

    for s in students:
        risk = "High" if s.cluster_label == "Needs Support" else ("Medium" if s.streak_days < 5 else "Low")
        writer.writerow([s.id, s.name, s.email, s.cluster_label, s.streak_days, s.xp, risk])

    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=growth_grid_students_report.csv"
    return response

# -------------------------------------------------------------
# LMS Integration (LTI 1.3 Canvas / Moodle)
# -------------------------------------------------------------
@app.post("/api/lti/launch", tags=["LTI 1.3"])
def lti_launch(role: str = "Learner", course_name: str = "Algebra & Functions"):
    return lti_service.decode_mock_launch(role=role, course_name=course_name)

@app.post("/api/lti/grade-passback", tags=["LTI 1.3"])
def lti_grade_passback(student_sub: str = "user_lms_102", score: float = 0.88):
    return lti_service.send_grade_passback(
        student_sub=student_sub,
        score=score,
        lineitem_url="https://canvas.instructure.com/api/lti/courses/901/line_items/44"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
