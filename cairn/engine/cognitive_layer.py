from dataclasses import dataclass
from cairn.domain.portfolio import Portfolio


@dataclass
class CognitiveInsight:
    why_it_might_be_wrong: list[str]
    confidence: float
    bias_flags: list[str]


class CognitiveLayer:

    def analyze(self, portfolio: Portfolio, recommendation: dict, metrics: dict):

        biases = []
        local_context = []

        allocation = metrics.get("allocation", {})
        worst = metrics.get("worst")
        best = metrics.get("best")

        title = recommendation.get("title", "")

        # --------------------
        # GLOBAL CONTEXT (STRICT, UNIQUE, NON-DUPLICATED)
        # --------------------
        global_context = [
            "Marché crypto fortement volatil",
            "Signaux court terme bruités"
        ]

        # --------------------
        # LOCAL CONTEXT (ONLY SPECIFIC SIGNALS)
        # --------------------

        if "BTC" in title:
            local_context.append("BTC dominance peut être stratégie macro volontaire")

        if "SOL" in title:
            local_context.append("ALT volatilité élevée → swings extrêmes fréquents")

        if worst and worst.pnl_pct < -5:
            local_context.append("Sous-performance peut être bruit statistique")

        btc_weight = allocation.get("BTC", 0)

        if btc_weight > 0.7:
            biases.append("concentration_bias")

        if worst and abs(worst.pnl_pct) < 10:
            biases.append("noise_sensitivity")

        # -------------------------
        # SIGNAL AMPLIFIER (IMPORTANT FIX)
        # -------------------------

        amplifier = 1.0

        # strong risk cases
        if worst and worst.pnl_pct < -8:
            amplifier += 0.25

        # strong concentration
        if btc_weight > 0.85:
            amplifier += 0.20

        # strong opportunity
        if best and best.pnl_pct > 7:
            amplifier += 0.15


        type_multiplier = 1.0

        rec_type = recommendation.get("type", "")

        if rec_type == "risk":
            type_multiplier = 1.1

        elif rec_type == "performance":
            type_multiplier = 0.95

        elif rec_type == "opportunity":
            type_multiplier = 1.05
        # --------------------
        # CONFIDENCE FIX (NON CONSTANTE)
        # --------------------

        signal_strength = 0.6
        context_stability = 0.75

        if worst and worst.pnl_pct < -10:
            signal_strength += 0.3

        if worst and worst.pnl_pct < -5:
            signal_strength += 0.1

        if btc_weight > 0.85:
            signal_strength += 0.2

        if "SOL" in title and worst and worst.pnl_pct < -8:
            signal_strength -= 0.15

        confidence = (signal_strength * context_stability) * amplifier * type_multiplier
        confidence = max(0.05, min(confidence, 0.95))

        # -------------------------
        # INTENT SEPARATION LAYER
        # -------------------------

        intent_shift = 0.0

        rec_type = recommendation.get("type", "")

        if rec_type == "risk":
            intent_shift = +0.08   # stronger urgency

        elif rec_type == "info":
            intent_shift = -0.05   # dampened confidence

        elif rec_type == "opportunity":
            intent_shift = +0.03
        # -------------------------
        # GLOBAL NORMALIZATION
        # -------------------------

        target_mean = 0.55

        confidence = (signal_strength * context_stability) * amplifier * type_multiplier

        # clamp
        confidence = confidence + intent_shift
        confidence = max(0.05, min(confidence, 0.95))

        # -------------------------
        # SOFT NORMALIZATION (FIX FINAL)
        # -------------------------

        drift = confidence - target_mean

        # only damp extreme drift, don't crush signal
        confidence = target_mean + (drift * 0.7)
        # -------------------------
        # ASYMMETRIC DAMPING (FINAL FIX)
        # -------------------------

        if confidence > 0.75:
            confidence = 0.75 + (confidence - 0.75) * 0.5

        elif confidence < 0.30:
            confidence = 0.30 + (confidence - 0.30) * 0.5

        return CognitiveInsight(
            why_it_might_be_wrong=global_context + local_context,
            confidence=confidence,
            bias_flags=biases
        )