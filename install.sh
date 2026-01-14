#!/bin/bash
set -e

echo "[*] Installing BFS DEFENCE (venv mode)..."

# Check python
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 not found"
    exit 1
fi

# Create venv
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install launcher
sudo tee /usr/local/bin/bfs > /dev/null << 'EOF'
#!/bin/bash
source "$(pwd)/venv/bin/activate"
python "$(pwd)/main.py"
EOF

sudo chmod +x /usr/local/bin/bfs

deactivate

echo
echo "[✓] BFS DEFENCE installed successfully"
echo "Run tool using command: bfs"
