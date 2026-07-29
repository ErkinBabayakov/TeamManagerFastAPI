import logging
import uvicorn
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.admin import setup_admin
from app.api.admin import router as admin_router
from app.api.member import router as auth_router
from app.api.manager import router as manager_router
from app.api.manager_tasks import router as manager_tasks_router
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Team Manager API")

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(manager_router)
app.include_router(manager_tasks_router)

setup_admin(app)

@app.get("/", response_class=HTMLResponse, tags=["Главная страница документации"])
def home():
    return """
    <h1>Выберите тип документации</h1>
    <h2><a href="/docs">Swagger UI</a><br></h2>
    <h2><a href="/redoc">ReDoc</a></h2>
#     """


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="127.0.0.1", port=8000)
