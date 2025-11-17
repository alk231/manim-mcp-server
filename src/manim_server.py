import subprocess
import os
import shutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

# On Railway/Docker, the manim executable is just "manim"
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(BASE_DIR, exist_ok=True)


# -------------------- MANIM EXECUTION TOOL --------------------
@mcp.tool()
def execute_manim_code(manim_code: str) -> str:
    """Runs user-provided Manim code and generates a video."""

    tmpdir = os.path.join(BASE_DIR, "manim_tmp")
    os.makedirs(tmpdir, exist_ok=True)

    script_path = os.path.join(tmpdir, "scene.py")

    try:
        with open(script_path, "w") as f:
            f.write(manim_code)

        # Run manim (Linux-friendly)
        result = subprocess.run(
            [MANIM_EXECUTABLE, "-p", script_path],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )

        if result.returncode == 0:
            return f"Execution successful. Video saved in: {tmpdir}"
        else:
            return f"Execution failed:\n{result.stderr}"

    except Exception as e:
        return f"Error during execution: {str(e)}"


# -------------------- CLEANUP TOOL --------------------
@mcp.tool()
def cleanup_manim_temp_dir(directory: str) -> str:
    """Deletes the Manim temp directory."""
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            return f"Cleanup successful for: {directory}"
        return f"Directory not found: {directory}"
    except Exception as e:
        return f"Cleanup error: {str(e)}"


# -------------------- MCP SERVER START --------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))

    mcp.run(
        transport="streamable-http",   # REQUIRED for HTTP servers
        host="0.0.0.0",
        port=port
    )
