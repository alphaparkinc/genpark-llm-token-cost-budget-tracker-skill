"""Example usage for LLM Token Cost Budget Tracker."""
from client import LlmTokenCostBudgetTracker
import json

tracker = LlmTokenCostBudgetTracker(daily_budget_usd=25.0)

# Simulate requests
res1 = tracker.record_usage("gpt-4o", input_tokens=150_000, output_tokens=30_000, agent_id="researcher")
print("Usage 1:", json.dumps(res1, indent=2))

res2 = tracker.record_usage("claude-3-5-sonnet", input_tokens=500_000, output_tokens=120_000, agent_id="coder")
print("Usage 2:", json.dumps(res2, indent=2))
