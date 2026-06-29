def cognitive_bias_analysis(trader_id, metrics):
    biases = []

    if metrics["winrate"] > 0.7 and metrics["max_dd"] < -5:
        biases.append("martingale_risk")

    if metrics["leverage"] > 15:
        biases.append("over_leverage")

    if metrics["consistency"] < 0.4:
        biases.append("unstable_equity_curve")

    if metrics["avg_pnl"] > 2 and metrics["winrate"] < 0.55:
        biases.append("low_frequency_luck_bias")

    return biases


def why_it_might_be_wrong(trader_id, metrics):
    reasons = []

    if metrics["winrate"] > 0.7:
        reasons.append("High winrate may be due to short sample size")

    if metrics["max_dd"] < -5:
        reasons.append("Hidden tail risk not visible in average PnL")

    if metrics["leverage"] > 10:
        reasons.append("Performance may be leverage-dependent and unstable")

    if metrics["consistency"] < 0.5:
        reasons.append("Equity curve may not generalize across regimes")

    return reasons

def detect_biases(metrics):
    biases = []

    if metrics["winrate"] > 0.75 and metrics["max_dd"] < -6:
        biases.append("hidden_tail_risk")

    if metrics["leverage"] > 15:
        biases.append("over_leveraged_strategy")

    if metrics["consistency"] < 0.4:
        biases.append("unstable_equity_curve")

    if metrics["avg_pnl"] > 1 and metrics["winrate"] < 0.5:
        biases.append("luck_based_returns")

    return biases


def why_it_might_be_wrong(metrics):
    reasons = []

    if metrics["winrate"] > 0.7:
        reasons.append("Winrate may be inflated by short sample size")

    if metrics["max_dd"] < -5:
        reasons.append("Tail risk may not be visible in average returns")

    if metrics["leverage"] > 10:
        reasons.append("High leverage may not scale safely")

    if metrics["consistency"] < 0.5:
        reasons.append("Performance may not generalize across market regimes")

    return reasons