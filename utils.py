import json
import os
import uuid

def save_conversation(conversation):
    os.makedirs("conversations",exist_ok=True)
    filepath = f"conversations/{conversation['id']}.json"
    with open(filepath, "w") as f:
        json.dump(conversation, f)

def load_conversations():
    conversations = []
    for file in os.listdir("conversations"):
        if file.endswith(".json"):
            with open(f"conversations/{file}", "r") as f:
                data = json.load(f)
                conversations.append(data)
    return conversations

def create_new_chat():
    return {
        "id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": []
    }

def load_specific_chat(chat_id):
    filepath = f"conversations/{chat_id}.json"
    with open(filepath, "r") as f:
        return json.load(f)