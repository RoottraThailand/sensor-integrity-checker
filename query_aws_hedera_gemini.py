# query_aws_hedera_gemini.py

import os
import requests
import json
import hashlib
import base64
import openai

# ── CONFIG ────────────────────────────────────────────────────────────────────

# Hedera topic on testnet containing your sensor‐data hashes
TOPIC_ID   = "0.0.6025735"

# A currently supported OpenAI chat model
MODEL      = "gpt-3.5-turbo"

# ── FILE HASH VERIFICATION ─────────────────────────────────────────────────────

def verify_against_hedera(filepath: str, topic_id: str) -> str:
    # compute local SHA-256
    with open(filepath, "rb") as f:
        local_hash = hashlib.sha256(f.read()).hexdigest()

    # fetch all messages from Hedera mirror node
    url = f"https://testnet.mirrornode.hedera.com/api/v1/topics/{topic_id}/messages"
    response = requests.get(url).json()

    on_chain_hashes = []
    for msg in response.get("messages", []):
        try:
            decoded = base64.b64decode(msg["message"]).decode("utf-8").strip()
            on_chain_hashes.append(decoded)
        except Exception:
            continue

    if local_hash in on_chain_hashes:
        return f"✅ File is authentic — hash {local_hash} found on Hedera."
    else:
        return f"❌ File is NOT verified — hash {local_hash} not found on Hedera."

# ── CHAT WITH OPENAI ────────────────────────────────────────────────────────────

def ask_ollama(messages: list[dict], model: str = MODEL) -> str:
    # initialize client with your secret
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content
