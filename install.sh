#!/bin/bash

echo "[*] Installing BFS DEFENCE (venv mode)..."

INSTALL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Detect Termux
if [ -d "/data/data/com.termux/files/usr" ]; then
    PLATFORM="termux"
    BIN_DIR="$HOME/bin"
    SHELL_RC="$HOME/.bashrc"
else
    PLATFORM="linux"
    BIN_DIR="/usr/local/bin"
    SHELL_RC="$HOME/.bashrc"
fi

# Check python
if ! command -v python3 >/dev/null 2>&1; then
    echo "[-] Python3 not found. Install python3 first."
    exit 1
fi

# Create venv
if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv "$INSTALL_DIR/venv"
fi

# Activate venv
source "$INSTALL_DIR/venv/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install requirements
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    pip install -r "$INSTALL_DIR/requirements.txt"
else
    echo "[-] requirements.txt not found"
    deactivate
    exit 1
fi

# Prepare bin directory
mkdir -p "$BIN_DIR"

# Create launcher (absolute paths only)
cat > bfs << EOF
#!/bin/bash
source "$INSTALL_DIR/venv/bin/activate"
python "$INSTALL_DIR/main.py"
EOF

chmod +x bfs

# Move launcher
if [ "$PLATFORM" = "linux" ]; then
    sudo mv bfs "$BIN_DIR/bfs"
else
    mv bfs "$BIN_DIR/bfs"
fi

deactivate

# Ensure PATH (Termux & safety)
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "export PATH=$BIN_DIR:\$PATH" >> "$SHELL_RC"
    PATH_UPDATED=1
else
    PATH_UPDATED=0
fi

echo
echo "[✓] BFS DEFENCE installed successfully"

if command -v bfs >/dev/null 2>&1; then
    echo "👉 Run tool using command: bfs"
else
    echo "⚠ Shell reload required"
    echo "👉 Close & reopen terminal, then run: bfs"
    echo "👉 Or run directly: $BIN_DIR/bfs"
fi
