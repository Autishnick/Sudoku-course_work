from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse

from ..core import game_manager
from ..services import database, report_generator, pdf_generator

router = APIRouter()

Board = List[List[int]]

class GenerateRequest(BaseModel):
    difficulty: str

class SolveRequest(BaseModel):
    board: Board

class SaveGameRequest(BaseModel):
    game_id: int
    current_board: Board
    name: str

class FinishGameRequest(BaseModel):
    game_id: int
    final_board: Board

class CustomGameRequest(BaseModel):
    board: Board

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/status")
def get_status():
    status = game_manager.get_solver_status()
    if not status:
        raise HTTPException(status_code=500, detail="C++ 'sudoku_solver' module not loaded")
    return {"cpp_module_loaded": True}

@router.post("/generate")
def generate_game(request: GenerateRequest, db: Session = Depends(get_db)):
    
    puzzle = game_manager.generate_new_puzzle(request.difficulty)
    if puzzle is None:
        raise HTTPException(status_code=500, detail="Failed to generate puzzle. C++ module error.")
    
    solution = game_manager.solve_puzzle(puzzle)
    if solution is None:
        raise HTTPException(status_code=500, detail="Generated puzzle has no solution. C++ module error.")

    game_id = database.create_new_game(db, initial_board=puzzle)
    
    return {"game_id": game_id, "puzzle": puzzle, "solution": solution}

@router.post("/solve")
def solve_game(request: SolveRequest):
    solution = game_manager.solve_puzzle(request.board)
    if solution is None:
        raise HTTPException(status_code=500, detail="Failed to solve puzzle. C++ module error or no solution.")
    return {"solution": solution}

@router.post("/save")
def save_game(request: SaveGameRequest, db: Session = Depends(get_db)):
    success, message = database.save_game_state(
        db, request.game_id, request.current_board, request.name
    )
    if not success:
        raise HTTPException(status_code=404, detail=message)
    return {"message": "Game saved successfully"}

@router.get("/load_by_name/{name}")
def load_game_by_name_endpoint(name: str, db: Session = Depends(get_db)):
    
    game_data = database.load_game_by_name(db, name)
    
    if game_data is None:
        raise HTTPException(status_code=404, detail="Game not found with that name")
    
    initial_board = game_data["initial_board"]
    
    solution = game_manager.solve_puzzle(initial_board)
    if solution is None:
        raise HTTPException(status_code=500, detail="Could not solve the initial board to get solution.")

    game_data["solution"] = solution
    
    return game_data

@router.post("/finish")
def finish_game_endpoint(request: FinishGameRequest, db: Session = Depends(get_db)):
    success = database.finish_game(db, request.game_id, request.final_board)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found or already completed")
    return {"message": "Game completed and logged for reporting."}


@router.get("/saves")
def get_all_saves(db: Session = Depends(get_db)):
    games_info = database.get_all_saves_info(db)
    return {"saves": games_info}

@router.delete("/delete/{name}")
def delete_game_endpoint(name: str, db: Session = Depends(get_db)):
    success = database.delete_game_by_name(db, name)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found with that name")
    return {"message": "Game deleted successfully"}


@router.get("/report/html", response_class=HTMLResponse)
def get_html_report(db: Session = Depends(get_db)):
    games_list = database.get_all_reports(db)
    
    html_content = report_generator.format_report_as_html(games_list)
    
    return html_content

@router.get("/report/pdf")
def get_pdf_report(db: Session = Depends(get_db)):
    games = database.get_all_reports(db)
    pdf_data_bytearray = pdf_generator.create_pdf_report(games)
    
    return Response(
        content=bytes(pdf_data_bytearray), 
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=sudoku_report.pdf"}
    )

@router.post("/start_custom_game")
def start_custom_game(request: CustomGameRequest, db: Session = Depends(get_db)):
    board = request.board
    
    solution = game_manager.solve_puzzle(board)
    if solution is None:
        raise HTTPException(status_code=400, detail="This puzzle is unsolvable.")
        
    solution_count = game_manager.count_puzzle_solutions(list(board))
    if solution_count > 1:
        raise HTTPException(status_code=400, detail="This puzzle has multiple solutions. Please provide more clues.")
        
    game_id = database.create_new_game(db, initial_board=board)
    
    return {"game_id": game_id, "puzzle": board, "solution": solution}