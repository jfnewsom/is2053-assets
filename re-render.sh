#!/bin/bash
cd "$(dirname "$0")"

echo "Re-rendering labs..."
for f in pages/labs/json/lab-*.json; do
    python3 render_lab.py "$f" && echo "  ✓ $f"
done

echo ""
echo "Re-rendering BookEx pages..."
for f in pages/bookex/json/bookex-ch*.json; do
    python3 render_bookex.py "$f" && echo "  ✓ $f"
done

echo ""
echo "Done. Push via GitHub Desktop."
