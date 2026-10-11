# Growth Grid — REST API Specification

FastAPI Interactive Swagger documentation is available at `/docs` (and ReDoc at `/redoc`).

---

## 🔐 1. Authentication & RBAC

### `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "student@growthgrid.org",
    "password": "password123"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "access_token": "growthgrid_jwt_1_student",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "Alex Student",
      "email": "student@growthgrid.org",
      "role": "student",
      "cluster_label": "Steady",
      "streak_days": 5,
      "xp": 420
    }
  }
  ```

---

## 📚 2. Courses & Adaptive Quizzes

### `GET /api/courses`
Returns all 3 courses with topics, prerequisites, and learner mastery scores.

### `GET /api/topics/{topic_id}/questions?difficulty=2&limit=5`
Retrieves adaptive questions for the specified topic.

### `POST /api/quiz/submit`
Submits question attempt and runs Bayesian Knowledge Tracing.
- **Request Body**:
  ```json
  {
    "question_id": 202,
    "selected_index": 0,
    "response_time_sec": 14.5,
    "hints_used": 1
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "is_correct": true,
    "correct_index": 0,
    "explanation": "Adding 5 gives 3x = 21, and dividing by 3 results in x = 7.",
    "step_by_step": "1) Add 5: 3x = 21. 2) Divide by 3: x = 7.",
    "citation_source": "Growth Grid Algebra Vol 1, §2.2",
    "previous_mastery": 58.0,
    "new_mastery": 71.4,
    "is_mastered": false,
    "mastery_unlocked": false,
    "xp_gained": 25,
    "next_question_difficulty": 3,
    "explanation_rationale": "BKT updated mastery from 58.0% to 71.4%."
  }
  ```

---

## 🕸️ 3. Knowledge Graph & Recommendation (XAI)

### `GET /api/knowledge-graph/{course_id}`
Returns DAG nodes, prerequisite edges, detected root knowledge gaps, and next recommended topic.

### `GET /api/recommendation/{current_topic_id}`
Returns transparent "Why this recommendation?" XAI explanation:
- BKT score vs. 80% Mastery Gate
- Ancestor prerequisite check status
- Learner cluster pacing rationale

---

## 🤖 4. AI Tutor (RAG)

### `POST /api/tutor/chat`
- **Request Body**:
  ```json
  {
    "message": "How do I solve 3x - 5 = 16?",
    "topic_id": 2,
    "scaffold_tier": 1,
    "language": "en"
  }
  ```
- **Response** (`200 OK`):
  ```json
  {
    "reply": "💡 Concept Hint: Think about maintaining equality balance...",
    "scaffold_tier": 1,
    "course_citation": null,
    "suggested_followups": ["Give me a step-by-step breakdown", "Show me the full solution"]
  }
  ```

---

## ⛓️ 5. Polygon Blockchain Credentials

### `POST /api/credentials/mint`
Mints on-chain verifiable badge if mastery $\ge 80\%$.
- Stores SHA-256 hash only (Zero PII).

### `GET /api/credentials/verify/{badge_hash}`
Public verification endpoint returning contract address, timestamp, issuer, and score.

---

## 👩‍🏫 6. Educator Analytics

### `GET /api/educator/overview`
Returns class average mastery, weak topics, risk distribution, and 50-student roster.

### `GET /api/educator/export/csv`
Downloads complete student roster with risk flags as CSV.

---

## 🏫 7. LMS Integration (LTI 1.3)

### `POST /api/lti/launch`
Simulates Canvas / Moodle OIDC launch and role token.

### `POST /api/lti/grade-passback`
Pushes normalized score ($0.0 - 1.0$) to LMS Assignment & Grade Service lineitem endpoint.
