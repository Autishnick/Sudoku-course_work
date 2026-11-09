import os
import datetime
from fpdf import FPDF

def _find_unicode_font():
    """
    Пошук доступного шрифту з підтримкою кирилиці на системі (Windows або Linux/Docker).
    """
    candidates = [
        # Linux / Docker (Debian/Ubuntu fonts-dejavu-core)
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None

class PDF(FPDF):
    def __init__(self, font_name="Helvetica", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_font = font_name

    def header(self):
        self.set_font(self.report_font, 'B' if self.report_font == 'Helvetica' else '', 15)
        self.cell(0, 10, 'Sudoku Game Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.report_font, 'I' if self.report_font == 'Helvetica' else '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_report(game_list: list) -> bytes:
    font_path = _find_unicode_font()
    if font_path:
        font_name = "UnicodeSans"
        pdf = PDF(font_name=font_name)
        pdf.add_font(font_name, fname=font_path)
    else:
        font_name = "Helvetica"
        pdf = PDF(font_name=font_name)

    pdf.add_page()
    
    # Заголовки таблиці
    pdf.set_font(font_name, 'B' if font_name == 'Helvetica' else '', 10)
    pdf.cell(15, 10, 'ID', 1, 0, 'C')
    pdf.cell(70, 10, 'Name', 1, 0, 'C')
    pdf.cell(45, 10, 'Start Time (UTC)', 1, 0, 'C')
    pdf.cell(30, 10, 'Duration', 1, 1, 'C')
    
    # Дані
    pdf.set_font(font_name, '' if font_name == 'Helvetica' else '', 9)
    for game in game_list:
        game_id = str(game.get("id", ""))
        raw_name = game.get("name")
        if raw_name:
            if font_name == "Helvetica":
                # Fallback для Helvetica (якщо кириличний шрифт не знайдено)
                game_name = raw_name.encode('ascii', errors='replace').decode('ascii')
            else:
                game_name = str(raw_name)
        else:
            game_name = "(Unnamed)"

        start_time = game.get("start_time")
        end_time = game.get("end_time")

        start_str = start_time.strftime('%Y-%m-%d %H:%M') if hasattr(start_time, "strftime") else "N/A"
        duration = "N/A"
        if end_time and start_time and hasattr(end_time, "__sub__"):
            try:
                duration_delta = end_time - start_time
                duration = str(duration_delta).split(".")[0]  # без мікросекунд
            except Exception:
                duration = "N/A"
        
        pdf.cell(15, 10, game_id, 1, 0, 'C')
        pdf.cell(70, 10, game_name, 1, 0, 'L')
        pdf.cell(45, 10, start_str, 1, 0, 'C')
        pdf.cell(30, 10, duration, 1, 1, 'C')
        
    return bytes(pdf.output())
