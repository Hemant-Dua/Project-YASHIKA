import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "llm")))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from fastapi.staticfiles import StaticFiles

from actions import handle_local_commands


from main import (
    build_prompt, load_context, load_memory,
    update_memory_from_input, save_memory, save_context,
    stream_response
)

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Clean context and memory on startup
    save_context([])
    yield  # App runs here
    # You can also do cleanup on shutdown after this if needed

app = FastAPI(lifespan=lifespan)

# Enable CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

@app.post("/chat")
async def chat_api(req: Request):
    data = await req.json()
    user_input = data.get("message", "")

    memory = load_memory()
    context = load_context()
    memory = update_memory_from_input(user_input, memory)
    save_memory(memory)

    # Check for local commands
    response, matched = handle_local_commands(user_input)
    if not matched:
        prompt = build_prompt(user_input, context=context, memory=memory)
        response = stream_response(prompt)


    context.append({"user": user_input, "ai": response})
    context = context[-5:]
    save_context(context)

    return {"response": response}

# Serve static files from 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open("index.html", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
