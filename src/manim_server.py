import subprocess
import tempfile
import os
import shutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

MANIM_EXECUTABLE = os.getenv(
    "C:/Users/DELL/AppData/Local/Programs/Python/Python311/Scripts/manim.exe",
    "C:/Users/DELL/AppData/Local/Programs/Python/Python311/python.exe",
)

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(BASE_DIR, exist_ok=True)


@mcp.tool()
def execute_manim_code(manim_code: str) -> str:
    tmpdir = os.path.join(BASE_DIR, "manim_tmp")
    os.makedirs(tmpdir, exist_ok=True)

    script_path = os.path.join(tmpdir, "scene.py")

    try:
        with open(script_path, "w") as script_file:
            script_file.write(manim_code)

        result = subprocess.run(
            [MANIM_EXECUTABLE, "-m", "manim", "-p", script_path],
            capture_output=True,
            text=True,
            cwd=tmpdir,
        )

        if result.returncode == 0:
            return "Execution successful. Video generated."
        else:
            return f"Execution failed: {result.stderr}"

    except Exception as e:
        return f"Error during execution: {str(e)}"


@mcp.tool()
def cleanup_manim_temp_dir(directory: str) -> str:
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            return f"Cleanup successful for directory: {directory}"
        else:
            return f"Directory not found: {directory}"
    except Exception as e:
        return f"Failed to clean up directory: {directory}. Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="http",host="0.0.0.0",port=int(os.getenv("PORT", 8000))
)
