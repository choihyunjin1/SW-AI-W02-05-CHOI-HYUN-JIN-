#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting AlgoViz Mac App Build Process..."

# 1. Clean previous builds
rm -rf build dist *.spec

# 2. Run PyInstaller
# --name: Name of the output app
# --onefile: Bundle everything into a single executable (inside the .app)
# --windowed: No terminal window
# --add-data: Include the '원본 폴더' containing algorithm scripts
echo "📦 Packaging with PyInstaller..."
pyinstaller --name "AlgoViz" \
            --windowed \
            --add-data "원본 폴더:원본 폴더" \
            launcher.py

echo "✅ Build Complete!"
echo "📂 Locate your app in: $(pwd)/dist/AlgoViz.app"
