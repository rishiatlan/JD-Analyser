#!/bin/bash
cd /opt/render/project/src
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1 