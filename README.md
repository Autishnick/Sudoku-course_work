🎮 Веб-додаток Судоку / Sudoku Web Application

Це повнофункціональний веб-додаток Судоку, створений як курсовий проект. Він використовує поліглотну архітектуру: високопродуктивне ядро на C++, бекенд API на Python (FastAPI) та інтерактивний UI на React.

---

🎮 Sudoku Web Application

This is a fully functional Sudoku web application created as a course project. It uses a polyglot architecture: a high-performance core in C++, a backend API in Python (FastAPI), and an interactive UI in React.

🚀 Live Demo https://course-work-sudoku.vercel.app/

✨ Main Features Generator with a unique solution (implemented in C++).

Three difficulty levels (Easy, Medium, Hard).

“Create your own game” mode with instant rule validation.

Instant move validation (highlighting incorrect numbers).

Saving/loading/deleting games with unique names.

Instant name availability check when saving.

Navigation across the field using arrow keys.

Automatic victory determination.

Generation of HTML and PDF reports on completed games.

🏗️ Technology stack C++ Core: Logic core (solve, count, generate) in C++17.

Bridge: pybind11 for “wrapping” C++ code in a Python module.

Backend: Python 3.14 with FastAPI (for API), SQLAlchemy (for SQLite), and fpdf2 (for PDF).

Frontend: React 18 (with Vite) with React Context API for state management and axios for HTTP requests.

Deployment:

The backend is containerized with Docker and hosted on Render.

The frontend is hosted on Vercel.
