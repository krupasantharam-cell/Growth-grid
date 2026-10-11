# 🎬 Growth Grid — Comprehensive Demo Script & Presentation Guide

This guide walks you step-by-step through presenting and evaluating the Growth Grid platform.

---

## ⏱️ Demo Outline (10-Minute Walkthrough)

### Phase 1: Login Page First & Authentication Gate (Minutes 0–2)
1. **Open the Application**: Open `preview.html` in your web browser.
2. **Notice the Login Page First**:
   - The platform greets the user with the dedicated **Sign In / Registration Screen**.
   - Input your **Mail ID** (e.g. `student@growthgrid.org`) and **Password** (`password123`), or click the **1-Click Demo Accounts** (`🎓 Student (Alex)`, `👩‍🏫 Educator (Dr. Vance)`, `⚙️ Admin (LMS)`).
   - Click **"Sign In & Start Learning →"**. The system validates credentials and launches the application!
3. **Review the Authenticated Student Dashboard**:
   - Notice the user's name (`Alex Student`) and role pill displayed in the top navigation bar, with a prominent **Sign Out** button.
   - Point out the **Streak Counter (🔥 5 Days)** and **XP Score (420 XP)**.
   - Show the **Topic Mastery Heatmap** across Algebra, Physics, and Coding.
   - Notice the **P(L) percentage scores**:
     - *Fractions & Decimals* is at **88%** (Mastered ✅).
     - *Linear Equations* is at **58%** (In Progress ⏳).
     - *Systems of Equations* is locked (🔒 Requires 80% on Linear Equations).

### Phase 2: Transparent Recommendation & "Why this recommendation?" (Minutes 2–3)
1. Look at the **Next Recommended Lesson** hero card suggesting *Linear Equations*.
2. Click **"💡 Why this recommendation?"**:
   - Highlight the **Bayesian Knowledge Tracing score** (58% vs. 80% Mastery Gate).
   - Show the **Prerequisite check**: Fractions (88%) is satisfied, so no prior remediation is required.
   - Point out the **K-Means Pacing Profile**: Student is clustered as a *Steady Learner*, so the engine delivers balanced difficulty (Level 2–3).

### Phase 3: Adaptive Quiz & Real-Time Bayesian Knowledge Tracing (Minutes 3–5)
1. Click **"Start Adaptive Quiz"** (or switch to the "Adaptive Quiz" tab):
   - Notice the **Live BKT Probability Gauge**: updates after every question.
   - Point out the **Key Formula & PhET Simulation link** for multi-modal learning.
   - Explore **Tiered Pedagogical Scaffolding**:
     - Click **"💡 Hint 1 (Concept)"** — gives a conceptual nudge without giving away the answer.
     - Click **"🔍 Hint 2 (Formula)"** — gives deeper formula assistance.
     - Select an answer option and click **"Submit Answer"**.
   - Review the **Instant Feedback Panel**:
     - Displays mathematical step-by-step derivation.
     - Official textbook course citation (`Growth Grid Algebra Vol 1, §2.2`).
     - Real-time BKT probability delta ($P(L)$ jumps from $58\% \rightarrow 71\%$).
     - Audio Reader (`🔊 Read Aloud`) powered by Web Speech API.
2. When mastery reaches $\ge 80\%$, observe the **Mastery Gate Celebration Modal**:
   - Awards bonus $+100$ XP.
   - Unlocks the next syllabus topic (*Systems of Equations*).
   - Prompts the student to mint their verifiable Polygon credential.

### Phase 4: Prerequisite Knowledge Graph & Root-Gap Detection (Minutes 5–6)
1. Switch to the **"🕸️ Knowledge Graph"** tab:
   - Examine the interactive Directed Acyclic Graph (DAG) with dependency arrows.
   - Explain how Growth Grid detects **Root Skill Gaps**:
     - If a student fails on *Quadratic Equations*, traditional LMSs just repeat quadratics.
     - Growth Grid's DAG traversal pinpoints that the true root gap is in *Fractions & Decimals* or *Linear Equations*, directing the learner to foundational remediation.

### Phase 5: AI Tutor with RAG & Multilingual Accessibility (Minutes 6–7)
1. Switch to the **"🤖 AI Tutor"** tab:
   - Notice the 3 scaffolding tier buttons: **Hint First**, **Step-by-Step**, and **Full Solution**.
   - Click one of the quick prompt chips (e.g. *"How do I solve 3x - 5 = 16?"*).
   - Show how the AI tutor gives guiding questions first instead of cheating.
   - Toggle language to **Tamil (தமிழ்)** or **Hindi (हिन्दी)** to demonstrate accessibility.
   - Click **"🔊 Read Aloud"** to hear the spoken explanation.

### Phase 6: Verifiable Polygon Testnet Badges (Zero PII) (Minutes 7–8)
1. Switch to the **"🏅 On-Chain Badges"** tab:
   - View the soulbound mastery badge for *Fractions & Rational Numbers*.
   - Point out the **dynamic QR code** for instant third-party verification.
   - Inspect the cryptographic proof: **SHA-256 Badge Hash**, **Transaction Hash**, and **Polygon Amoy Testnet** network details.
   - **Privacy Guarantee**: Emphasize that zero personal names or emails are stored on-chain.

### Phase 7: Educator Analytics & At-Risk Roster (Minutes 8–10)
1. Switch the role dropdown to **"Role: Educator (Dr. Vance)"**:
   - Point out the **Class Overview metrics**: 50 students, 74.5% class average mastery, 13 at-risk learners.
   - Review the **Weak Area Heatmap**: identifies topics with high failure rates (*Linear Equations* at 38% failure rate).
   - View the **50-Student Roster**:
     - Color-coded risk badges (🔴 High Risk, 🟡 Moderate, 🟢 Low Risk).
     - K-Means clusters (Fast, Steady, Needs Support).
     - Automated Root Gap indicator for struggling students.
   - Click **"View Interventions ↗"** on an at-risk student:
     - Displays individualized root-cause analysis and actionable teacher intervention recommendations.
   - Click **"📥 Export CSV"** to demonstrate instant gradebook/analytics export.
2. Switch role to **"Role: Admin (LMS)"**:
   - Demonstrate the **LTI 1.3 Canvas / Moodle OIDC launch** and **Assignment & Grade Service (AGS)** passback tester.

---

## 🏆 Key Talking Points for Evaluators
- **Pedagogical Integrity**: Unlike raw LLMs that simply blurt out quiz answers, Growth Grid uses Socratic scaffolding (hints first, citations required).
- **Mathematical Rigor**: Bayesian Knowledge Tracing calculates true posterior skill mastery rather than simple percentage averages.
- **Root-Cause Discovery**: The prerequisite DAG traces learning bottlenecks back to their origin.
- **Web3 with True Privacy**: Verifiable credentials without GDPR / COPPA privacy violations (cryptographic hashes only).
