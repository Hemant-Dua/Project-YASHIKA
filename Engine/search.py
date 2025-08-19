import os
import json
import requests
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API = os.getenv("OLLAMA_API")
MODEL = os.getenv("MODEL")

def web_search(query, max_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(f"{r['title']}: {r['body']} ({r['href']})")
    return "\n".join(results)

def ask_ollama(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": True,
    }

    try:
        with requests.post(OLLAMA_API, json=payload, stream=True) as res:
            res.raise_for_status()
            full_response = ""
            for line in res.iter_lines():
                if line:
                    try:
                        # Ollama streaming lines start with "data: "
                        data = json.loads(line.decode("utf-8").replace("data: ", ""))
                        token = data.get("response", "")
                        print(token, end="", flush=True)   # stream to console
                        full_response += token
                    except json.JSONDecodeError:
                        continue
            print("\n", flush=True)
            return full_response
    except Exception as e:
        print(f"[Error: {e}]")
        return "[Error: streaming failed]"


def yashika_browse(query):
    snippets = web_search(query)
    prompt = f"""
    Boss asked: "{query}"

    Here are the top search snippets:
    {snippets}

    Instructions:
    1. First decide the query type:
    - If factual (asks for a name, date, place, number, 'latest', 'who', 'what', 'when', 'capital'), 
        then extract the exact fact from the snippets and reply in **one concise line**.
    - If explanatory (asks for a summary, strategy, why, how, pros/cons, overview),
        then reply in **2–4 clear sentences**.
    2. Only include a source if it is critical for credibility.
    3. Stay short, direct, and no filler words.

    Now, answer Boss accordingly:
    """

    return ask_ollama(prompt)


# if __name__ == "__main__":
#     while True:
#         query = input("Boss, what do you want me to browse?\n> ")
#         yashika_browse(query)
