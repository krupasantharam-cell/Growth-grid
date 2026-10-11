"""
Unit Tests for Growth Grid Core Logic
Tests:
- Bayesian Knowledge Tracing (BKT) updates
- Prerequisite Knowledge Graph & Root Gap Detection
- K-Means Learner Clustering
- RAG AI Tutor Socratic Scaffolding
- Blockchain Badge Zero-PII Hashing
"""

import pytest
from app.ml.bkt_engine import bkt_engine, MASTERY_THRESHOLD
from app.ml.clustering import clustering_service
from app.ml.decision_engine import decision_engine
from app.ai_tutor.rag_tutor import rag_tutor
from app.blockchain.badge_issuer import badge_issuer

def test_bkt_correct_answer_increases_mastery():
    prior = 0.20
    new_p, telemetry = bkt_engine.update_mastery(p_known=prior, is_correct=True, hints_used=0)
    assert new_p > prior
    assert telemetry["is_mastered"] is False

def test_bkt_incorrect_answer_decreases_or_damps_mastery():
    prior = 0.50
    new_p, telemetry = bkt_engine.update_mastery(p_known=prior, is_correct=False, hints_used=0)
    # Posterior should be significantly lower than prior before learning transition
    assert telemetry["posterior_p_known"] < prior

def test_bkt_mastery_gate_threshold():
    # High prior + correct answer should cross 80% threshold
    prior = 0.78
    new_p, telemetry = bkt_engine.update_mastery(p_known=prior, is_correct=True, hints_used=0)
    assert new_p >= MASTERY_THRESHOLD
    assert telemetry["is_mastered"] is True

def test_bkt_dynamic_difficulty_scaling():
    diff_low = bkt_engine.select_next_difficulty(p_known=0.20, last_correct=False)
    assert diff_low == 1
    diff_high = bkt_engine.select_next_difficulty(p_known=0.90, last_correct=True)
    assert diff_high == 5

def test_learner_clustering_heuristic():
    fast_profile = clustering_service.predict_profile([0.90, 12.0, 0.1, 0.10])
    assert fast_profile == "Fast"

    support_profile = clustering_service.predict_profile([0.45, 45.0, 2.0, 0.55])
    assert support_profile == "Needs Support"

def test_root_gap_detection():
    class MockTopic:
        def __init__(self, id, title, prerequisites, order_num):
            self.id = id
            self.title = title
            self.prerequisites = prerequisites
            self.order_num = order_num

    topics_map = {
        1: MockTopic(1, "Fractions", [], 1),
        2: MockTopic(2, "Linear Equations", [1], 2),
        3: MockTopic(3, "Systems of Equations", [2], 3)
    }

    # Student has low Fractions (0.40) and is trying to solve Linear Equations
    mastery_map = {1: 0.40, 2: 0.30, 3: 0.10}
    root_gap = decision_engine.find_root_gap(2, topics_map, mastery_map)
    assert root_gap == 1  # Fractions is the root gap!

def test_rag_tutor_scaffolding_tiers():
    # Tier 1 must NOT show the full solution
    resp_tier1 = rag_tutor.generate_response("How do I solve 2x + 5 = 15?", scaffold_tier=1, language="en")
    assert "Concept Hint" in resp_tier1["reply"]
    assert resp_tier1["course_citation"] is None

    # Tier 3 must include official course citation
    resp_tier3 = rag_tutor.generate_response("How do I solve 2x + 5 = 15?", scaffold_tier=3, language="en")
    assert resp_tier3["course_citation"] is not None
    assert "Complete Solution" in resp_tier3["reply"]

def test_rag_tutor_multilingual():
    resp_ta = rag_tutor.generate_response("linear equations", scaffold_tier=1, language="ta")
    assert "குறிப்பு" in resp_ta["reply"]

    resp_hi = rag_tutor.generate_response("linear equations", scaffold_tier=1, language="hi")
    assert "संकेत" in resp_hi["reply"]

def test_blockchain_zero_pii_hash():
    student_id = 42
    s_hash = badge_issuer.generate_student_hash(student_id)
    assert s_hash.startswith("0x")
    assert len(s_hash) == 66
    # Personal info (like name or email) is not in the hash
    assert "42" not in s_hash[2:10]

    b_data = badge_issuer.issue_credential(
        student_id=student_id,
        topic_id=1,
        topic_title="Fractions",
        mastery_score=88.5
    )
    assert b_data["badge_hash"].startswith("0x")
    assert "Polygon" in b_data["network"]
