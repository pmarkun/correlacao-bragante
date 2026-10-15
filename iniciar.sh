#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
exec uv run --offline python -m http.server 8765 --bind 127.0.0.1
