#!/bin/sh

[ ! -f .venv/bin/activate ] && python -m venv .venv

. ".venv/bin/activate"

echo "Building frontend..."

cd "osmosis/frontend" || exit

[ ! -e node_modules ] && yarn install

yarn run build

echo "Building Python project..."

cd "../.." || exit

python -c "import build" 2> /dev/null || python -m pip install build

python -m build
