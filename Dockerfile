# Базовий образ
FROM python:3.13-slim

# Встановлення C++ компілятора та інструментів збірки
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    pybind11-dev \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Встановлення Python-залежностей
WORKDIR /app
COPY backend/requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Копіювання коду додатку
COPY backend /app/backend
COPY cpp_core /app/cpp_core

# Компіляція C++ ядра
RUN mkdir -p /app/cpp_core/build
WORKDIR /app/cpp_core/build
RUN cmake ..
RUN cmake --build .

# Копіювання скомпільованого C++ модуля у backend
RUN mkdir -p /app/backend/cpp_module
RUN cp /app/cpp_core/build/*.so /app/backend/cpp_module/

# Запуск ASGI сервера
WORKDIR /app/backend
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
