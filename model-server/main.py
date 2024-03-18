from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from summarizer import summarize_text, summarize_from_pdf
from pydantic import BaseModel
from fastapi import UploadFile, File
from uuid import uuid4

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
    return {"app_name": "enigma", "team_name": "The Strivers"}


class Input(BaseModel):
    content: str


@app.post("/summarize")
async def summarize_the_text(data: Input):
    summary = summarize_text(data.content)
    return summary


@app.post("/summarize/text")
def get_summary_from_text(data: Input):
    result = summarize_text(data.content)
    return {
        "summary": result
    }


@app.post("/summarize/pdf")
async def get_summary(file: UploadFile = File()):
    ROOT_PATH="./tmp"
    fileData = await file.read()

    with open(f"{ROOT_PATH}/{file.filename}", "bw") as writeFile:
        writeFile.write(fileData)

    summary = summarize_from_pdf(f"{ROOT_PATH}/{file.filename}")

    return {
        **summary,
    }