#!/usr/bin/env bash
set -euo pipefail

# usage: ./switch_bluegreen.sh blue|green
TARGET=${1:-}

if [ "$TARGET" != "blue" ] && [ "$TARGET" != "green" ]; then
  echo "Usage: $0 blue|green"
  exit 1
fi

echo "Patching service selector to variant=$TARGET"
kubectl patch service aceest-service -p "{\"spec\":{\"selector\":{\"app\":\"aceest\",\"variant\":\"$TARGET\"}}}"

echo "Service updated."
