#include "generator.h"
#include "solver.h" 
#include "board.h"
#include <random>
#include <algorithm>
#include <chrono>
#include <vector>

// Допоміжна функція: заповнює 3 діагональні квадрати 3x3,
// які не конфліктують між собою, щоб створити "затравку".
void fill_diagonal_boxes(Board& board) {
    std::vector<int> nums = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::mt19937 g(seed);

    for (int i = 0; i < N; i += 3) {
        std::shuffle(nums.begin(), nums.end(), g);
        int k = 0;
        for (int row = 0; row < 3; row++) {
            for (int col = 0; col < 3; col++) {
                board[i + row][i + col] = nums[k++];
            }
        }
    }
}

// Головна функція генерації головоломки
Board generate_puzzle_function(std::string difficulty) {
    
    // 1. Створюємо повністю вирішене поле Судоку
    Board puzzle_board(N, std::vector<int>(N, 0));
    fill_diagonal_boxes(puzzle_board);
    solve_puzzle_function(puzzle_board); // Вирішуємо неповну дошку

    // 2. Створюємо список індексів (0-80) і перемішуємо його
    std::vector<int> cell_indices(N * N);
    for (int i = 0; i < N * N; ++i) {
        cell_indices[i] = i;
    }

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::shuffle(cell_indices.begin(), cell_indices.end(), std::mt19937(seed));

    // 3. Визначаємо, скільки клітинок видалити
    int cells_to_remove;
    if (difficulty == "easy") {
        cells_to_remove = 35; 
    } else if (difficulty == "medium") {
        cells_to_remove = 45;
    } else { 
        cells_to_remove = 50; 
    }
    
    int cells_removed = 0;

    // 4. Головний цикл: видаляємо клітинки, перевіряючи унікальність
    for (int index : cell_indices) {
        if (cells_removed >= cells_to_remove) {
            break; 
        }

        int row = index / N;
        int col = index % N;

        // Запам'ятовуємо цифру і видаляємо її
        int original_value = puzzle_board[row][col];
        puzzle_board[row][col] = 0;

        // Перевіряємо, чи має дошка тепер більше одного рішення
        Board temp_board = puzzle_board;
        int solutions = count_solutions(temp_board);

        if (solutions > 1) {
            // Якщо так - скасовуємо видалення (повертаємо цифру)
            puzzle_board[row][col] = original_value;
        } else {
            // Якщо ні (рішення унікальне) - зараховуємо видалення
            cells_removed++;
        }
    }

    return puzzle_board;
}