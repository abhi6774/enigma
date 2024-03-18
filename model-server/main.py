from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from summarizer import _summarize_text
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

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
    return { "app_name": "enigma", "team_name": "The Strivers" }


class Input(BaseModel):
    content: str

@app.post("/summarize/pdf")
def get_summary():
    return {}

@app.post("/summarize/text")
def get_summary_from_text(data: Input):
    result = _summarize_text(data.content)
    return { 
        "summary": result
    }