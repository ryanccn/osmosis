#!/bin/sh

source ".venv/bin/activate"

echo "Building frontend..."

cd "osmosis/frontend"
yarn build

echo "Building Python project..."

cd "../.."
python -m build
