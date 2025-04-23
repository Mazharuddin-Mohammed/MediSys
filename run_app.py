#!/usr/bin/env python3
"""
MediSys Hospital Management System - Application Runner

This script launches both the C++ backend and Python frontend components of the
MediSys application. It handles process management, environment setup, and ensures
proper shutdown of all components when the application exits.

Author: Mazharuddin Mohammed
"""

import sys
import os
import subprocess
import time

# Add the build directory to the Python path
build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "build")
sys.path.append(build_dir)

# Start the backend
backend_process = subprocess.Popen(
    [os.path.join(build_dir, "medisys_main")],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
print("Backend started with PID:", backend_process.pid)

# Give the backend a moment to start
time.sleep(1)

# Set the Python path for the frontend
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src/frontend/python")
os.environ["PYTHONPATH"] = build_dir + ":" + frontend_dir + ":" + os.environ.get("PYTHONPATH", "")
print("PYTHONPATH:", os.environ["PYTHONPATH"])

# Start the frontend
try:
    frontend_process = subprocess.run(
        [sys.executable, "src/frontend/python/main.py"],
        check=True
    )
except subprocess.CalledProcessError as e:
    print(f"Frontend exited with error code {e.returncode}")
except KeyboardInterrupt:
    print("Frontend interrupted by user")
finally:
    # Terminate the backend when the frontend exits
    print("Terminating backend...")
    backend_process.terminate()
    try:
        backend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Backend did not terminate gracefully, killing...")
        backend_process.kill()

    print("Application shutdown complete")
