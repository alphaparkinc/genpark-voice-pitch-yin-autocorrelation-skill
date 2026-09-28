import sys
import json
from client import VoicePitchYINEngine

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-voice-pitch-yin-autocorrelation-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "detect_pitch",
                    "description": "Detect fundamental frequency (F0) from mono audio PCM samples using YIN algorithm",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "signal": {"type": "array", "items": {"type": "number"}},
                            "sample_rate": {"type": "integer", "default": 16000},
                            "min_freq": {"type": "number", "default": 50.0},
                            "max_freq": {"type": "number", "default": 500.0}
                        },
                        "required": ["signal"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "detect_pitch":
            yin = VoicePitchYINEngine(
                sample_rate=args.get("sample_rate", 16000),
                min_freq=args.get("min_freq", 50.0),
                max_freq=args.get("max_freq", 500.0)
            )
            data = yin.detect_pitch(args.get("signal", []))
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
