import requests
import json
import hashlib
import base64
import openai
import os

TOPIC_ID = "0.0.6025735"
MODEL = "gpt-3.5-turbo"
DATA_FILE = "mock_sensor_data.json"

def verify_against_hedera(filepath, topic_id):
    with open(filepath, "rb") as f:
        local_hash = hashlib.sha256(f.read()).hexdigest()

    url = f"https://testnet.mirrornode.hedera.com/api/v1/topics/{topic_id}/messages"
    response = requests.get(url).json()

    on_chain_hashes = []
    for m in response['messages']:
        try:
            decoded = base64.b64decode(m['message']).decode('utf-8').strip()
            on_chain_hashes.append(decoded)
        except:
            continue

    if local_hash in on_chain_hashes:
        return f"✅ File is authentic — hash {local_hash} found on Hedera."
    else:
        return f"❌ File is NOT verified — hash {local_hash} not found on Hedera."

def ask_ollama(messages, model=MODEL):
    print("📤 Sending prompt to OpenAI...")
    print("📜 Prompt being sent to LLM:\n", json.dumps(messages, indent=2))

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=500
    )

    return response.choices[0].message.content
