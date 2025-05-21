# streamlit_app.py (OpenAI version)

import json
import tempfile
import os
import streamlit as st
import openai

from query_aws_hedera_gemini_online import (
    verify_against_hedera,  # Hedera mirror-node lookup
    TOPIC_ID                # Hedera topic containing the hashes
)

# === API Key Setup ===
openai.api_key = st.secrets.get("openai_key") or os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Sensor Integrity Checker",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 Sensor Data Integrity Checker")
st.markdown(
    "Upload a sensor JSON file, verify its on-chain hash, and chat about the data — all in one place 🚀"
)

# === Chat Function Using OpenAI ===
def call_openai_llm(messages, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"❌ Error calling OpenAI: {e}"

# --- FILE UPLOAD -----------------------------------------------------------
uploaded = st.file_uploader("Upload sensor JSON", type="json")
if uploaded is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    # 1️⃣ Show a preview
    data = json.load(open(tmp_path))
    preview = json.dumps(data, indent=2)[:1000]
    st.subheader("📄 Data preview (first 1 000 chars)")
    st.code(preview, language="json")

    # 2️⃣ Verify on Hedera
    st.subheader("🔍 Blockchain integrity check")
    status = verify_against_hedera(tmp_path, TOPIC_ID)
    if status.startswith("✅"):
        st.success(status)
    else:
        st.error(status)

    # 3️⃣ LLM Q&A with OpenAI
    st.subheader("🤖 Ask anything about this file")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a data-verification assistant. Use blockchain hash status and "
                    "sensor data to answer clearly and helpfully."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Sensor data preview:\n{preview}\n\n"
                    f"Hash verification result:\n{status}\n\n"
                    "What can you infer from this? Is the data valid?"
                ),
            },
        ]

    prompt = st.text_input("Your question", placeholder="e.g. Does any reading look abnormal?")
    ask = st.button("Ask")
    if ask and prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Querying OpenAI..."):
            reply = call_openai_llm(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display convo
    for msg in st.session_state.messages[2:]:
        who = "assistant" if msg["role"] == "assistant" else "user"
        st.chat_message(who).markdown(msg["content"])

# --- SIDEBAR ---------------------------------------------------------------
st.sidebar.header("⚙️ Settings")
st.sidebar.info("This version uses OpenAI's cloud model (gpt-3.5-turbo). Make sure your key is set.")
