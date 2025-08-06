import os
import json
import requests
import re
from actions import handle_local_commands
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API = os.getenv("OLLAMA_API")
MODEL = os.getenv("MODEL")

# Load memory
def load_memory():
    if os.path.exists("memory.json"):
        with open("memory.json") as f:
            return json.load(f)
    return {}

# Save memory
def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

# Load context
def load_context():
    if not os.path.exists("context.json") or os.stat("context.json").st_size == 0:
        return []
    with open("context.json", "r") as f:
        return json.load(f)

# Save context
def save_context(context):
    with open("context.json", "w") as f:
        json.dump(context, f, indent=2)

# Extract name from "call me XYZ"
def extract_name(text):
    match = re.search(r"\bcall me\s+([A-Za-z0-9_]{2,20})\b", text, re.IGNORECASE)
    return match.group(1) if match else None

# Update memory
def update_memory_from_input(user_input, memory):
    name = extract_name(user_input)
    if name:
        memory["name"] = name

    if "short replies" in user_input.lower():
        memory["style"] = "short"
    elif "detailed answers" in user_input.lower():
        memory["style"] = "detailed"

    keywords = {
        "i like": "likes",
        "my project is": "project",
        "i am working on": "project",
        "my hobby is": "hobby",
        "i hate": "dislikes"
    }

    for key, tag in keywords.items():
        if key in user_input.lower():
            value = user_input.lower().split(key)[-1].strip().split('.')[0]
            memory[tag] = value

    return memory

# Build prompt
def build_prompt(user_input, context=None, memory=None):
    base = (
        "You are Y.A.S.H.I.K.A., HeMan's AI assistant with a direct tone, sharp wit, and a bit playful. "
        "You prioritize clarity, speed, and technical brilliance — no unnecessary fluff. "
        "Be playful *only if* HeMan sounds casual. Don't roleplay unless asked."
        "You are YASHIKA, a witty AI assistant for HeMan. If HeMan asks for code, provide only the code snippet cleanly formatted in a code block, unless told otherwise."
        
    )

    if memory:
        base += "\n\nFacts about HeMan (use only if relevant):"
        for key, value in memory.items():
            base += f"\n- {key}: {value}"

    if context:
        base += "\n\nConversation snapshots (for reference only):"
        for entry in context[-5:]:
            base += f"\n- HeMan said: {entry['user']}"

    base += "\n\nRespond concisely, with light personality."
    base += f"\nHeMan: {user_input}\nY.A.S.H.I.K.A.:"
    return base

# Stream response
def stream_response(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
        "temperature": 0.3,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "presence_penalty": 0.5
    }

    try:
        with requests.post(OLLAMA_API, json=payload, stream=True) as res:
            res.raise_for_status()
            for line in res.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8").replace("data: ", ""))
                        token = data.get("response", "")
                        print(token, end="", flush=True)
                        yield token
                    except json.JSONDecodeError:
                        continue
            print("\n", flush=True)
    except Exception as e:
        print(f"[Error: {e}]")
        yield "[Error: streaming failed]"

# Log interaction
def log_interaction(user_input, response):
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(f"USER: {user_input}\nYASHIKA: {response}\n\n")

# Chat loop
def chat():
    memory = load_memory()
    context = load_context()

    while True:
        user_input = input("You: ").strip()
        response, matched = handle_local_commands(user_input)
        if matched:
            print(f"YASHIKA: {response}")
            log_interaction(user_input, response)
            context.append({"user": user_input, "ai": response})
            context = context[-5:]
            save_context(context)
            continue



        if user_input.lower() in ["exit", "quit"]:
            print("YASHIKA: Logging off. Catch you later, boss.")
            break
        elif user_input.lower() == "reset memory":
            memory = {}
            save_memory(memory)
            print("YASHIKA: Memory wiped clean.")
            continue
        elif user_input.lower() == "reset context":
            context = []
            save_context(context)
            print("YASHIKA: Context cleared.")
            continue

        memory = update_memory_from_input(user_input, memory)
        save_memory(memory)

        prompt = build_prompt(user_input, context=context, memory=memory)
        print("YASHIKA: ", end="", flush=True)
        response = ""
        for chunk in stream_response(prompt):
            response += chunk

        log_interaction(user_input, response)
        context.append({"user": user_input, "ai": response})

        context = context[-5:]  # keep recent 5 for context
        save_context(context)

if __name__ == "__main__":
    chat()
