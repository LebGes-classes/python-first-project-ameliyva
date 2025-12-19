"""
Модуль с классом Game.
Управляет основным игровым процессом.
"""
from maze import(
    Maze,
(
from player import(
    Player,
(
from cell_types import(
    PATH, PLAYER,
(

class Game:
    """
    Класс игры, управляющий основным процессом.

    Атрибуты:
        current_level (int): Текущий уровень.
        max_levels (int): Максимальное количество уровней.
        player (Player): Объект игрока.
        maze (Maze): Объект лабиринта.
        is_running (bool): Флаг работы игры.
        level_scores (dict): Очки за уровни.
    """

    def __init__(self) -> None:
        """Инициализирует объект игры."""
        self.current_level = 1  # Текущий уровень
        self.max_levels = 5  # Максимальное количество уровней
        self.player = None  # Объект игрока
        self.maze = None  # Объект лабиринта
        self.is_running = True  # Флаг работы игры
        self.level_scores = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500}  # Очки за уровни

    def display_menu(self) -> str:
        """
        Отображает главное меню игры.

        Returns:
            str: Выбор пользователя.
        """
        print("=" * 40)
        print("1. Начать новую игру")
        print("2. Продолжить (если доступно)")
        print("3. Выход")
        print("=" * 40)

        while True:
            choice = input("Выберите пункт меню (1-3): ")
            if choice in ['1', '2', '3']:

                return choice

            print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    def display_game_ui(self) -> None:
        """Отображает игровой интерфейс."""
        print(f"Уровень: {self.current_level}")
        print(f"Счет: {self.player.score}")
        print("Управление: W-вверх, S-вниз, A-влево, D-вправо, M-меню")
        print("=" * (self.maze.width + 2))

        # Отображение лабиринта
        for row in self.maze.setka:
            print('|' + ''.join(cell for cell in row) + '|')

        print("=" * (self.maze.width + 2))

    def handle_input(self) -> str:
        """
        Обрабатывает пользовательский ввод.

        Returns:
            str: Результат обработки ввода ('menu' или 'moved').
        """
        move_dict = {
            'w': (-1, 0),  # Вверх
            's': (1, 0),  # Вниз
            'a': (0, -1),  # Влево
            'd': (0, 1),  # Вправо
        }

        while True:
            key = input("Введите команду: ").lower()

            if key == 'm':

                return 'menu'

            elif key in move_dict:
                dx, dy = move_dict[key]
                old_x, old_y = self.player.x, self.player.y

                if self.player.move(dx, dy, self.maze):
                    # Обновляем клетки на карте
                    self.maze.update_cell(old_x, old_y, PATH)
                    self.maze.update_cell(self.player.x, self.player.y, PLAYER)

                    return 'moved'

                else:
                    print("Не могу переместиться! Стена на пути.")
            else:
                print("Неверная команда! Используйте W,A,S,D для движения или M для меню.")

    def check_win_condition(self) -> bool:
        """
        Проверяет достижение выхода.

        Returns:
            bool: True если выход достигнут, False в противном случае.
        """
        if (self.player.x, self.player.y) == self.maze.exit_position:
            self.player.score += self.level_scores.get(self.current_level, 100)

            if self.current_level < self.max_levels:
                print(f"Поздравляем! Вы прошли уровень {self.current_level}!")
                print(f"Получено очков: {self.level_scores[self.current_level]}")
                input("Нажмите Enter для перехода на следующий уровень...")
                self.current_level += 1

                return True

            else:
                print("Поздравляем! Вы прошли все уровни!")
                print(f"Итоговый счет: {self.player.score}")
                self.is_running = False

                return True

        return False

    def generate_level(self) -> None:
        """Генерирует новый уровень."""
        # Увеличиваем сложность с каждым уровнем
        base_size = 15
        size_increase = self.current_level * 2
        width = base_size + size_increase
        height = base_size + size_increase

        self.maze = Maze(width, height)
        self.maze.generate()

        # Находим позицию игрока
        for i in range(height):
            for j in range(width):
                if self.maze.get_cell(i, j) == PLAYER:
                    self.player = Player(i, j)
                    break

    def run(self) -> None:
        """Запускает основной игровой цикл."""
        while self.is_running:
            menu_choice = self.display_menu()

            if menu_choice == '1':
                self.current_level = 1
                self.player = None
                self.play_game()
            elif menu_choice == '2' and self.player:
                self.play_game()
            elif menu_choice == '3':
                print("Спасибо за игру!")
                self.is_running = False

    def play_game(self) -> None:
        """Запускает игровой процесс."""
        if not self.player:
            self.generate_level()

        while self.is_running and self.current_level <= self.max_levels:
            self.display_game_ui()

            result = self.handle_input()

            if result == 'menu':
                break

            if self.check_win_condition():
                if self.current_level <= self.max_levels:
                    self.generate_level()