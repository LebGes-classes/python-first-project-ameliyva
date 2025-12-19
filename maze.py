"""
Модуль с классом Maze.
Генерирует и управляет лабиринтом.
"""

import random
from cell_types import WALL, PATH, PLAYER, EXIT, VISITED


class Maze:
    """
    Класс для представления лабиринта.

    Атрибуты:
        width (int): Ширина лабиринта.
        height (int): Высота лабиринта.
        setka (list): Двумерный список для хранения клеток.
        player_start (tuple): Стартовая позиция игрока.
        exit_position (tuple): Позиция выхода.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Инициализирует объект лабиринта.

        Args:
            width (int): Ширина лабиринта.
            height (int): Высота лабиринта.
        """
        self.width = width  # Ширина лабиринта
        self.height = height  # Высота лабиринта
        self.setka = []  # Двумерный список для хранения клеток
        self.player_start = (1, 1)  # Стартовая позиция игрока
        self.exit_position = None  # Позиция выхода

    def generate(self) -> list:
        """
        Генерирует лабиринт алгоритмом поиска в глубину.

        Returns:
            list: Двумерный список сгенерированного лабиринта.
        """
        # Инициализируем сетку стенами
        self.setka = [[WALL for _ in range(self.width)]
                      for _ in range(self.height)]

        # Начальная точка для генерации
        stack = [(1, 1)]
        self.setka[1][1] = VISITED

        # Список возможных направлений
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

        while stack:
            current_x, current_y = stack[-1]

            # Получаем все возможные направления
            possible_dirs = []
            for dx, dy in directions:
                next_x = current_x + dx
                next_y = current_y + dy

                # Проверяем, находится ли клетка в пределах лабиринта
                if (0 < next_x < self.height - 1 and
                        0 < next_y < self.width - 1 and
                        self.setka[next_x][next_y] == WALL):
                    possible_dirs.append((dx, dy, next_x, next_y))

            if possible_dirs:
                # Выбираем случайное направление
                dx, dy, next_x, next_y = random.choice(possible_dirs)

                # Убираем стену между текущей и следующей клеткой
                wall_x = current_x + dx // 2
                wall_y = current_y + dy // 2
                self.setka[wall_x][wall_y] = VISITED
                self.setka[next_x][next_y] = VISITED

                stack.append((next_x, next_y))
            else:
                # Если нет возможных направлений, возвращаемся назад
                stack.pop()

        # Преобразуем посещенные клетки в проходы
        for i in range(self.height):
            for j in range(self.width):
                if self.setka[i][j] == VISITED:
                    self.setka[i][j] = PATH

        # Устанавливаем стартовую позицию и выход
        self.setka[1][1] = PLAYER
        self.exit_position = (self.height - 2, self.width - 2)
        self.setka[self.exit_position[0]][self.exit_position[1]] = EXIT

        return self.setka

    def is_valid_move(self, x: int, y: int) -> bool:
        """
        Проверяет возможность перемещения в указанную клетку.

        Args:
            x (int): Координата X целевой клетки.
            y (int): Координата Y целевой клетки.

        Returns:
            bool: True если перемещение возможно, False в противном случае.
        """
        return (0 <= x < self.height and
                0 <= y < self.width and
                self.setka[x][y] != WALL)

    def get_cell(self, x: int, y: int) -> str:
        """
        Получает тип клетки по координатам.

        Args:
            x (int): Координата X клетки.
            y (int): Координата Y клетки.

        Returns:
            str: Символ, представляющий тип клетки.
        """
        return self.setka[x][y]

    def update_cell(self, x: int, y: int, cell_type: str) -> None:
        """
        Обновляет тип клетки по координатам.

        Args:
            x (int): Координата X клетки.
            y (int): Координата Y клетки.
            cell_type (str): Новый тип клетки.
        """
        self.setka[x][y] = cell_type