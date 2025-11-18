# src/manim_server.py
import os
import subprocess
import shutil
from pathlib import Path
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Manim Server")

# Configuration
MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")
BASE_DIR = Path(__file__).parent / "media"
BASE_DIR.mkdir(exist_ok=True)


@mcp.tool()
def execute_manim_code(manim_code: str) -> dict:
    """
    Execute Manim animation code and generate video output.

    Args:
        manim_code: Python code containing Manim scene definition

    Returns:
        Dictionary with status, message, and output directory or error details

    Note: Keep scenes simple for lightweight environment. Avoid heavy LaTeX rendering.
    """
    tmpdir = BASE_DIR / "manim_tmp"
    tmpdir.mkdir(exist_ok=True)
    script_path = tmpdir / "scene.py"

    try:
        # Write the Manim code to file
        script_path.write_text(manim_code, encoding="utf-8")

        # Execute Manim CLI to render the scene
        cmd = [
            MANIM_EXECUTABLE,
            str(script_path),
            "--format",
            "mp4",
            "-qk",  # Medium quality, render last frame
        ]

        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(tmpdir), timeout=120
        )

        if result.returncode == 0:
            return {
                "status": "success",
                "message": "Animation rendered successfully",
                "output_dir": str(tmpdir),
                "stdout": result.stdout,
            }
        else:
            return {
                "status": "error",
                "message": "Manim execution failed",
                "stderr": result.stderr,
                "stdout": result.stdout,
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Execution timed out (exceeded 120 seconds)",
        }
    except Exception as e:
        return {"status": "error", "message": f"Unexpected error: {str(e)}"}


@mcp.tool()
def cleanup_manim_temp_dir(directory: str) -> dict:
    """
    Clean up temporary Manim output directory.

    Args:
        directory: Path to directory to clean up

    Returns:
        Dictionary with status and message
    """
    try:
        dir_path = Path(directory)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            return {
                "status": "success",
                "message": f"Successfully cleaned up: {directory}",
            }
        return {"status": "warning", "message": f"Directory not found: {directory}"}
    except Exception as e:
        return {"status": "error", "message": f"Cleanup failed: {str(e)}"}


# Run the server
if __name__ == "__main__":
    mcp.run(transport="sse")
