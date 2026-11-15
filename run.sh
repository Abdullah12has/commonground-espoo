#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec uv run --project prometheus python -m uvicorn commonground_app.app:app --host 127.0.0.1 --port "${PORT:-8766}"
