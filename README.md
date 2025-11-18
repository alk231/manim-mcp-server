# Manim MCP Server

![Manim MCP Demo](Demo-manim-mcp.gif)

## Overview

A Model Context Protocol (MCP) server that executes Manim animation code and returns generated videos. This server allows AI assistants like Claude to dynamically generate mathematical animations using Manim.

## Features

- ✨ Execute Manim Python scripts via MCP
- 📁 Automatic media folder management
- 🧹 Cleanup tools for temporary files
- ⚙️ Configurable via environment variables
- 🚀 Compatible with FastMCP Cloud

## Quick Start with FastMCP Cloud

This server is optimized for deployment on FastMCP Cloud:

1. Fork this repository
2. Deploy to FastMCP Cloud using the repository URL
3. The server will be automatically configured using `pyproject.toml`

## Local Installation

### Prerequisites

- Python 3.11+
- Manim (Community Edition)
- pip or uv package manager

### Install Dependencies
```bash
pip install -e .
```

Or using uv (faster):
```bash
uv pip install -e .
```

### Run the Server
```bash
python src/manim_server.py
```

## Integration with Claude Desktop

Add to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "manim-server": {
      "command": "python",
      "args": ["/absolute/path/to/manim-mcp-server/src/manim_server.py"],
      "env": {
        "MANIM_EXECUTABLE": "manim"
      }
    }
  }
}
```

### Finding Paths

**Windows (PowerShell):**
```powershell
(Get-Command python).Source
```

**Linux/macOS:**
```bash
which python
```

## Available Tools

### `execute_manim_code`
Executes Manim animation code and generates video output.

**Parameters:**
- `manim_code` (str): Python code containing Manim scene definition

**Returns:**
- Dictionary with status, message, and output details

### `cleanup_manim_temp_dir`
Cleans up temporary Manim output directory.

**Parameters:**
- `directory` (str): Path to directory to clean up

**Returns:**
- Dictionary with status and message

## Example Usage
```python
from manim import *

class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.wait()
```

## Project Structure
```
manim-mcp-server/
├── src/
│   ├── manim_server.py    # Main MCP server
│   └── media/             # Output directory
├── pyproject.toml         # Project configuration
├── README.md              # Documentation
└── LICENSE.txt            # MIT License
```

## Configuration

Environment variables:
- `MANIM_EXECUTABLE`: Path to Manim executable (default: "manim")

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature-name`
5. Open a pull request

## License

MIT License - see LICENSE.txt for details

## Credits

- Created by **[abhiemj](https://github.com/abhiemj)**
- Adapted for FastMCP Cloud by the community
- Featured in [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)
- Thanks to [Manim Community](https://www.manim.community/)

## Connect

Instagram: [@aiburner_official](https://www.instagram.com/aiburner_official)