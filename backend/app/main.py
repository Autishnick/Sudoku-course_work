import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

cpp_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cpp_module'))
sys.path.append(cpp_module_path)

from .api import game_routes
from .services import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://course-work-sudoku.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Sudoku API is running. Go to /docs for API info."}