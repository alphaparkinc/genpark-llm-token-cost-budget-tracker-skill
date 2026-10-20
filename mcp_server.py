"""MCP Server for LLM Token Cost Budget Tracker.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import LlmTokenCostBudgetTracker

tracker = LlmTokenCostBudgetTracker(daily_budget_usd=50.0)

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "record_usage",
                                "description": "Record LLM token usage and check budget alert status",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "model": {"type": "string", "description": "LLM model identifier"},
                                        "input_tokens": {"type": "integer"},
                                        "output_tokens": {"type": "integer"},
                                        "agent_id": {"type": "string", "default": "default"}
                                    },
                                    "required": ["model", "input_tokens", "output_tokens"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                res = tracker.record_usage(
                    model=args.get("model"),
                    input_tokens=args.get("input_tokens", 0),
                    output_tokens=args.get("output_tokens", 0),
                    agent_id=args.get("agent_id", "default")
                )
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
