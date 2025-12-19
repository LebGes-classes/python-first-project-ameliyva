"""
Модуль с классом Player.
Представляет игрока в лабиринте.
"""


class Player:
    """
    Класс для представления игрока.

    Атрибуты:
        x (int): Координата X игрока на карте.
        y (int): Координата Y игрока на карте.
        score (int): Счет игрока.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Инициализирует объект игрока.

        Args:
            x (int): Начальная координата X игрока.
            y (int): Начальная координата Y игрока.
        """
        self.x = x  # Координата X игрока
        self.y = y  # Координата Y игрока
        self.score = 0  # Счет игрока

    def move(self, dx: int, dy: int, maze) -> bool:
        """
        Перемещает игрока в заданном направлении.

        Args:
            dx (int): Изменение координаты X.
            dy (int): Изменение координаты Y.
            maze (Maze): Объект лабиринта для проверки перемещения.

        Returns:
            bool: True если перемещение успешно, False в противном случае.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем, можно ли переместиться в новую позицию
        if maze.is_valid_move(new_x, new_y):
            self.x = new_x
            self.y = new_y

            return True

        return False