#!/bin/bash
set -e  # Exit on error
cd /opt/render/project/src
export PYTHONPATH=/opt/render/project/src
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 --log-level info 