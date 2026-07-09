#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

exec > >(tee -a backend_launcher.log) 2>&1

echo ""
echo "=== Starting backend: $(date) ==="

if [ -n "${PYTHON_BIN:-}" ]; then
  PYTHON_BIN="$PYTHON_BIN"
elif [ -x "/usr/local/bin/python3" ]; then
  PYTHON_BIN="/usr/local/bin/python3"
elif [ -x "/opt/homebrew/bin/python3" ]; then
  PYTHON_BIN="/opt/homebrew/bin/python3"
else
  PYTHON_BIN="python3"
fi

echo "Using Python: $("$PYTHON_BIN" --version) at $PYTHON_BIN"

if [ -f ".venv/bin/python" ]; then
  if ! .venv/bin/python -c 'import sys; raise SystemExit(sys.version_info < (3, 10))'; then
    backup=".venv.python-too-old.$(date +%Y%m%d%H%M%S)"
    echo "Existing .venv uses an unsupported Python version. Moving it to $backup"
    mv .venv "$backup"
  fi
fi

if [ ! -f ".venv/bin/activate" ]; then
  "$PYTHON_BIN" -m venv .venv
fi

source .venv/bin/activate
echo "Active venv Python: $(python --version)"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd backend
exec python -m uvicorn main_API:app --host 127.0.0.1 --port 8000
