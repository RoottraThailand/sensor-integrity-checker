import os
from hashlib import sha256
from hedera import (
    Client, PrivateKey, AccountId,
    TopicCreateTransaction, TopicMessageSubmitTransaction
)

# === Replace these with your Hedera Testnet credentials ===
ACCOUNT_ID = AccountId.fromString("0.0.YOUR_ID_HERE")
PRIVATE_KEY = PrivateKey.fromString("302e...YOUR_PRIVATE_KEY")

# === Your mock data file path ===
DATA_FILE = "mock_data.json"  # Update this to your AWS-downloaded file

# === Connect to Hedera Testnet ===
client = Client.forTestnet()
client.setOperator(ACCOUNT_ID, PRIVATE_KEY)

# === Step 1: Hash your data ===
with open(DATA_FILE, "rb") as f:
    data = f.read()
    data_hash = sha256(data).hexdigest()

print(f"SHA256 Hash: {data_hash}")

# === Step 2: Create a new topic (one-time) ===
topic_tx = TopicCreateTransaction().setMemo("RootTra dMRV Data Hash").execute(client)
topic_receipt = topic_tx.getReceipt(client)
topic_id = topic_receipt.topicId
print(f"✅ Created Topic ID: {topic_id}")

# === Step 3: Submit the hash ===
submit_tx = TopicMessageSubmitTransaction()\
    .setTopicId(topic_id)\
    .setMessage(data_hash)\
    .execute(client)

submit_receipt = submit_tx.getReceipt(client)
print("✅ Hash submitted to Hedera testnet.")
