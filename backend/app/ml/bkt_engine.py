"""
Bayesian Knowledge Tracing (BKT) Engine

Models student knowledge acquisition over a sequence of practice opportunities.
Parameters:
- P(L0): Prior probability student knows skill beforehand (default: 0.15)
- P(T): Transition probability of learning skill at step t (default: 0.20)
- P(G): Guess probability - answering correctly without knowing (default: 0.25)
- P(S): Slip probability - answering incorrectly despite knowing (default: 0.10)
"""

import math
from typing import Tuple, Dict, Any

MASTERY_THRESHOLD = 0.80  # 80% threshold required to unlock next topic

class BayesianKnowledgeTracer:
    def __init__(
        self,
        p_init: float = 0.15,
        p_transit: float = 0.20,
        p_guess: float = 0.25,
        p_slip: float = 0.10
    ):
        self.p_init = p_init
        self.p_transit = p_transit
        self.p_guess = p_guess
        self.p_slip = p_slip

    def update_mastery(
        self,
        p_known: float,
        is_correct: bool,
        hints_used: int = 0,
        response_time_sec: float = 15.0
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates posterior probability of knowledge P(L_t | obs)
        and predicts next state probability P(L_{t+1}).
        """
        p_l = max(0.01, min(0.99, p_known))
        
        # Adjust guess probability if student used hints (higher chance of assisted correct)
        eff_guess = self.p_guess
        if hints_used == 1:
            eff_guess = min(0.40, eff_guess + 0.15)
        elif hints_used >= 2:
            eff_guess = min(0.55, eff_guess + 0.30)

        # Fast response time (< 5s) on correct answer might reflect high certainty or guessing
        eff_slip = self.p_slip
        if response_time_sec < 4.0 and not is_correct:
            # Rushed response -> slightly higher slip weight
            eff_slip = min(0.20, eff_slip + 0.08)

        # 1. Bayesian Posterior Step: P(L_t | obs)
        if is_correct:
            numerator = p_l * (1.0 - eff_slip)
            denominator = numerator + ((1.0 - p_l) * eff_guess)
        else:
            numerator = p_l * eff_slip
            denominator = numerator + ((1.0 - p_l) * (1.0 - eff_guess))

        p_l_given_obs = numerator / max(1e-6, denominator)
        p_l_given_obs = max(0.01, min(0.99, p_l_given_obs))

        # 2. Transition Step: P(L_{t+1}) = P(L_t | obs) + (1 - P(L_t | obs)) * P(T)
        p_next = p_l_given_obs + ((1.0 - p_l_given_obs) * self.p_transit)
        p_next = round(max(0.01, min(0.99, p_next)), 4)

        is_mastered = p_next >= MASTERY_THRESHOLD

        telemetry = {
            "prior_p_known": round(p_known, 4),
            "effective_guess": round(eff_guess, 4),
            "effective_slip": round(eff_slip, 4),
            "posterior_p_known": round(p_l_given_obs, 4),
            "next_p_known": p_next,
            "mastery_percent": round(p_next * 100, 1),
            "is_mastered": is_mastered
        }

        return p_next, telemetry

    def select_next_difficulty(self, p_known: float, last_correct: bool) -> int:
        """
        Dynamically adjusts question difficulty (1 to 5) based on current BKT estimate.
        """
        if p_known < 0.30:
            return 1
        elif p_known < 0.55:
            return 2 if not last_correct else 3
        elif p_known < 0.75:
            return 3 if not last_correct else 4
        elif p_known < 0.85:
            return 4
        else:
            return 5

bkt_engine = BayesianKnowledgeTracer()
