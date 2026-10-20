"""LLM Token Cost Budget Tracker.
100% Python Standard Library.
"""
import time

class LlmTokenCostBudgetTracker:
    """Multi-model token cost budget ledger and burn rate forecaster."""

    MODEL_PRICING_PER_1M = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku": {"input": 0.80, "output": 4.00},
        "deepseek-v3": {"input": 0.14, "output": 0.28},
    }

    def __init__(self, daily_budget_usd: float = 50.0):
        self.daily_budget = daily_budget_usd
        self.ledger = []

    def record_usage(self, model: str, input_tokens: int, output_tokens: int, agent_id: str = "default") -> dict:
        pricing = self.MODEL_PRICING_PER_1M.get(model, {"input": 2.00, "output": 8.00})
        cost_input = (input_tokens / 1_000_000.0) * pricing["input"]
        cost_output = (output_tokens / 1_000_000.0) * pricing["output"]
        total_cost = round(cost_input + cost_output, 6)

        entry = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": total_cost
        }
        self.ledger.append(entry)

        total_spent = sum(e["cost_usd"] for e in self.ledger)
        budget_pct = (total_spent / self.daily_budget) * 100.0 if self.daily_budget > 0 else 100.0

        alert_level = "NORMAL"
        if budget_pct >= 100.0:
            alert_level = "EXCEEDED"
        elif budget_pct >= 90.0:
            alert_level = "CRITICAL_90"
        elif budget_pct >= 80.0:
            alert_level = "WARNING_80"

        return {
            "recorded_cost_usd": total_cost,
            "cumulative_cost_usd": round(total_spent, 6),
            "budget_limit_usd": self.daily_budget,
            "budget_used_percentage": round(budget_pct, 2),
            "alert_level": alert_level,
            "total_requests": len(self.ledger)
        }
