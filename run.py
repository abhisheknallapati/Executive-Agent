"""
Application Entrypoint for Executive Productivity Agent — AIONOS
Starts FastAPI server serving REST APIs and Executive Dashboard UI.
"""

import uvicorn
import socket
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.db import init_db
from backend.agents.pipeline import ExecutivePipeline

def find_available_port(preferred_port=8000, max_attempts=10):
    for offset in range(max_attempts):
        port = preferred_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    return preferred_port

if __name__ == "__main__":
    print("=" * 70)
    print("  EXECUTIVE PRODUCTIVITY AGENT — AIONOS")
    print("  User: Arjun Malhotra — VP Sales (Veridian Corp)")
    print("  Anchor Period: 21–25 September 2026 (Simulated Date: 23 Sep 2026)")
    print("=" * 70)
    
    # Pre-populate database
    init_db()
    pipeline = ExecutivePipeline()
    actions, cal, brief = pipeline.run_full_pipeline()
    
    port = find_available_port(8000)
    
    print(f"[OK] Pipeline initialized: {len(actions)} actions extracted across multi-modal sources.")
    print(f"[OK] Executive dashboard ready at: http://localhost:{port}")
    print("=" * 70)
    
    uvicorn.run("backend.main:app", host="127.0.0.1", port=port, log_level="info")
