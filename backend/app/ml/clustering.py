"""
Learner Clustering Engine using scikit-learn K-Means

Classifies students into 3 pacing profiles:
- 'Fast': High accuracy, swift completion, minimal hints. Needs accelerated challenge.
- 'Steady': Balanced pace, consistent accuracy. Standard curriculum progression.
- 'Needs Support': Frequent errors, prolonged response times, high hint usage. Needs scaffolding & remediation.
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import KMeans

class LearnerClusteringService:
    def __init__(self):
        self.model = KMeans(n_clusters=3, random_state=42, n_init=10)
        self.is_fitted = False
        self.cluster_labels_map = {0: "Steady", 1: "Fast", 2: "Needs Support"}

    def extract_features(self, student_stats: Dict[str, Any]) -> List[float]:
        """
        Features vector:
        [avg_accuracy (0-1), avg_response_time_sec (0-60), avg_hints_per_q (0-3), error_rate (0-1)]
        """
        acc = float(student_stats.get("accuracy", 0.70))
        resp_time = float(student_stats.get("avg_response_time", 20.0))
        hints = float(student_stats.get("avg_hints", 0.5))
        err_rate = float(student_stats.get("error_rate", 1.0 - acc))
        return [acc, resp_time, hints, err_rate]

    def fit_from_cohort(self, students_features: List[List[float]]):
        if len(students_features) >= 6:
            X = np.array(students_features)
            self.model.fit(X)
            self.is_fitted = True
            
            # Identify which cluster index corresponds to which profile based on cluster centers
            # Center format: [accuracy, response_time, hints, error_rate]
            centers = self.model.cluster_centers_
            # Fast cluster: highest accuracy, lowest response time
            fast_idx = int(np.argmax(centers[:, 0] - (centers[:, 1] / 60.0)))
            # Needs Support cluster: highest error rate + hints
            support_idx = int(np.argmax(centers[:, 3] + centers[:, 2]))
            
            steady_candidates = [i for i in [0, 1, 2] if i not in (fast_idx, support_idx)]
            steady_idx = steady_candidates[0] if steady_candidates else 0

            self.cluster_labels_map = {
                fast_idx: "Fast",
                steady_idx: "Steady",
                support_idx: "Needs Support"
            }

    def predict_profile(self, features: List[float]) -> str:
        """
        Predict cluster for a single student. If model not fitted, use robust heuristic boundaries.
        """
        acc, resp_time, hints, err_rate = features

        if self.is_fitted:
            try:
                cluster_idx = int(self.model.predict([features])[0])
                return self.cluster_labels_map.get(cluster_idx, "Steady")
            except Exception:
                pass

        # Robust pedagogical rule heuristic
        if acc >= 0.82 and resp_time <= 18.0 and hints <= 0.4:
            return "Fast"
        elif acc < 0.60 or hints >= 1.2 or resp_time >= 35.0:
            return "Needs Support"
        else:
            return "Steady"

clustering_service = LearnerClusteringService()
