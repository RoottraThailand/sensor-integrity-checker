@@ -18,25 +18,27 @@

import json
import tempfile

import streamlit as st
import os
import streamlit as st

# ✅ MUST be the first Streamlit command
st.set_page_config(
    page_title="Sensor Integrity Checker",
    page_icon="🔗",
    layout="centered"
)

# ✅ Debug print BEFORE other Streamlit functions
st.write("DEBUG: OpenAI key is", os.getenv("OPENAI_API_KEY"))

# Re-use your existing helpers 👇
from query_aws_hedera_gemini import (
    verify_against_hedera,  # Hedera mirror-node lookup
    ask_ollama,             # chat with local Ollama instance
    ask_ollama,             # chat with OpenAI or local Ollama instance
    MODEL,                  # default model name
    TOPIC_ID                # Hedera topic containing the hashes
)

st.set_page_config(
    page_title="Sensor Integrity Checker",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 Sensor Data Integrity Checker")
st.markdown(
    "Upload a sensor JSON file, verify its on-chain hash, and chat about the data — all in one place 🚀"
