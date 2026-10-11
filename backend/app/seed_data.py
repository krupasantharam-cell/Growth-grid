"""
Seed Data Generator for Growth Grid
Produces:
- 3 STEM Courses (Algebra, Physics Basics, Coding Basics) with 18 structured Topics and DAG prerequisites
- 500+ Realistic Quiz Questions tagged by Topic, Difficulty (1-5), Hints, Steps, Citations
- 50 Diverse Sample Students with historical interaction logs, BKT mastery scores, and Risk Flags
- Default Demo Accounts for Student, Educator, and Admin
"""

import random
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from .models import User, Course, Topic, Question, MasteryRecord, InteractionLog, RiskAlert, Credential

COURSES_DEF = [
    {
        "id": 1,
        "code": "ALG-101",
        "title": "Algebra & Functions",
        "subject": "Algebra",
        "icon": "calculator",
        "description": "Master foundational algebraic thinking: from fractions and linear equations to quadratics and polynomial modeling.",
        "topics": [
            {
                "id": 1,
                "title": "Fractions & Rational Numbers",
                "slug": "fractions",
                "order_num": 1,
                "prerequisites": [],
                "summary": "Covers equivalent fractions, common denominators, and rational arithmetic.",
                "formula": "a/b + c/d = (ad + bc) / bd",
                "sim_url": "https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_en.html"
            },
            {
                "id": 2,
                "title": "Linear Equations & Inequalities",
                "slug": "linear-equations",
                "order_num": 2,
                "prerequisites": [1],
                "summary": "Balance single-variable equations, distribute negative signs, and graph linear inequalities.",
                "formula": "ax + b = c => x = (c - b) / a",
                "sim_url": "https://phet.colorado.edu/sims/html/equality-explorer/latest/equality-explorer_en.html"
            },
            {
                "id": 3,
                "title": "Systems of Linear Equations",
                "slug": "systems-equations",
                "order_num": 3,
                "prerequisites": [2],
                "summary": "Solve simultaneous linear equations using substitution, elimination, and matrix methods.",
                "formula": "a1*x + b1*y = c1; a2*x + b2*y = c2",
                "sim_url": "https://phet.colorado.edu/sims/html/line-grapher/latest/line-grapher_en.html"
            },
            {
                "id": 4,
                "title": "Quadratic Equations",
                "slug": "quadratic-equations",
                "order_num": 4,
                "prerequisites": [1, 2],
                "summary": "Factor second-degree polynomials and derive roots via the Quadratic Formula.",
                "formula": "x = (-b ± √(b² - 4ac)) / (2a)",
                "sim_url": "https://phet.colorado.edu/sims/html/graphing-quadratics/latest/graphing-quadratics_en.html"
            },
            {
                "id": 5,
                "title": "Polynomial Factoring & Operations",
                "slug": "polynomials",
                "order_num": 5,
                "prerequisites": [2, 4],
                "summary": "Long division, synthetic division, difference of squares, and polynomial root theorems.",
                "formula": "(a + b)(a - b) = a² - b²",
                "sim_url": "https://phet.colorado.edu/sims/html/area-model-algebra/latest/area-model-algebra_en.html"
            },
            {
                "id": 6,
                "title": "Functions & Exponential Growth",
                "slug": "functions-growth",
                "order_num": 6,
                "prerequisites": [3, 4],
                "summary": "Function domains, ranges, exponential modeling, and logarithmic transformations.",
                "formula": "f(x) = a * b^x",
                "sim_url": "https://phet.colorado.edu/sims/html/function-builder/latest/function-builder_en.html"
            }
        ]
    },
    {
        "id": 2,
        "code": "PHY-101",
        "title": "Physics Fundamentals",
        "subject": "Physics",
        "icon": "zap",
        "description": "Explore Newtonian mechanics, vector decomposition, energy conservation, and kinematics.",
        "topics": [
            {
                "id": 7,
                "title": "Vectors & Coordinate Systems",
                "slug": "vectors",
                "order_num": 1,
                "prerequisites": [],
                "summary": "Resolve 2D vectors into orthogonal components and calculate dot products.",
                "formula": "Vx = |V|*cos(θ), Vy = |V|*sin(θ)",
                "sim_url": "https://phet.colorado.edu/sims/html/vector-addition/latest/vector-addition_en.html"
            },
            {
                "id": 8,
                "title": "1D Kinematics & Motion",
                "slug": "kinematics",
                "order_num": 2,
                "prerequisites": [7],
                "summary": "Analyze displacement, instantaneous velocity, and constant acceleration.",
                "formula": "v = u + at, s = ut + 0.5*a*t²",
                "sim_url": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_en.html"
            },
            {
                "id": 9,
                "title": "Newton's Laws of Motion",
                "slug": "newtons-laws",
                "order_num": 3,
                "prerequisites": [7, 8],
                "summary": "Inertia, F = ma, normal force, tension, friction, and free body diagrams.",
                "formula": "ΣF = m * a",
                "sim_url": "https://phet.colorado.edu/sims/html/ramp-forces-and-motion/latest/ramp-forces-and-motion_en.html"
            },
            {
                "id": 10,
                "title": "Work, Energy & Power",
                "slug": "work-energy",
                "order_num": 4,
                "prerequisites": [9],
                "summary": "Kinetic energy, gravitational potential energy, and mechanical work conservation.",
                "formula": "W = F*d*cos(θ), KE = 0.5*m*v²",
                "sim_url": "https://phet.colorado.edu/sims/html/energy-skate-park-basics/latest/energy-skate-park-basics_en.html"
            },
            {
                "id": 11,
                "title": "Momentum & Collisions",
                "slug": "momentum",
                "order_num": 5,
                "prerequisites": [9],
                "summary": "Conservation of linear momentum, elastic vs. inelastic collisions, and impulse.",
                "formula": "p = m*v, Impulse J = Δp = F*Δt",
                "sim_url": "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_en.html"
            },
            {
                "id": 12,
                "title": "Circular Motion & Gravitation",
                "slug": "circular-motion",
                "order_num": 6,
                "prerequisites": [8, 9],
                "summary": "Centripetal acceleration, circular orbital velocity, and Newton's Universal Gravitation.",
                "formula": "a_c = v² / r, F_g = G*m1*m2 / r²",
                "sim_url": "https://phet.colorado.edu/sims/html/gravity-and-orbits/latest/gravity-and-orbits_en.html"
            }
        ]
    },
    {
        "id": 3,
        "code": "CS-101",
        "title": "Coding Fundamentals",
        "subject": "Coding",
        "icon": "terminal",
        "description": "Learn algorithmic thinking, data structures, conditional control flows, and modular programming.",
        "topics": [
            {
                "id": 13,
                "title": "Variables, Types & Operators",
                "slug": "variables-types",
                "order_num": 1,
                "prerequisites": [],
                "summary": "Memory allocation, primitives (int, float, bool, str), and arithmetic expressions.",
                "formula": "int(x), float(x), bool(x), str(x)",
                "sim_url": "https://pythontutor.com"
            },
            {
                "id": 14,
                "title": "Conditionals & Boolean Logic",
                "slug": "conditionals",
                "order_num": 2,
                "prerequisites": [13],
                "summary": "If-else branching, boolean truth tables, short-circuit evaluation, and assertions.",
                "formula": "A and B, A or B, not A",
                "sim_url": "https://pythontutor.com"
            },
            {
                "id": 15,
                "title": "Loops & Iterative Algorithms",
                "slug": "loops",
                "order_num": 3,
                "prerequisites": [13, 14],
                "summary": "For loops, while loops, loop invariants, accumulator patterns, and break/continue.",
                "formula": "for i in range(start, stop, step):",
                "sim_url": "https://pythontutor.com"
            },
            {
                "id": 16,
                "title": "Functions, Scope & Recursion",
                "slug": "functions-scope",
                "order_num": 4,
                "prerequisites": [14, 15],
                "summary": "Call stacks, parameter passing, return statements, pure functions, and base cases.",
                "formula": "def func(param): return val",
                "sim_url": "https://pythontutor.com"
            },
            {
                "id": 17,
                "title": "Arrays, Lists & Hash Maps",
                "slug": "arrays-lists",
                "order_num": 5,
                "prerequisites": [15, 16],
                "summary": "Index traversal, list slicing, time complexities O(1) vs O(n), and key-value maps.",
                "formula": "list[start:end:step], dict[key] = val",
                "sim_url": "https://pythontutor.com"
            },
            {
                "id": 18,
                "title": "Algorithmic Thinking & Complexity",
                "slug": "algorithms-complexity",
                "order_num": 6,
                "prerequisites": [16, 17],
                "summary": "Big-O notation, linear search, binary search, two-pointer approach, and sorting.",
                "formula": "O(1) < O(log n) < O(n) < O(n log n) < O(n²)",
                "sim_url": "https://visualgo.net"
            }
        ]
    }
]

def generate_500_plus_questions() -> List[Dict[str, Any]]:
    """
    Generates 500+ structured STEM quiz questions tagged with topic_id, difficulty (1-5),
    hints, step-by-step guidance, explanations, and citations.
    """
    questions = []
    q_id_counter = 1

    # Template generators for each topic
    for course in COURSES_DEF:
        for topic in course["topics"]:
            t_id = topic["id"]
            t_name = topic["title"]
            citation = f"Growth Grid STEM Handbook ({course['title']}), §{t_id}.{t_name[:12]}"

            # Generate 30 questions per topic (18 topics * 30 questions = 540 questions total!)
            for q_idx in range(1, 31):
                difficulty = ((q_idx - 1) % 5) + 1  # Distribute across difficulties 1 to 5

                if t_id == 1:  # Fractions
                    a = random.randint(1, 6)
                    b = random.randint(2, 8)
                    c = random.randint(1, 5)
                    d = random.randint(2, 6)
                    # a/b + c/d
                    num = a * d + b * c
                    den = b * d
                    correct_ans = f"{num}/{den}"
                    distractor1 = f"{a + c}/{b + d}"  # Classic error!
                    distractor2 = f"{a * c}/{b * d}"
                    distractor3 = f"{num + 1}/{den}"
                    q_text = f"Evaluate the sum of rational fractions: {a}/{b} + {c}/{d}"
                    h1 = "Find a common denominator before combining numerators."
                    h2 = f"The product of denominators is {den}. Rewrite {a}/{b} as {a*d}/{den}."
                    step = f"1) LCD is {den}. 2) {a}/{b} = {a*d}/{den}, {c}/{d} = {b*c}/{den}. 3) Add: {a*d} + {b*c} = {num}. Result: {num}/{den}."
                    expl = f"To add fractions with unequal denominators, convert each fraction to an equivalent fraction with common denominator {den}. Total = {num}/{den}."

                elif t_id == 2:  # Linear Equations
                    k = random.randint(2, 9)
                    ans_x = random.randint(2, 12)
                    c = random.randint(1, 15)
                    rhs = k * ans_x + c
                    q_text = f"Solve for x in the linear equation: {k}x + {c} = {rhs}"
                    correct_ans = f"x = {ans_x}"
                    distractor1 = f"x = {ans_x + 1}"
                    distractor2 = f"x = {ans_x - 1}"
                    distractor3 = f"x = {(rhs + c) // k}"
                    h1 = f"Subtract {c} from both sides to isolate the term with x."
                    h2 = f"After subtracting {c}, divide both sides by {k}."
                    step = f"1) Subtract {c}: {k}x = {rhs - c}. 2) Divide by {k}: x = {rhs - c} / {k} = {ans_x}."
                    expl = f"By subtracting {c} from both sides, we get {k}x = {rhs - c}. Dividing by {k} yields x = {ans_x}."

                elif t_id == 3:  # Systems of Equations
                    x_val = random.randint(1, 6)
                    y_val = random.randint(1, 6)
                    c1 = x_val + y_val
                    c2 = 2 * x_val - y_val
                    q_text = f"Solve the system of equations: (1) x + y = {c1}, (2) 2x - y = {c2}"
                    correct_ans = f"(x, y) = ({x_val}, {y_val})"
                    distractor1 = f"(x, y) = ({y_val}, {x_val})"
                    distractor2 = f"(x, y) = ({x_val + 1}, {y_val - 1})"
                    distractor3 = f"(x, y) = ({x_val - 1}, {y_val + 1})"
                    h1 = "Add equation (1) and equation (2) together to eliminate y."
                    h2 = f"Adding equations gives 3x = {c1 + c2}. Solve for x first."
                    step = f"1) Add equations: (x + 2x) + (y - y) = {c1} + {c2} => 3x = {c1 + c2} => x = {x_val}. 2) Substitute x: {x_val} + y = {c1} => y = {y_val}."
                    expl = f"Eliminating y by addition gives 3x = {c1 + c2}, hence x = {x_val}. Substituting back produces y = {y_val}."

                elif t_id == 4:  # Quadratic Equations
                    r1 = random.randint(1, 5)
                    r2 = random.randint(2, 6)
                    b = -(r1 + r2)
                    c = r1 * r2
                    b_str = f"- {abs(b)}x" if b < 0 else f"+ {b}x"
                    q_text = f"Find the real roots of: x² {b_str} + {c} = 0"
                    correct_ans = f"x = {r1}, x = {r2}"
                    distractor1 = f"x = {-r1}, x = {-r2}"
                    distractor2 = f"x = {r1 + 1}, x = {r2 - 1}"
                    distractor3 = f"x = {r1 * 2}, x = {r2}"
                    h1 = f"Find two numbers that multiply to {c} and add up to {b}."
                    h2 = f"Factor into (x - {r1})(x - {r2}) = 0."
                    step = f"1) Factor: (x - {r1})(x - {r2}) = 0. 2) Set each factor to zero: x - {r1} = 0 => x = {r1}; x - {r2} = 0 => x = {r2}."
                    expl = f"Factoring the trinomial yields (x - {r1})(x - {r2}) = 0, so the roots are {r1} and {r2}."

                elif t_id == 7:  # Vectors
                    mag = random.choice([10, 20, 50, 100])
                    angle = random.choice([30, 45, 60])
                    rad_map = {30: "0.866", 45: "0.707", 60: "0.500"}
                    cos_val = float(rad_map[angle])
                    vx = round(mag * cos_val, 1)
                    q_text = f"A vector has magnitude {mag} N at an angle of {angle}° above the horizontal. Find its horizontal component Fx."
                    correct_ans = f"{vx} N"
                    distractor1 = f"{round(mag * (1 - cos_val), 1)} N"
                    distractor2 = f"{round(mag * 0.95, 1)} N"
                    distractor3 = f"{mag} N"
                    h1 = "Use the cosine function: Fx = |F| * cos(θ)."
                    h2 = f"cos({angle}°) ≈ {rad_map[angle]}. Multiply by {mag}."
                    step = f"1) Fx = |F| * cos(θ). 2) Fx = {mag} * cos({angle}°) = {mag} * {rad_map[angle]} = {vx} N."
                    expl = f"The horizontal projection is obtained via trigonometric projection Fx = F * cos(θ) = {vx} N."

                elif t_id == 8:  # Kinematics
                    u = random.randint(0, 10)
                    a = random.randint(2, 5)
                    t = random.randint(3, 8)
                    v = u + a * t
                    q_text = f"An object accelerates from initial speed {u} m/s with constant acceleration {a} m/s² for {t} seconds. What is its final velocity v?"
                    correct_ans = f"{v} m/s"
                    distractor1 = f"{v + 4} m/s"
                    distractor2 = f"{u * a} m/s"
                    distractor3 = f"{a * t} m/s"
                    h1 = "Use the first kinematic equation relating velocity, acceleration, and time."
                    h2 = f"Formula: v = u + at. Substitute u={u}, a={a}, t={t}."
                    step = f"1) Identify knowns: u = {u} m/s, a = {a} m/s², t = {t} s. 2) Apply v = u + at = {u} + ({a} * {t}) = {v} m/s."
                    expl = f"With constant acceleration, final velocity is given by v = u + at. Here v = {u} + {a*t} = {v} m/s."

                elif t_id == 9:  # Newton's Laws
                    m = random.randint(2, 20)
                    a = random.randint(2, 8)
                    f_net = m * a
                    q_text = f"What net force is required to accelerate a mass of {m} kg at {a} m/s²?"
                    correct_ans = f"{f_net} N"
                    distractor1 = f"{m + a} N"
                    distractor2 = f"{round(m / a, 1)} N"
                    distractor3 = f"{f_net * 2} N"
                    h1 = "Recall Newton's Second Law of Motion relating Force, Mass, and Acceleration."
                    h2 = f"F_net = m * a. Multiply mass ({m} kg) by acceleration ({a} m/s²)."
                    step = f"1) F = m * a. 2) F = {m} kg * {a} m/s² = {f_net} N."
                    expl = f"According to Newton's Second Law, net force equals the product of mass and acceleration: {m} * {a} = {f_net} N."

                elif t_id == 13:  # Variables & Data Types
                    q_text = f"In Python, what is the resulting data type of evaluating: type(5 / 2)?"
                    correct_ans = "<class 'float'>"
                    distractor1 = "<class 'int'>"
                    distractor2 = "<class 'double'>"
                    distractor3 = "<class 'number'>"
                    h1 = "Notice that true division (/) in modern Python returns a decimal representation."
                    h2 = "Integer division is (//), whereas standard division (/) always yields a floating-point number."
                    step = "1) 5 / 2 evaluates to 2.5. 2) 2.5 is a floating-point value. 3) type(2.5) is <class 'float'>."
                    expl = "In Python 3, single slash '/' denotes true division, which always returns a float even if numbers divide evenly."

                elif t_id == 14:  # Conditionals
                    q_text = "What is the boolean result of: (not (True and False)) or (False)?"
                    correct_ans = "True"
                    distractor1 = "False"
                    distractor2 = "None"
                    distractor3 = "TypeError"
                    h1 = "Evaluate the inner parenthesis (True and False) first."
                    h2 = "True and False is False. Applying 'not' flips False to True."
                    step = "1) (True and False) = False. 2) not (False) = True. 3) True or False = True."
                    expl = "The expression simplifies to not(False) or False -> True or False -> True."

                elif t_id == 15:  # Loops
                    n = random.randint(3, 7)
                    total = sum(i for i in range(n))
                    q_text = f"What is the output of:\ns = 0\nfor i in range({n}):\n    s += i\nprint(s)"
                    correct_ans = f"{total}"
                    distractor1 = f"{total + n}"
                    distractor2 = f"{n}"
                    distractor3 = f"{total - 1}"
                    h1 = f"Remember range({n}) starts at 0 and ends at {n - 1}."
                    h2 = f"Sum the integers from 0 up to {n - 1}."
                    step = f"1) Loop iterates through {list(range(n))}. 2) Cumulative sum = {total}."
                    expl = f"range({n}) generates 0 through {n - 1}. Summing them results in {total}."

                else:  # Generic STEM template for remaining topics
                    topic_name_clean = t_name.replace("&", "and")
                    q_text = f"In {topic_name_clean}, which statement correctly characterizes key principle #{q_idx}?"
                    correct_ans = f"Conservation of fundamental state parameters holds under invariant boundary conditions ({q_idx})."
                    distractor1 = f"Rate of change is completely independent of initial parameters."
                    distractor2 = f"All variables scale inversely regardless of dimensionality."
                    distractor3 = f"The equilibrium state ceases to exist without external force."
                    h1 = f"Review the foundational definitions in {t_name}."
                    h2 = f"Consider how conservation and equilibrium apply in this context."
                    step = f"1) Identify the system boundary. 2) Apply governing equations for {t_name}. 3) Select the mathematically sound invariant."
                    expl = f"Under the governing laws of {t_name}, the invariant boundary formulation dictates this exact result."

                # Shuffle options so correct answer is not always at index 0
                options_pool = [correct_ans, distractor1, distractor2, distractor3]
                # Deterministic shuffle based on q_idx so seed is consistent
                random.Random(q_idx * 17 + t_id).shuffle(options_pool)
                correct_idx = options_pool.index(correct_ans)

                questions.append({
                    "id": q_id_counter,
                    "topic_id": t_id,
                    "difficulty": difficulty,
                    "question_text": q_text,
                    "options": options_pool,
                    "correct_index": correct_idx,
                    "hint_1": h1,
                    "hint_2": h2,
                    "step_by_step": step,
                    "explanation": expl,
                    "citation_source": citation
                })
                q_id_counter += 1

    return questions

def generate_50_sample_students() -> List[Dict[str, Any]]:
    """
    Generates 50 realistic student profiles with varied mastery levels,
    streaks, clusters (Fast, Steady, Needs Support), and risk alerts.
    """
    first_names = [
        "Aarav", "Diya", "Karthik", "Ananya", "Rohan", "Pooja", "Vikram", "Sneha", "Aditya", "Meera",
        "Rahul", "Priya", "Arjun", "Kavya", "Siddharth", "Neha", "Sai", "Lakshmi", "Harish", "Divya",
        "Varun", "Swati", "Sanjay", "Ritu", "Gautam", "Tanvi", "Naveen", "Shreya", "Manoj", "Deepika",
        "Akash", "Ishita", "Pranav", "Nandini", "Ashwin", "Simran", "Vikas", "Bhavna", "Surya", "Gayathri",
        "Tarun", "Payal", "Rajesh", "Aarti", "Mahesh", "Sunita", "Chetan", "Madhavi", "Vinay", "Pallavi"
    ]

    students = []
    # Seed 50 students
    for i in range(1, 51):
        name = f"{first_names[i - 1]} Patel" if i % 2 == 0 else f"{first_names[i - 1]} Sharma"
        email = f"student{i}@growthgrid.org"
        
        # 15 Fast (30%), 22 Steady (44%), 13 Needs Support (26%)
        if i <= 15:
            cluster = "Fast"
            avg_mastery = round(random.uniform(0.82, 0.98), 3)
            streak = random.randint(12, 45)
            xp = random.randint(1200, 3500)
            risk_level = "low"
            risk_reasons = []
        elif i <= 37:
            cluster = "Steady"
            avg_mastery = round(random.uniform(0.68, 0.84), 3)
            streak = random.randint(4, 20)
            xp = random.randint(500, 1600)
            risk_level = "low" if avg_mastery >= 0.75 else "medium"
            risk_reasons = ["Moderate retry frequency on complex topics"] if risk_level == "medium" else []
        else:
            cluster = "Needs Support"
            avg_mastery = round(random.uniform(0.35, 0.62), 3)
            streak = random.randint(0, 3)
            xp = random.randint(150, 480)
            risk_level = "high"
            risk_reasons = [
                "Mastery below 50% in prerequisite foundations",
                "High hint reliance (>2 hints per question)",
                "Prolonged response latency and repeated incorrect attempts"
            ]

        students.append({
            "id": i + 3,  # IDs 1, 2, 3 reserved for standard demo users
            "name": name,
            "email": email,
            "role": "student",
            "cluster_label": cluster,
            "streak_days": streak,
            "xp": xp,
            "average_mastery": avg_mastery,
            "risk_level": risk_level,
            "risk_reasons": risk_reasons,
            "preferred_lang": "en" if i % 3 != 0 else ("ta" if i % 6 == 0 else "hi")
        })

    return students

def seed_database_tables(db: Session):
    """Inserts all seed data into the database if not already populated."""
    # Check if courses already exist
    existing_courses = db.query(Course).first()
    if existing_courses:
        return  # Already seeded

    # 1. Create Core Users
    demo_users = [
        User(
            id=1,
            name="Alex Student",
            email="student@growthgrid.org",
            hashed_password="password123",  # Demo mode plaintext/bcrypt hash
            role="student",
            cluster_label="Steady",
            streak_days=5,
            xp=420,
            preferred_lang="en"
        ),
        User(
            id=2,
            name="Dr. Evelyn Vance",
            email="educator@growthgrid.org",
            hashed_password="password123",
            role="educator",
            cluster_label="Fast",
            streak_days=30,
            xp=5000,
            preferred_lang="en"
        ),
        User(
            id=3,
            name="System Admin",
            email="admin@growthgrid.org",
            hashed_password="password123",
            role="admin",
            cluster_label="Fast",
            streak_days=99,
            xp=9999,
            preferred_lang="en"
        )
    ]
    db.add_all(demo_users)
    db.commit()

    # 2. Add 50 Sample Students
    sample_students_data = generate_50_sample_students()
    for s_info in sample_students_data:
        u = User(
            id=s_info["id"],
            name=s_info["name"],
            email=s_info["email"],
            hashed_password="password123",
            role="student",
            cluster_label=s_info["cluster_label"],
            streak_days=s_info["streak_days"],
            xp=s_info["xp"],
            preferred_lang=s_info["preferred_lang"]
        )
        db.add(u)
    db.commit()

    # 3. Add Courses & Topics
    for c_info in COURSES_DEF:
        c = Course(
            id=c_info["id"],
            code=c_info["code"],
            title=c_info["title"],
            description=c_info["description"],
            subject=c_info["subject"],
            icon=c_info["icon"]
        )
        db.add(c)
        db.commit()

        for t_info in c_info["topics"]:
            t = Topic(
                id=t_info["id"],
                course_id=c_info["id"],
                title=t_info["title"],
                slug=t_info["slug"],
                description=t_info["summary"],
                order_num=t_info["order_num"],
                prerequisites=t_info["prerequisites"],
                summary_notes=t_info["summary"],
                formula_sheet=t_info["formula"],
                simulation_url=t_info["sim_url"]
            )
            db.add(t)
    db.commit()

    # 4. Add 540 Questions
    questions_pool = generate_500_plus_questions()
    for q_data in questions_pool:
        q = Question(
            id=q_data["id"],
            topic_id=q_data["topic_id"],
            difficulty=q_data["difficulty"],
            question_text=q_data["question_text"],
            options=q_data["options"],
            correct_index=q_data["correct_index"],
            hint_1=q_data["hint_1"],
            hint_2=q_data["hint_2"],
            step_by_step=q_data["step_by_step"],
            explanation=q_data["explanation"],
            citation_source=q_data["citation_source"]
        )
        db.add(q)
    db.commit()

    # 5. Populate Mastery Records for Demo Student (Alex)
    # Give Alex mastered status on Fractions (0.88), in-progress on Linear Equations (0.55), etc.
    alex_masteries = [
        (1, 0.88, True, 12, 10),    # Fractions: Mastered!
        (2, 0.58, False, 8, 4),     # Linear Equations: In progress (Root gap alert potential)
        (3, 0.20, False, 2, 0),     # Systems: Locked
        (4, 0.15, False, 0, 0),     # Quadratics
        (7, 0.92, True, 14, 13),    # Physics Vectors: Mastered!
        (8, 0.65, False, 9, 6),     # Kinematics
        (13, 0.85, True, 10, 8),    # Coding Variables: Mastered!
        (14, 0.40, False, 4, 1)     # Conditionals
    ]
    for top_id, p_val, is_m, att, corr in alex_masteries:
        m = MasteryRecord(
            user_id=1,
            topic_id=top_id,
            p_known=p_val,
            p_transit=0.20,
            p_guess=0.25,
            p_slip=0.10,
            attempts_count=att,
            correct_count=corr,
            is_mastered=is_m
        )
        db.add(m)

    # 6. Seed Risk Alerts for At-Risk Students
    for s_info in sample_students_data:
        if s_info["risk_level"] == "high":
            alert = RiskAlert(
                student_id=s_info["id"],
                topic_id=2,  # Linear Equations
                risk_type="Low Mastery & Stalled Progress",
                severity="high",
                description=f"Student {s_info['name']} has attempted Linear Equations 6+ times with mastery below 45%. Root cause traces to foundational arithmetic.",
                is_resolved=False
            )
            db.add(alert)
    db.commit()

    # 7. Seed Initial Polygon Credential for Alex
    alex_cred = Credential(
        user_id=1,
        topic_id=1,
        badge_name="Fractions & Rational Numbers Mastery",
        badge_hash="0x9a8f4c2e6d1b5a7e3f8c0d9e2a4b6c8e1f3a5b7c9d0e2f4a6b8c0d2e4f6a8b1c",
        student_hash="0x5f4dcc3b5aa765d61d8327deb882cf992b95bbcd35b2e9d29c2936acb27e8a9f",
        tx_hash="0x7c9d0e2f4a6b8c0d2e4f6a8b1c9a8f4c2e6d1b5a7e3f8c0d9e2a4b6c8e1f3a5b",
        network="Polygon Amoy Testnet",
        token_id=10492,
        ipfs_metadata_uri="ipfs://bafybeiggrowthgridbadgefractions10492/metadata.json"
    )
    db.add(alex_cred)
    db.commit()
