# genpark-voice-pitch-yin-autocorrelation-skill

> Fundamental frequency (F0) pitch detector utilizing the YIN algorithm and cumulative mean normalized difference function.

Part of the **GenPark AI Agent Skills Matrix**. Production-ready, zero external dependencies, native Python 3.9+ standard library.

## Architecture

```mermaid
flowchart TD
    A[Audio Input Signal] --> B[Processing Engine]
    B --> C[DSP Core Operations]
    C --> D[Feature / Filtered Result]
    D --> E[MCP Protocol Endpoint]
```

## Features
- **Zero Third-Party Dependencies**: Pure Python standard library (`math`, `cmath`).
- **High Precision DSP**: Optimized algorithms with sub-sample interpolation and direct form structures.
- **Native MCP Protocol Support**: Integrated JSON-RPC 2.0 stdio server ready for Claude Desktop, Cursor, and Windsurf.

## Installation

```bash
pip install genpark-voice-pitch-yin-autocorrelation-skill
```

Or clone directly:

```bash
git clone https://github.com/alphaparkinc/genpark-voice-pitch-yin-autocorrelation-skill.git
cd genpark-voice-pitch-yin-autocorrelation-skill
python example_usage.py
```

## Quick Start

```python
from client import *
# Refer to example_usage.py for end-to-end execution
```

## Model Context Protocol (MCP) Setup

Add to your `claude_desktop_config.json` or `cursor.json`:

```json
{
  "mcpServers": {
    "genpark-voice-pitch-yin-autocorrelation-skill": {
      "command": "python",
      "args": ["-m", "genpark-voice-pitch-yin-autocorrelation-skill.mcp_server"]
    }
  }
}
```

## License
MIT License. Copyright (c) 2026 AlphaPark Inc. & Alpha-Park.
