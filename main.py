# backend/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import models, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request : Request):
    db = next(get_db())
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add")
def add_task(title: str = Form(...)):
    db = next(get_db())
    crud.create_task(db, title)
    return RedirectResponse("/", status_code=303)

@app.post("/complete/{task_id}")
def complete_task(task_id: int):
    db = next(get_db())
    crud.complete_task(db, task_id)
    return RedirectResponse("/", status_code=303)

@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    db = next(get_db())
    crud.delete_task(db, task_id)
    return RedirectResponse("/", status_code=303)


