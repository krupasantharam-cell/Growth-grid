# Growth Grid — AI-Powered Adaptive Learning Platform

Growth Grid is a full-stack, responsive, PWA-enabled adaptive STEM learning platform that detects skill gaps and personalizes learning paths in real time using Bayesian Knowledge Tracing (BKT), K-Means learner clustering, RAG-powered AI tutoring, and Polygon blockchain verifiable credentials.

---

## 🌟 Key Features

### 🎓 1. Student Experience
- **Smart Onboarding & Diagnostic Quiz**: Select subjects (Algebra, Physics Basics, Coding Basics) and determine baseline mastery.
- **Adaptive Learning & Mastery Gates**: Difficulty dynamically shifts after every answer based on real-time BKT updates. Requires $\ge 80\%$ mastery to unlock advanced topics; triggers automated root-gap remediation if below.
- **Prerequisite Knowledge Graph**: Interactive DAG visualization highlighting exact root knowledge gaps (e.g., Fractions gap impeding Linear Equations).
- **RAG AI Tutor**: Pedagogically scaffolded (Hint 1 -> Hint 2 -> Step-by-Step -> Full Solution on request) with exact course citations.
- **Transparent XAI ("Why this recommendation?")**: Explains the exact BKT score, prerequisite DAG status, and cluster learning pace behind each suggestion.
- **Verifiable Polygon Credentials**: Soulbound badges with cryptographic SHA-256 hashes verified on-chain without exposing personal data. Includes QR code and verification page.

### 👩‍🏫 2. Educator Analytics
- **Class Mastery Overview & Topic Heatmaps**: Real-time average mastery and weakest topic identification.
- **Risk Detection Engine**: Auto-flags students with low mastery, long inactivity, or repetitive error patterns.
- **Student Timeline & Interventions**: Deep-dive into individual BKT mastery curves, interaction history, and recommended teacher interventions.
- **Content Studio**: Create, tag, and publish questions with tiered hints and difficulty ratings.
- **One-Click Export**: Export comprehensive student reports to CSV and printable format.

### ⚙️ 3. Admin & Integrations
- **LTI 1.3 LMS Integration**: Canvas / Moodle compliant launch endpoints, grade passback, and deep linking simulation.
- **Course & Knowledge Graph Management**: Configure DAG dependencies and prerequisite edges.
- **Inclusive Accessibility & Privacy**:
  - Multilingual support: English, Tamil (தமிழ்), Hindi (हिन्दी).
  - Web Speech API Text-to-Speech audio reader.
  - High-Contrast and Low-Bandwidth modes.
  - Privacy consent screen and zero personal data on-chain.

---

## 🚀 Quick Start

### Option A: Instant Browser Preview (Zero Setup Needed!)
You can open `preview.html` directly in any web browser:
```bash
# Simply double-click preview.html or open it in your browser:
# C:\Users\SAI KRUPA\.gemini\antigravity\scratch\growth-grid\preview.html
```
This contains the entire responsive React application, full interactive BKT engine, RAG AI tutor, Prerequisite DAG graph, 500+ question seed pool, multi-language engine, and educator dashboard running out of the box!

### Option B: Running the Python FastAPI Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```
The API and Swagger docs will be live at `http://localhost:8000/docs`.

### Option C: Running the React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to access the application.

---

## 🏗️ Architecture

```
growth-grid/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI server & route registration
│   │   ├── database.py          # SQLAlchemy PostgreSQL engine with SQLite fallback
│   │   ├── models.py            # ORM models (Users, Courses, Questions, Mastery, Logs, Badges)
│   │   ├── schemas.py           # Pydantic validation schemas
│   │   ├── ml/
│   │   │   ├── bkt_engine.py    # Bayesian Knowledge Tracing implementation
│   │   │   ├── clustering.py    # K-Means learner clustering (Fast/Steady/Support)
│   │   │   └── decision_engine.py # DAG knowledge graph gap detection & recommendation engine
│   │   ├── ai_tutor/
│   │   │   └── rag_tutor.py     # RAG AI tutor with tiered hints and citations
│   │   ├── blockchain/
│   │   │   └── badge_issuer.py  # Polygon testnet credential generator & verifier
│   │   ├── lti/
│   │   │   └── lti_service.py   # LTI 1.3 Canvas/Moodle integration service
│   │   └── seed_data.py         # 3 courses, 50 students, 500+ tagged STEM questions
│   └── requirements.txt
├── contracts/
│   └── GrowthGridBadges.sol     # Polygon ERC721 verifiable credential smart contract
├── frontend/
│   ├── public/
│   │   ├── manifest.json        # PWA configuration
│   │   └── sw.js                # Service Worker for offline lesson caching
│   ├── src/
│   │   ├── App.jsx              # Main React SPA routing and state
│   │   ├── components/          # Student, Educator, Admin, Tutor, Graph, Credentials
│   │   └── index.css            # Soft blue palette Tailwind CSS
│   └── package.json
├── docs/
│   ├── DEMO_SCRIPT.md           # Step-by-step walkthrough demo script
│   └── API_SPEC.md              # REST API reference specification
└── preview.html                 # Standalone, interactive, zero-dependency browser preview
```
