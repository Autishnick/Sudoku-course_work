# Потрібна версія 3.15+ для сучасного пошуку Python
cmake_minimum_required(VERSION 3.15)
project(sudoku_core)

# Знайти Python 3.13+
find_package(Python 3.13 COMPONENTS Interpreter Development REQUIRED)

# Знайти pybind11
find_package(pybind11 REQUIRED)

# Вказуємо стандарт C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Створюємо Python-модуль
pybind11_add_module(
    sudoku_solver 
    # Список ваших C++ файлів:
    src/board.cpp
    src/solver.cpp
    src/generator.cpp
    pybind/bindings.cpp # Головний файл зв'язки
)

# pybind11_add_module автоматично додає потрібні include для
# Python та pybind11. Нам потрібно додати лише наш власний 'include'
target_include_directories(
    sudoku_solver 
    PRIVATE 
    include 
)