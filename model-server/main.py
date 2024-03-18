from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return { "app_name": "enigma", "team_name": "The Strivers" }


@app.post("/summarize/pdf")
def get_summary():
    return {}