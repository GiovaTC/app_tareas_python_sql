# app_tareas_python_sql

<img width="2556" height="1079" alt="image" src="https://github.com/user-attachments/assets/20c9b734-e379-4f3b-ae6b-bb77f51226dd" />

# 🎯 Objetivo del proyecto: "Administrador de Tareas"

Una pequeña app donde el usuario puede:

- Ver todas las tareas  
- Agregar una tarea  
- Marcarla como completada  
- Eliminarla  

---

## 📁 Estructura del Proyecto

task_app/
│
├── backend/
│ ├── main.py
│ ├── models.py
│ ├── database.py
│ └── crud.py
│
├── frontend/
│ ├── index.html
│ └── style.css
│
├── requirements.txt
└── run.py

---

## 🔧 Paso a paso

### 1. Instalar dependencias

Crea un entorno virtual y ejecuta:

```bash
pip install fastapi uvicorn sqlalchemy jinja2 aiofiles

2. database.py – Configurar la base de datos
python

# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

3. models.py – Crear el modelo de la base de datos
python

# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

4. crud.py – Funciones para manejar la base de datos
python

# backend/crud.py
from sqlalchemy.orm import Session
from . import models

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_task(db: Session, title: str):
    task = models.Task(title=title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()

def complete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        task.completed = True
        db.commit()

5. main.py – Backend con FastAPI
python

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
def read_root(request: Request):
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

6. frontend/index.html – HTML del frontend
html

<!-- frontend/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Administrador de Tareas</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Mis Tareas</h1>
    <form action="/add" method="post">
        <input type="text" name="title" placeholder="Nueva tarea" required>
        <button type="submit">Agregar</button>
    </form>

    <ul>
        {% for task in tasks %}
            <li class="{{ 'completed' if task.completed else '' }}">
                {{ task.title }}
                {% if not task.completed %}
                    <form action="/complete/{{ task.id }}" method="post">
                        <button type="submit">Completar</button>
                    </form>
                {% endif %}
                <form action="/delete/{{ task.id }}" method="post">
                    <button type="submit">Eliminar</button>
                </form>
            </li>
        {% endfor %}
    </ul>
</body>
</html>

7. frontend/style.css – Estilos básicos

css

/* frontend/style.css */
body {
    font-family: Arial;
    max-width: 600px;
    margin: 50px auto;
}

h1 {
    text-align: center;
}

form {
    margin-bottom: 20px;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.completed {
    text-decoration: line-through;
    color: gray;
}

8. run.py – Archivo para ejecutar
# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
🚀 Para ejecutar la app
Asegúrate de estar en el entorno virtual

Ejecuta:

python run.py
Visita http://127.0.0.1:8000
