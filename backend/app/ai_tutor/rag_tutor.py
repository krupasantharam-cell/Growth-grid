"""
RAG-Powered AI STEM Tutor with Tiered Socratic Scaffolding

Features:
- Knowledge retrieval across Algebra, Physics, and Coding course corpora
- Pedagogical scaffolding:
  - Tier 1: Socratic hint / concept nudge (never reveals direct answers first)
  - Tier 2: Step-by-step methodology breakdown
  - Tier 3: Complete derivation/solution with exact course manual citation
- Multilingual responses: English, Tamil (தமிழ்), Hindi (हिन्दी)
"""

import os
from typing import Dict, Any, List, Optional

# Course corpus for RAG semantic search & citation lookup
STEM_KNOWLEDGE_CORPUS = {
    "fractions": {
        "title": "Fractions & Proportions",
        "citation": "Growth Grid Algebra Vol. 1, §1.4 (Rational Arithmetic)",
        "summary": "To add or subtract fractions, identify the Least Common Denominator (LCD). For multiplication, multiply numerators and denominators directly. For division, multiply by the reciprocal.",
        "common_errors": "Adding denominators directly without finding common denominator (e.g., 1/2 + 1/3 != 2/5).",
        "guidance": "Step 1: Check denominators. Step 2: Convert to equivalent fractions with LCD. Step 3: Combine numerators."
    },
    "linear_equations": {
        "title": "Linear Equations & Inequalities",
        "citation": "Growth Grid Algebra Vol. 1, §2.2 (Single-Variable Equations)",
        "summary": "Standard form: ax + b = c. The Golden Rule of Algebra states that whatever operation is performed on one side must be performed on the other. Isolate the variable term first, then divide by coefficient.",
        "common_errors": "Sign flip omission when distributing negative terms or dividing inequalities by negative numbers.",
        "guidance": "Step 1: Distribute parentheses. Step 2: Group like variable terms on one side. Step 3: Group constants on the opposite side. Step 4: Divide by variable coefficient."
    },
    "quadratic_equations": {
        "title": "Quadratic Equations",
        "citation": "Growth Grid Algebra Vol. 1, §4.1 (Second-Degree Polynomials)",
        "summary": "General form: ax^2 + bx + c = 0. Roots are given by the Quadratic Formula: x = (-b ± √(b^2 - 4ac)) / (2a). The discriminant Δ = b^2 - 4ac determines nature of roots: Δ > 0 (two real roots), Δ = 0 (one repeated root), Δ < 0 (complex roots).",
        "common_errors": "Forgetting the denominator 2a applies to the entire numerator (-b ± √Δ), or miscalculating -4ac when c is negative.",
        "guidance": "Step 1: Write in standard form ax^2 + bx + c = 0. Step 2: Identify a, b, c. Step 3: Compute discriminant b^2 - 4ac. Step 4: Substitute into quadratic formula."
    },
    "vectors": {
        "title": "Vectors and Scalars",
        "citation": "Growth Grid Physics Basics, §1.2 (Vector Algebra)",
        "summary": "Scalars have magnitude only (mass, temperature, speed). Vectors have both magnitude and direction (displacement, velocity, force). Vector components: Vx = V * cos(θ), Vy = V * sin(θ).",
        "common_errors": "Treating vectors like scalar numbers without resolving orthogonal components.",
        "guidance": "Step 1: Establish coordinate axes (x and y). Step 2: Resolve vectors into components using trigonometry. Step 3: Sum x-components and y-components independently."
    },
    "kinematics": {
        "title": "1D Kinematics & Motion",
        "citation": "Growth Grid Physics Basics, §2.3 (Uniform Acceleration Equations)",
        "summary": "The 3 kinematic equations for constant acceleration: 1) v = u + at, 2) s = ut + 0.5*a*t^2, 3) v^2 = u^2 + 2as, where u=initial velocity, v=final velocity, a=acceleration, s=displacement, t=time.",
        "common_errors": "Confusing displacement with total distance, or omitting negative sign for gravitational deceleration (a = -9.8 m/s^2).",
        "guidance": "Step 1: List known variables (u, v, a, s, t). Step 2: Identify the single unknown. Step 3: Pick the equation that contains only knowns plus that unknown."
    },
    "newtons_laws": {
        "title": "Newton's Laws of Motion",
        "citation": "Growth Grid Physics Basics, §3.1 (Classical Dynamics)",
        "summary": "1st Law: Inertia. 2nd Law: Net Force = mass * acceleration (ΣF = m*a). 3rd Law: For every action, there is an equal and opposite reaction force.",
        "common_errors": "Forgetting normal force or friction in Free Body Diagrams (FBD).",
        "guidance": "Step 1: Draw a Free Body Diagram (FBD). Step 2: Identify all contact and non-contact forces. Step 3: Apply ΣF_x = m*a_x and ΣF_y = m*a_y."
    },
    "variables_datatypes": {
        "title": "Variables and Data Types",
        "citation": "Growth Grid Coding Fundamentals, §1.1 (Memory & Types)",
        "summary": "Variables store values in memory. Fundamental types: Integer (int), Floating-point (float), Boolean (bool), String (str). Type coercion converts one type to another.",
        "common_errors": "Confusing integer division with float division, or variable shadowing.",
        "guidance": "Step 1: Inspect value type. Step 2: Match variable declaration. Step 3: Verify scope boundaries."
    },
    "conditionals_logic": {
        "title": "Conditionals and Boolean Logic",
        "citation": "Growth Grid Coding Fundamentals, §2.1 (Control Flow)",
        "summary": "Branching statements (if, else if, else) execute code blocks based on truth values. Logical operators: AND (&&), OR (||), NOT (!). De Morgan's Laws: !(A && B) == (!A || !B).",
        "common_errors": "Using assignment operator (=) instead of equality comparison (==).",
        "guidance": "Step 1: Evaluate inner boolean expressions. Step 2: Follow branch hierarchy. Step 3: Handle edge conditions in else."
    },
    "loops_iteration": {
        "title": "Loops and Iteration",
        "citation": "Growth Grid Coding Fundamentals, §3.2 (Iterative Execution)",
        "summary": "Loops repeat a block while a condition holds. For-loops iterate over sequences; while-loops iterate until a condition becomes false. Termination conditions are vital to prevent infinite loops.",
        "common_errors": "Off-by-one errors in range bounds (e.g. range(0, n) stops at n-1).",
        "guidance": "Step 1: Define loop invariant. Step 2: Check initialization value. Step 3: Check increment and boundary exit condition."
    }
}

class RagAiTutor:
    def retrieve_context(self, query: str) -> Dict[str, Any]:
        """Simple keyword/concept retrieval over STEM corpus."""
        q_lower = query.lower()
        best_match = STEM_KNOWLEDGE_CORPUS["linear_equations"]
        
        for key, entry in STEM_KNOWLEDGE_CORPUS.items():
            if (key in q_lower or 
                any(word in q_lower for word in entry["title"].lower().split()) or
                any(token in q_lower for token in key.split("_"))):
                best_match = entry
                break

        return best_match

    def generate_response(
        self,
        user_message: str,
        scaffold_tier: int = 1,
        language: str = "en",
        topic_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates pedagogically sound responses based on scaffolding tier:
        - Tier 1: Socratic Hint (Never reveals final answer)
        - Tier 2: Step-by-Step Breakdown
        - Tier 3: Complete Solution & Course Citation
        """
        context = self.retrieve_context(f"{topic_title or ''} {user_message}")

        # English Templates
        if scaffold_tier == 1:
            reply_en = (
                f"💡 **Concept Hint:** Think about how **{context['title']}** works.\n\n"
                f"Recall: {context['summary']}\n\n"
                f"❓ *Guiding Question:* What is the first balance operation you need to isolate the key term? "
                f"Avoid this common pitfall: *{context['common_errors']}*\n\n"
                f"Would you like a step-by-step walkthrough or another hint?"
            )
            followups = ["Give me a step-by-step breakdown", "Show me the full solution", "Explain with an example"]
        elif scaffold_tier == 2:
            reply_en = (
                f"📝 **Step-by-Step Guidance:**\n\n"
                f"{context['guidance']}\n\n"
                f"🔍 *Checkpoint:* Apply step 1 to your current numbers. What intermediate value do you obtain before solving for the final result?"
            )
            followups = ["Show full solution with citation", "I think the answer is...", "Explain the formula again"]
        else:
            reply_en = (
                f"📖 **Complete Solution & Derivation:**\n\n"
                f"1. **Core Principle:** According to **{context['citation']}**, {context['summary']}\n\n"
                f"2. **Detailed Solution Path:**\n{context['guidance']}\n\n"
                f"3. **Verification:** Always substitute your result back into the original expression to confirm both sides balance.\n\n"
                f"📌 *Source Citation:* `{context['citation']}`"
            )
            followups = ["Practice another question like this", "Test my mastery on this concept", "Switch topic"]

        # Multilingual localization for Tamil & Hindi
        if language == "ta":
            tamil_prefix = {
                1: f"💡 **குறிப்பு (Hint):** {context['title']} பற்றிய முக்கிய கருத்து:\n{context['summary']}\n\nமுதல் படியை கவனியுங்கள். அடுத்த உதவி வேண்டுமா?",
                2: f"📝 **படிப்படியான வழிகாட்டுதல் (Step-by-step):**\n{context['guidance']}\n\nஇப்போது உங்கள் சமன்பாட்டை தீர்க்க முயற்சிக்கவும்.",
                3: f"📖 **முழுமையான தீர்வு (Full Solution):**\nஆதாரம்: {context['citation']}\n{context['guidance']}\nமுடிவை எப்போதும் சரிபார்க்கவும்."
            }
            reply = tamil_prefix.get(scaffold_tier, reply_en)
        elif language == "hi":
            hindi_prefix = {
                1: f"💡 **संकेत (Hint):** {context['title']} के मुख्य सिद्धांत पर ध्यान दें:\n{context['summary']}\n\nक्या आप चरणबद्ध मार्गदर्शन चाहते हैं?",
                2: f"📝 **चरणबद्ध समाधान (Step-by-step):**\n{context['guidance']}\n\nपहले चरण को हल करके देखें।",
                3: f"📖 **पूर्ण समाधान और संदर्भ (Full Solution):**\nसंदर्भ: {context['citation']}\n{context['guidance']}\nउत्तर की पुन: जांच करें।"
            }
            reply = hindi_prefix.get(scaffold_tier, reply_en)
        else:
            reply = reply_en

        return {
            "reply": reply,
            "scaffold_tier": scaffold_tier,
            "course_citation": context["citation"] if scaffold_tier >= 2 else None,
            "suggested_followups": followups,
            "detected_concept": context["title"]
        }

rag_tutor = RagAiTutor()
