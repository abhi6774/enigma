from fastapi import FastAPI, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from summarizer import summarize_text, summarize_from_pdf, extract_key_phrase
from pydantic import BaseModel
from uuid import uuid4
from chat_session import ChatSession
from logger import log
from dataclasses import dataclass
from typing import Optional
from redis_server import * 
from uvicorn import run

load_dotenv()

app = FastAPI()

sessions = ChatSession()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"app_name": "enigma", "team_name": "The Strivers"}


class Input(BaseModel):
    content: str


@app.post("/summarize")
async def summarize_the_text(data: Input):
    summary = summarize_text(data.content)
    return summary




@app.post("/summarize/text", response_class=RedirectResponse, status_code=302)
def get_summary_from_text(data: Input):
    summary = summarize_text(data.content)
    chat_session_id = uuid4().hex
    session = sessions.get_chat_session(chat_session_id)
    model_response = session.set_context(data.content)
    log(model_response)
    log(session)
    session_id = session.get_session_id(),

    session.set_summary(summary["summary"])
    key_entities = extract_key_phrase(data.content)
    session.set_key_entities(key_entities)

    return f"http://localhost:3000/conversation/{session_id}"



@app.post("/summarize/pdf")
async def get_summary(file: UploadFile = File()):
    ROOT_PATH="./tmp"
    fileData = await file.read()

    with open(f"{ROOT_PATH}/{file.filename}", "bw") as writeFile:
        writeFile.write(fileData)

    summary = summarize_from_pdf(f"{ROOT_PATH}/{file.filename}")
    chat_session_id = uuid4().hex

    session = sessions.get_chat_session(chat_session_id)
    log(session)

    model_response = session.set_context(summary["original_text"])
    log(model_response)

    session_id = session.get_session_id(),
    session.set_summary(summary["summary"])
    key_entities = extract_key_phrase(summary["original_text"])
    session.set_key_entities(key_entities)

    return {
        "session_id": session_id[0]
    }


@dataclass
class QuestionInput(BaseModel):
    content: Optional[str] = None
    context: Optional[str] = None


@app.post("/chat/{chat_session}")
def talk(chat_session: str, inp: QuestionInput):

    session = sessions.get_chat_session(chat_session)
    mResponse = session.send_message(inp.content)
    return  mResponse


@app.get("/chat/s/{chat_session}")
def talk(chat_session: str):
    session = sessions.get_chat_session(chat_session)
    return {
        **session.__dict__,
        "summary": session.get_summary(),
        "key_entities": session.get_key_entities(),
        "messages": session.get_messages()[session._context_width:]
    }


@app.get("/s/list")
def get_session_id_list():
    return [x.get_session_id() for x in sessions._chat_sessions]


if __name__=="__main__":
    run(app)