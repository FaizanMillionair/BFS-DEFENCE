import requests
import uuid
import hashlib
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

SERVER_URL = "http://13.203.201.49:8000"
TOOL_VERSION = "1.0"

DEVICE_FILE = os.path.expanduser("~/.bfs_device_id")

# ================= DEVICE ID =================
def get_device_id():
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "r") as f:
            return f.read().strip()

    raw = str(uuid.uuid4())
    device_id = hashlib.sha256(raw.encode()).hexdigest()

    with open(DEVICE_FILE, "w") as f:
        f.write(device_id)

    return device_id

# ================= BANNER =================
def banner():
    art = r"""
   ██████╗ ███████╗███████╗     ██████╗ ███████╗███████╗███████╗███╗   ██╗ ██████╗███████╗
  ██╔══██╗██╔════╝██╔════╝    ██╔═══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝██╔════╝
  ██████╔╝█████╗  ███████╗    ██║   ██║█████╗  █████╗  █████╗  ██╔██╗ ██║██║     █████╗
  ██╔══██╗██╔══╝  ╚════██║    ██║   ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██║     ██╔══╝
  ██████╔╝██║     ███████║    ╚██████╔╝██║     ███████╗███████╗██║ ╚████║╚██████╗███████╗
  ╚═════╝ ╚═╝     ╚══════╝     ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝

                🛡️  BFS DEFENCE  🛡️
             💀  N A L A N D A  •  O S I N T  💀
    """
    for i, line in enumerate(art.split("\n")):
        print((Fore.CYAN if i % 2 == 0 else Fore.RED) + Style.BRIGHT + line)
        time.sleep(0.03)

    print(Fore.YELLOW + Style.BRIGHT + "\n   [ DEFENCE MODE : ACTIVE ]\n")

# ================= OUTPUT FORMAT =================
def pretty(resp):
    if not resp.get("success"):
        print(Fore.RED + "[-] Request failed / no data")
        return

    print(Fore.MAGENTA + Style.BRIGHT + "\n════════════════════════════════════════════")
    print(Fore.CYAN + Style.BRIGHT + "      PERSONAL DETAILS FIND")
    print(Fore.MAGENTA + Style.BRIGHT + "════════════════════════════════════════════\n")

    for i, rec in enumerate(resp.get("result", []), 1):
        print(Fore.YELLOW + Style.BRIGHT + f"[ RECORD {i} ]")
        print(Fore.CYAN + "-" * 45)
        for k, v in rec.items():
            if v:
                print(Fore.GREEN + f"{k:<15}" + Fore.WHITE + " : " + Fore.CYAN + str(v))
        print(Fore.CYAN + "-" * 45 + "\n")

    print(Fore.MAGENTA + Style.BRIGHT + "DETAILS FIND BY BFS DEFENCE OSINT")
    print(Fore.GREEN + Style.BRIGHT + "THANKS FOR PURCHASED\n")

# ================= MAIN =================
def main():
    banner()
    print(Fore.WHITE + f"Version: {TOOL_VERSION}\n")

    lic = input("Enter Licence Key: ").strip()
    did = get_device_id()

    try:
        v = requests.post(
            f"{SERVER_URL}/verify",
            json={"licence": lic, "device_id": did},
            timeout=15
        ).json()
    except:
        print(Fore.RED + "[-] Server not reachable")
        return

    if not v.get("status"):
        print(Fore.RED + "[-] Licence invalid / device mismatch")
        return

    print(Fore.GREEN + "[✓] Login successful")

    # ===== MAIN LOOP =====
    while True:
        print("\n[1] Phone Lookup")
        print("[2] Aadhaar Lookup")
        print("[0] Exit")

        ch = input("Choose option: ").strip()

        if ch == "0":
            print(Fore.YELLOW + "\nBye 👋")
            break

        if ch not in ("1", "2"):
            print(Fore.RED + "Invalid option")
            continue

        term = input("Enter value: ").strip()
        typ = "PHONE" if ch == "1" else "AADHAAR"

        try:
            r = requests.post(
                f"{SERVER_URL}/lookup",
                json={
                    "licence": lic,
                    "device_id": did,
                    "type": typ,
                    "term": term,
                    "version": TOOL_VERSION
                },
                timeout=30
            ).json()
        except:
            print(Fore.RED + "[-] Server error")
            continue

        pretty(r)

# ================= RUN =================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n[!] Tool closed by user 👋")
