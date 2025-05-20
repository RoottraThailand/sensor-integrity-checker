
import boto3
import json
from openai import OpenAI

# === CONFIG ===
bucket_name = "datauploadgpt"
object_key = "mock_sensor_data.json"
model_name = "llama3:latest"

# === AWS S3 Download ===
print("🔄 Connecting to AWS S3...")
try:
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    sensor_data = json.loads(response["Body"].read())
    print("✅ S3 file loaded successfully.")
except Exception as e:
    print(f"❌ Error loading S3 file: {e}")
    exit()

# === Ollama Connect ===
print("🔄 Connecting to Ollama...")
try:
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
except Exception as e:
    print(f"❌ Ollama connection error: {e}")
    exit()

# === Query Loop ===
print("\n🧠 You can now ask questions about the farm sensor data.")
print("Type 'exit' to quit.\n")

while True:
    question = input("❓ Your question: ")
    if question.lower() in ['exit', 'quit']:
        print("👋 Exiting.")
        break

    data_sample = json.dumps(sensor_data[:10], indent=2) # Use only the first 10 rows of data

    prompt = f"""
You are analyzing the following 10 rows of farm sensor data.

Each record includes:
- CO2 (ppm)
- PM2.5 (ug/m3)
- Temperature (C)
- Humidity (%)

Data:
{data_sample}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        print(f"\n🟢 LLM Response:\n{answer}\n")

    except Exception as e:
        print(f"❌ LLM processing error: {e}")
