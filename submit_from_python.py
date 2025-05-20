import hashlib
import subprocess

def hash_and_submit_to_hedera(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
        hash_hex = hashlib.sha256(data).hexdigest()

    print("🧠 SHA256 Hash:", hash_hex)

    # Run the Node.js script to submit
    subprocess.run(["node", "submit_hash.js", hash_hex])

# Update with the path to your mock data file
hash_and_submit_to_hedera("mock_sensor_data.json")
