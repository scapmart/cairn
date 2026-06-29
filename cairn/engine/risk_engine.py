import math


class EquityRiskEngine:

    def _returns(self, curve):
        if len(curve) < 2:
            return []

        returns = []

        for i in range(1, len(curve)):
            prev = curve[i - 1]
            curr = curve[i]

            if prev <= 0:
                continue

            returns.append((curr - prev) / prev)

        return returns

    def max_drawdown(self, curve):
        if not curve:
            return 0

        peak = curve[0]
        max_dd = 0

        for x in curve:
            peak = max(peak, x)
            dd = (peak - x) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)

        return max_dd * 100

    def volatility(self, curve):
        returns = self._returns(curve)

        if not returns:
            return 0

        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / len(returns)

        return math.sqrt(variance)

    def sharpe_proxy(self, curve):
        returns = self._returns(curve)

        if not returns:
            return 0

        mean = sum(returns) / len(returns)
        vol = self.volatility(curve)

        if vol == 0:
            return 0

        sharpe = mean / vol

        return max(-2, min(sharpe, 2))

    def streak_risk(self, curve):
        if len(curve) < 2:
            return 0

        max_loss_streak = 0
        current = 0

        for i in range(1, len(curve)):
            if curve[i] < curve[i - 1]:
                current += 1
                max_loss_streak = max(max_loss_streak, current)
            else:
                current = 0

        return min(max_loss_streak / max(len(curve), 1), 1.0)

    def all(self, curve):
        return {
            "sharpe": self.sharpe_proxy(curve),
            "volatility": self.volatility(curve),
            "streak": self.streak_risk(curve),
            "max_dd": self.max_drawdown(curve),
        }