#!/bin/sh

[ ! -f .venv/bin/activate ] && python -m venv .venv

. ".venv/bin/activate"

echo "Building frontend..."

cd "osmosis/frontend" || exit 

[ ! -e node_modules ] && yarn install

yarn build

echo "Building Python project..."

cd "../.." || exit

python -m pip freeze | grep -E ^build
[ $? -eq 1 ] && python -m pip install build

python -m build
