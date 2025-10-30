from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from .rag_pipeline.preprocessing import load_and_prepare_text
from .rag_pipeline.llm_integration import summarize_text, generate_question, list_models
import uvicorn

app = FastAPI(title="GenAI GroupU - Educational Assistant")
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Get available models for the dropdown
    models = list_models()
    return templates.TemplateResponse("index.html", {"request": request, "models": models})


@app.post("/summarize/")
async def summarize_endpoint(
    text: str = Form(...),
    model_name: str = Form(...)
):
    summary = summarize_text(text, model_name)
    return {"summary": summary}


@app.post("/question/")
async def get_question(
    topic: str = Form(...),
    model_name: str = Form(...)
):
    question = generate_question(topic, model_name)
    return {"question": question}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    text = await file.read()
    try:
        content = text.decode("utf-8")
    except Exception:
        # fallback to latin-1 if utf-8 fails
        content = text.decode("latin-1")
    load_and_prepare_text(content)
    return {"status": "File processed and indexed", "content": content}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

