#!/bin/bash

REPO_RAW="https://raw.githubusercontent.com/FaizanMillionair/BFS-DEFENCE/main"
INSTALL_DIR="$(pwd)"

echo "[*] Checking for BFS DEFENCE updates..."

# Local version
LOCAL_VERSION=$(grep TOOL_VERSION main.py | cut -d'"' -f2)

# Remote version
LATEST_VERSION=$(curl -s $REPO_RAW/version.txt)

if [ -z "$LATEST_VERSION" ]; then
    echo "[-] Unable to check updates"
    exit 1
fi

if [ "$LOCAL_VERSION" = "$LATEST_VERSION" ]; then
    echo "[✓] Already up to date (v$LOCAL_VERSION)"
    exit 0
fi

echo "[+] Update found: v$LOCAL_VERSION → v$LATEST_VERSION"
read -p "Update now? (y/n): " ch
[ "$ch" != "y" ] && exit 0

echo "[*] Updating files..."
curl -s -o main.py $REPO_RAW/main.py
curl -s -o requirements.txt $REPO_RAW/requirements.txt
echo "$LATEST_VERSION" > version.txt

echo "[✓] Update completed. Run: bfs"
