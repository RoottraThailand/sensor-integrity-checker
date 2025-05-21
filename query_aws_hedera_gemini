import requests
import json
import hashlib
import base64

TOPIC_ID = "0.0.6025735"
MODEL = "mistral"
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
    print("📤 Sending prompt to Ollama...")
    print("📜 Prompt being sent to LLM:\n", json.dumps(messages, indent=2))

    try:
        print("📁 Reaching Ollama client...")
        print("📤 About to send POST to Ollama...")

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": model, "messages": messages},
            timeout=180
        )

        print("📥 Ollama POST returned successfully")
        print("🔍 RAW Ollama output:\n", response.text)

        lines = response.text.strip().splitlines()
        full_content = ""

        for line in lines:
            try:
                parsed = json.loads(line)
                content = parsed.get("message", {}).get("content", "")
                full_content += content
            except json.JSONDecodeError:
                continue

        if full_content:
            print("\n🧐 Parsed and combined content:", full_content)
            return full_content
        else:
            return "⚠️ Could not extract message content."

    except Exception as e:
        print("❌ Ollama error:", e)
        print("🔧 Response (if any):", getattr(e.response, 'text', 'No response'))
        return "⚠️ LLM request failed."

def main():
    with open(DATA_FILE, "r") as f:
        sensor_data = json.load(f)

    sensor_preview = json.dumps(sensor_data, indent=2)[:1000]
    hash_status = verify_against_hedera(DATA_FILE, TOPIC_ID)

    messages = [
        {
            "role": "system",
            "content": "You are a data verification assistant. Use blockchain hash status and sensor data to answer the user's question clearly."
        },
        {
            "role": "user",
            "content": (
                f"Sensor data preview:\n{sensor_preview}\n\n"
                f"Hash verification result from Hedera:\n{hash_status}\n\n"
                "What can you infer from this? Is the data valid?"
            )
        }
    ]

    print("📡 LLM with memory active. Ask questions or type 'exit'.")

    while True:
        question = input("\n🧠 Ask Ollama: ")
        if question.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": question})
        reply = ask_ollama(messages)
        print("\n🤖 LLM Answer:\n", reply)

        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
