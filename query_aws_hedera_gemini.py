--- query_aws_hedera_gemini.py
@@
-import openai
-import os
+from openai import OpenAI
+import os

 # … your verify_against_hedera() code stays the same …

-def ask_openai(messages: list[dict], model: str = MODEL) -> str:
-    # initialize client with your secret
-    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
-
-    response = client.chat.completions.create(
-        model=model,
-        messages=messages,
-        max_tokens=500
-    )
-    return response.choices[0].message.content
+def ask_openai(messages: list[dict], model: str = MODEL) -> str:
+    # Load your API key and construct the new client
+    api_key = os.getenv("OPENAI_API_KEY")
+    if not api_key:
+        raise ValueError("OPENAI_API_KEY not set in your environment")
+
+    client = OpenAI(api_key=api_key)
+
+    # Use the new .chat.completions.create interface
+    response = client.chat.completions.create(
+        model=model,
+        messages=messages,
+        max_tokens=500,
+    )
+    return response.choices[0].message.content
