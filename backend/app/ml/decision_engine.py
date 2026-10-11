"""
Decision Engine & Prerequisite Knowledge Graph Gap Detector

Traverses the course Directed Acyclic Graph (DAG) of topic dependencies.
Identifies:
1. Root knowledge gaps (e.g., student struggling on Quadratic Equations due to unmastered Fractions)
2. Optimal next content: Next topic vs. Foundational remediation vs. Accelerated challenge
3. XAI transparent rationale for "Why this recommendation?"
"""

from typing import List, Dict, Any, Optional

class DecisionEngine:
    def find_root_gap(
        self,
        current_topic_id: int,
        topics_map: Dict[int, Any],
        mastery_map: Dict[int, float]
    ) -> Optional[int]:
        """
        Recursively scans prerequisite ancestors in the DAG to find the deepest unmastered skill.
        Returns the topic_id of the earliest unmastered prerequisite (< 0.80), or None if all are satisfied.
        """
        curr = topics_map.get(current_topic_id)
        if not curr:
            return None

        prereqs = curr.prerequisites or []
        for prereq_id in prereqs:
            # Check ancestor recursively first
            ancestor_gap = self.find_root_gap(prereq_id, topics_map, mastery_map)
            if ancestor_gap:
                return ancestor_gap
            
            # Check immediate prerequisite
            p_score = mastery_map.get(prereq_id, 0.0)
            if p_score < 0.80:
                return prereq_id

        return None

    def recommend_next_path(
        self,
        current_topic_id: int,
        topics_list: List[Any],
        mastery_map: Dict[int, float],
        learner_cluster: str
    ) -> Dict[str, Any]:
        """
        Determines next pedagogical intervention based on BKT score, DAG prerequisites, and cluster.
        """
        topics_map = {t.id: t for t in topics_list}
        curr_topic = topics_map.get(current_topic_id) or (topics_list[0] if topics_list else None)

        if not curr_topic:
            return {
                "recommended_topic_id": 1,
                "recommended_topic_title": "Introduction",
                "action_type": "continue",
                "explanation": {
                    "topic_title": "Introduction",
                    "reason": "Initial starting topic.",
                    "bkt_mastery_percent": 0.0,
                    "prerequisite_status": "None required",
                    "learner_cluster": learner_cluster,
                    "suggested_action": "Begin diagnostic quiz"
                }
            }

        curr_mastery = mastery_map.get(curr_topic.id, 0.0)
        curr_percent = round(curr_mastery * 100, 1)

        # 1. Check for Root Knowledge Gap in Prerequisites
        root_gap_id = self.find_root_gap(curr_topic.id, topics_map, mastery_map)

        if root_gap_id and root_gap_id != curr_topic.id:
            root_gap_topic = topics_map.get(root_gap_id)
            root_gap_score = round(mastery_map.get(root_gap_id, 0.0) * 100, 1)
            return {
                "recommended_topic_id": root_gap_id,
                "recommended_topic_title": root_gap_topic.title,
                "action_type": "remediation",
                "explanation": {
                    "topic_title": root_gap_topic.title,
                    "reason": f"Skill Gap Detected: Your mastery in prerequisite '{root_gap_topic.title}' is {root_gap_score}%, which is impeding your grasp of '{curr_topic.title}'.",
                    "bkt_mastery_percent": root_gap_score,
                    "prerequisite_status": f"Unsatisfied ancestor for {curr_topic.title}",
                    "learner_cluster": learner_cluster,
                    "suggested_action": f"Take 5-minute targeted remediation on {root_gap_topic.title} to bridge the gap."
                }
            }

        # 2. Check if Current Topic is Mastered (>= 80%)
        if curr_mastery >= 0.80:
            # Find next topic in syllabus order
            sorted_topics = sorted(topics_list, key=lambda x: x.order_num)
            next_topic = None
            for t in sorted_topics:
                if t.order_num > curr_topic.order_num:
                    next_topic = t
                    break

            if next_topic:
                action_type = "challenge" if learner_cluster == "Fast" else "continue"
                pacing_note = "Accelerated track activated: advanced concepts unlocked." if learner_cluster == "Fast" else "Mastery gate cleared (>= 80%). Ready to proceed."
                return {
                    "recommended_topic_id": next_topic.id,
                    "recommended_topic_title": next_topic.title,
                    "action_type": action_type,
                    "explanation": {
                        "topic_title": next_topic.title,
                        "reason": f"Great job! You achieved {curr_percent}% mastery on '{curr_topic.title}', unlocking the next topic.",
                        "bkt_mastery_percent": curr_percent,
                        "prerequisite_status": f"All prerequisites cleared for {next_topic.title}",
                        "learner_cluster": learner_cluster,
                        "suggested_action": pacing_note
                    }
                }
            else:
                # All topics completed!
                return {
                    "recommended_topic_id": curr_topic.id,
                    "recommended_topic_title": curr_topic.title,
                    "action_type": "review",
                    "explanation": {
                        "topic_title": curr_topic.title,
                        "reason": f"Course mastery complete ({curr_percent}%)! Ready to claim Polygon blockchain certificate.",
                        "bkt_mastery_percent": curr_percent,
                        "prerequisite_status": "All course topics completed",
                        "learner_cluster": learner_cluster,
                        "suggested_action": "Mint verifiable on-chain credential."
                    }
                }

        # 3. Current Topic is In-Progress (< 80%)
        scaffold_advice = {
            "Fast": "Attempt higher difficulty questions (Level 3-4) to quickly reach the 80% threshold.",
            "Steady": "Continue practicing with adaptive difficulty (Level 2-3) to solidify understanding.",
            "Needs Support": "Review summary notes and take guided questions with hint support enabled."
        }.get(learner_cluster, "Continue adaptive practice.")

        return {
            "recommended_topic_id": curr_topic.id,
            "recommended_topic_title": curr_topic.title,
            "action_type": "continue",
            "explanation": {
                "topic_title": curr_topic.title,
                "reason": f"Current mastery is {curr_percent}% (needs 80% to unlock next topic). Prerequisite check passed.",
                "bkt_mastery_percent": curr_percent,
                "prerequisite_status": "Prerequisites satisfied",
                "learner_cluster": learner_cluster,
                "suggested_action": scaffold_advice
            }
        }

decision_engine = DecisionEngine()
