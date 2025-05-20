// submit_hash.js

const {
  Client,
  TopicMessageSubmitTransaction,
  TopicId,
  PrivateKey,
  AccountId
} = require("@hashgraph/sdk");

// ✅ Optional if using environment variables
// require("dotenv").config();

// === Hedera Testnet Credentials ===
const operatorId = AccountId.fromString("0.0.5996080");
const operatorKey = PrivateKey.fromString("3030020100300706052b8104000a0422042068ab1571f096e23f936d66111b2c1d9dab2b83bbe68b80d7b6367b0b8f7ed4f2");

// === Topic ID from create_topic.js output ===
const topicId = TopicId.fromString("0.0.6025735");

// === Accept SHA256 hash from command line ===
const message = process.argv[2];
if (!message) {
  console.error("❌ No hash provided!");
  process.exit(1);
}

// === Main submission logic ===
async function main() {
  const client = Client.forTestnet().setOperator(operatorId, operatorKey);

  const submitTx = await new TopicMessageSubmitTransaction()
    .setTopicId(topicId)
    .setMessage(message)
    .execute(client);

  const receipt = await submitTx.getReceipt(client);
  console.log("✅ Hash submitted! Status:", receipt.status.toString());
}

main();
