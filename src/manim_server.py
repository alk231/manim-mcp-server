# src/manim_server.py
import os
import subprocess
import shutil
from fastapi import FastAPI
import uvicorn
from mcp.server.fastmcp import FastMCP

mcp = FastMCP()

MANIM_EXECUTABLE = os.getenv("MANIM_EXECUTABLE", "manim")  # in container use "manim"
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
os.makedirs(BASE_DIR, exist_ok=True)


@mcp.tool()
def execute_manim_code(manim_code: str) -> str:
    """
    Write the provided python code to a scene file and run manim.
    Returns success message or stderr on failure.
    Note: keep scenes simple for 'lite' environment.
    """
    tmpdir = os.path.join(BASE_DIR, "manim_tmp")
    os.makedirs(tmpdir, exist_ok=True)
    script_path = os.path.join(tmpdir, "scene.py")

    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(manim_code)

        # Use manim CLI to render scene.py — default config
        cmd = [MANIM_EXECUTABLE, script_path, "--format", "mp4", "-qk"]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=tmpdir, timeout=120)

        if result.returncode == 0:
            return {"status": "ok", "message": "Execution successful", "output_dir": tmpdir}
        else:
            return {"status": "error", "stderr": result.stderr}

    except subprocess.TimeoutExpired:
        return {"status": "error", "stderr": "Execution timed out"}
    except Exception as e:
        return {"status": "error", "stderr": str(e)}


@mcp.tool()
def cleanup_manim_temp_dir(directory: str) -> str:
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            return f"Cleanup successful for: {directory}"
        return f"Directory not found: {directory}"
    except Exception as e:
        return f"Cleanup error: {str(e)}"


# FastAPI wrapper + health endpoint
app = FastAPI()
mcp.mount_to_fastapi(app)


@app.get("/mcp/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
