from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import models
import crud
from database import engine, SessionLocal

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la app
app = FastAPI()

# Montar los archivos estáticos (CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar el motor de plantillas Jinja2
templates = Jinja2Templates(directory="templates")


# Obtener conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ruta principal - ver tareas
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    db = next(get_db())
    tasks = crud.get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})


# Ruta para agregar una tarea
@app.post("/add")
def add_task(title: str = Form(...)):
    db = next(get_db())
    crud.create_task(db, title)
    return RedirectResponse("/", status_code=303)


# Ruta para marcar tarea como completada
@app.post("/complete/{task_id}")
def complete_task(task_id: int):
    db = next(get_db())
    crud.complete_task(db, task_id)
    return RedirectResponse("/", status_code=303)


# Ruta para eliminar una tarea
@app.post("/delete/{task_id}")
def delete_task(task_id: int):
    db = next(get_db())
    crud.delete_task(db, task_id)
    return RedirectResponse("/", status_code=303)
