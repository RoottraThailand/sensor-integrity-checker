### Updated streamlit_app.py
```python
# streamlit_app.py
"""
A quick Streamlit front-end that wraps your existing verification + LLM logic
for a minimum-viable product (MVP). It lets a user:
  • upload a sensor-data JSON file
  • see a prettified preview
  • verify the file hash on Hedera
  • chat with OpenAI about that data
"""
import os
import json
import tempfile
import streamlit as st

# Must be the very first Streamlit command to work properly
st.set_page_config(
    page_title="Sensor Integrity Checker",
    page_icon="🔗",
    layout="centered"
)

# Debug print BEFORE any other Streamlit calls
st.write("DEBUG: OpenAI key is", os.getenv("OPENAI_API_KEY"))

# Import your helper functions
from query_aws_hedera_gemini import (
    verify_against_hedera,  # Hedera mirror-node lookup
    ask_openai,             # chat with OpenAI
    MODEL,                  # default model name
    TOPIC_ID                # Hedera topic containing the hashes
)

# App header
st.title("🔗 Sensor Data Integrity Checker")
st.markdown(
    "Upload a sensor JSON file, verify its on-chain hash, and chat about the data — all in one place 🚀"
)

# --- FILE UPLOAD -----------------------------------------------------------
uploaded = st.file_uploader("Upload sensor JSON", type="json")
if uploaded is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    # 1️⃣ Show a preview
    data = json.load(open(tmp_path))
    preview = json.dumps(data, indent=2)[:1000]
    st.subheader("📄 Data preview (first 1 000 chars)")
    st.code(preview, language="json")

    # 2️⃣ Verify on Hedera
    st.subheader("🔍 Blockchain integrity check")
    status = verify_against_hedera(tmp_path, TOPIC_ID)
    if status.startswith("✅"):
        st.success(status)
    else:
        st.error(status)

    # 3️⃣ LLM Q&A
    st.subheader("🤖 Ask anything about this file")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": (
                "You are a data-verification assistant. Use blockchain hash status and"
                " sensor data to answer clearly."
            )},
            {"role": "user", "content": (
                f"Sensor data preview:\n{preview}\n\n"
                f"Hash verification result:\n{status}\n\n"
                "What can you infer from this? Is the data valid?"
            )},
        ]

    prompt = st.text_input("Your question", placeholder="e.g. Does any reading look abnormal?")
    ask = st.button("Ask")
    if ask and prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Thinking…"):
            reply = ask_openai(st.session_state.messages, model=st.session_state.get("model_name", MODEL))
        st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display conversation
    for msg in st.session_state.messages[2:]:
        who = "assistant" if msg["role"] == "assistant" else "user"
        st.chat_message(who).markdown(msg["content"])

# --- SIDEBAR ---------------------------------------------------------------
st.sidebar.header("⚙️ Settings")
st.sidebar.text_input("LLM model", value=MODEL, key="model_name")
st.sidebar.info("Make sure your OpenAI key is set in Secrets and that you have internet access.")
