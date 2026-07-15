# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
# from starlette.middleware.sessions import SessionMiddleware
# from sqlalchemy.orm import Session
# import uuid
# from database import SessionLocal
# from models import Chat
# from pydantic import BaseModel
# from llama_cpp import Llama

# app = FastAPI()

# #Add session middleware
# # app.add_middleware(SessionMiddleware, secret_key="secret")

# #Static + Templates
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

# #Load Model here
# llm = Llama(
#     model_path = r"D:/Local_Models/meta-llama-3-8b-instruct.Q4_K_M.gguf",
#     n_ctx = 2048,          #Context Size
#     n_threads = 4          #adjust based on CPU
# )

# # Get DB
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Create new session
# @app.get("/new-session")
# def new_session():
#     return {"session_id":str(uuid.uuid4())}


# # Load chat history
# @app.get("/history/{session_id}")
# def get_history(session_id: str):
#     db = SessionLocal()
#     chats = db.query(Chat).filter(Chat.session_id == session_id).all()

#     return [
#         {"role": c.role, "message": c.message}
#         for c in chats
#     ]


# class PromptRequest(BaseModel):
#     prompt : str


# # chat_history = []

# @app.get("/")
# def home(request: Request):
#     return templates.TemplateResponse(request= request, name="index.html", context={"request": request})


# # @app.post("/chat")
# # async def chat(request: PromptRequest):
# #     response = llm(
# #         prompt = f"### Instruction:\n{request.prompt}\n### Response:",
# #         max_tokens = 200,
# #         temperature = 0.7,
# #         stop = ["###"]
# #     )

# #     return {
# #         "response": response["choices"][0]["text"].strip()
# #     }


# #CHAT WITH HISTORY
# # @app.post("/chat")
# # async def chat(request: Request, data: PromptRequest):

# #     # Get session history
# #     history = request.session.get("chat_history", [])

# #     # Add user message
# #     history.append(f"User: {data.prompt}")

# #     # Build prompt
# #     full_prompt = "\n".join(history) + "\nAssistant:"

# #     # Generate response
# #     response = llm(full_prompt, max_tokens=200)
# #     answer = response["choices"][0]["text"].strip()

# #     #Save bot response
# #     history.append(f"Assistant: {answer}")

# #     # Store back in session
# #     request.session["Chat_history"] = history

# #     return {"response": answer}



# @app.post("/clear")
# def clear_chat(request: Request):
#     request.session["chat_history"] = []
#     return {"message": "Chat cleared"}


# # ⏳ Streaming Chat
# @app.post("/chat")
# def chat(request: dict):

#     session_id = request["session_id"]
#     prompt = request["prompt"]

#     db = SessionLocal()

#     # Save user message
#     db.add(Chat(session_id=session_id, role="user", message=prompt))
#     db.commit()

#     # Get history
#     # history = db.query(Chat).filter(Chat.session_id == session_id).all()
#     full_prompt = f"### Instruction:\n{prompt}\n### Response:"
#     # full_prompt = ""
#     # for h in history:
#     #     full_prompt += f"{h.role}: {h.message}\n"
#     # full_prompt += "assistant:"

#     def generate():
#         output = ""

#         for token in llm(full_prompt, stream=True, max_tokens=200):
#             text = token["choices"][0]["text"]
#             output += text
#             yield text

#         # Save final response
#         db.add(Chat(session_id=session_id, role="assistant", message=output))
#         db.commit()

#     return StreamingResponse(generate(), media_type="text/plain")



from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import uuid

from database import SessionLocal
from models import Chat
from llama_cpp import Llama

app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load Model
llm = Llama(
    model_path=r"D:/Local_Models/meta-llama-3-8b-instruct.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=4
)

# Home
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


# Create new session
@app.get("/new-session")
def new_session():
    return {"session_id": str(uuid.uuid4())}


# Load history (ONLY UI purpose)
@app.get("/history/{session_id}")
def get_history(session_id: str):
    db = SessionLocal()
    chats = db.query(Chat).filter(Chat.session_id == session_id).all()

    return [{"role": c.role, "message": c.message} for c in chats]


# 🔥 FIXED CHAT (NO HISTORY USED IN MODEL)
@app.post("/chat")
def chat(request: dict):

    session_id = request["session_id"]
    prompt = request["prompt"]

    db = SessionLocal()

    # Save user message
    db.add(Chat(session_id=session_id, role="user", message=prompt))
    db.commit()

    # ✅ STRICT PROMPT (NO HISTORY)
    full_prompt = f"""
You are an AI assistant.
Answer ONLY the current question.
Do NOT use any previous conversation.

Question:
{prompt}

Answer:
"""

    def generate():
        output = ""

        for token in llm(
            full_prompt,
            stream=True,
            max_tokens=200,
            temperature=0.7,
            stop=["Question:", "User:", "###"]
        ):
            text = token["choices"][0]["text"]
            output += text
            yield text

        # Save AI response
        db.add(Chat(session_id=session_id, role="assistant", message=output))
        db.commit()

    return StreamingResponse(generate(), media_type="text/plain")