"""
run.py - Python Course Study Assistant Launcher
Team No.: 11 | Venue: MB306 | Theme E: Problem 21
Starts FastAPI backend on http://localhost:8000 serving both REST API and Frontend.
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "127.0.0.1")
    
    print("=" * 75)
    print("PYTHON COURSE STUDY ASSISTANT - DEMO READY")
    print("=" * 75)
    print(f"  • Frontend & REST API: http://localhost:{port}")
    print(f"  • Swagger API Docs:     http://localhost:{port}/docs")
    print(f"  • Team:                11 | Venue: MB306")
    print("=" * 75)
    
    uvicorn.run("backend.main:app", host=host, port=port, reload=False)
