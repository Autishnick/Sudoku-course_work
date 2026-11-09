# 🎮 Sudoku Web Application

Веб-застосунок гри Судоку з поліглотною архітектурою: високопродуктивне ядро на **C++**, бекенд API на **Python (FastAPI)** та інтерактивний UI на **React**.

**🚀 Live Demo:** https://course-work-sudoku.vercel.app/

---

## ✨ Функціонал

- Генератор пазлів з гарантовано єдиним рішенням (C++)
- Три рівні складності: Easy, Medium, Hard
- Режим «Створи свій пазл» з миттєвою валідацією правил
- Підсвічування некоректних цифр у реальному часі
- Збереження / завантаження / видалення ігор за назвою
- Перевірка доступності назви при збереженні
- Навігація по полю стрілками клавіатури
- Автоматичне визначення перемоги
- Генерація HTML та PDF звітів по завершених іграх

---

## 🏗️ Технологічний стек

| Шар | Технології |
|-----|-----------|
| **C++ Core** | C++17, CMake, pybind11 |
| **Backend** | Python 3.13, FastAPI, Uvicorn, SQLAlchemy, SQLite, fpdf2 |
| **Frontend** | React 19, Vite 7, Axios, React Context API |
| **Deploy** | Backend → Docker → Render.com · Frontend → Vercel |

---

## 🚀 Локальний запуск

### Передумови
- Python 3.13+
- Node.js 18+
- CMake 3.15+
- Visual Studio Build Tools 2022 (Windows) / GCC (Linux/macOS)

### 1. Компіляція C++ модуля

```bash
cd cpp_core
mkdir build && cd build
cmake .. -Dpybind11_DIR="$(python -m pybind11 --cmakedir)"
cmake --build . --config Release
cp Release/sudoku_solver*.pyd ../backend/cpp_module/   # Windows
# або
cp build/*.so ../backend/cpp_module/                   # Linux/macOS
```

### 2. Запуск бекенду

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API доступне на http://localhost:8000  
Swagger UI: http://localhost:8000/docs

### 3. Запуск фронтенду

```bash
cd frontend
npm install
npm run dev
```

Гра доступна на http://localhost:5173

---

## 📡 API Ендпоінти

| Метод | Шлях | Опис |
|-------|------|------|
| `GET` | `/api/status` | Перевірка C++ модуля |
| `POST` | `/api/generate` | Генерація пазлу |
| `POST` | `/api/solve` | Вирішення пазлу |
| `POST` | `/api/save` | Збереження гри |
| `GET` | `/api/load_by_name/{name}` | Завантаження гри |
| `GET` | `/api/saves` | Список збережень |
| `DELETE` | `/api/delete/{name}` | Видалення збереження |
| `POST` | `/api/finish` | Позначити як завершену |
| `GET` | `/api/report/html` | HTML звіт |
| `GET` | `/api/report/pdf` | PDF звіт |
| `POST` | `/api/start_custom_game` | Запуск кастомного пазлу |

---

## 🗂️ Структура проєкту

```
course/
├── cpp_core/              # C++ ядро (генератор + розв'язувач)
│   ├── include/           # Заголовкові файли
│   ├── src/               # Реалізація
│   ├── pybind/            # pybind11 bindings
│   └── CMakeLists.txt
├── backend/               # FastAPI сервер
│   ├── app/
│   │   ├── api/           # REST роути
│   │   ├── core/          # Python-обгортка над C++
│   │   └── services/      # БД, PDF, HTML генератори
│   ├── cpp_module/        # Скомпільований .pyd/.so файл
│   └── requirements.txt
├── frontend/              # React застосунок
│   └── src/
│       ├── api/           # API клієнт (axios)
│       └── components/    # Board, Cell, Controls, Context
└── Dockerfile             # Docker для Render.com
```
