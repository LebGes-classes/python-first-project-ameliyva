import random
from enum import Enum


# Перечисление для типов клеток лабиринта
class CellType(Enum):
    wall = '██' #Стена
    path = '  '  # Проход
    player = '🐹'  # Игрок
    exit = '🟩'  # Выход
    visited = '🟡 '  # Посещенная клетка (для генерации)


# Класс для представления игрока
class Player:
    def __init__(self, x, y):
        self.x = x  # Координата X игрока
        self.y = y  # Координата Y игрока
        self.score = 0  # Счет игрока

    def move(self, dx, dy, maze):
        """Перемещение игрока в заданном направлении"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Проверяем, можно ли переместиться в новую позицию
        if maze.is_valid_move(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        return False


# Класс для представления лабиринта
class Maze:
    def __init__(self, width, height):
        self.width = width  # Ширина лабиринта
        self.height = height  # Высота лабиринта
        self.setka = []  # Двумерный список для хранения клеток
        self.player_start = (1, 1)  # Стартовая позиция игрока
        self.exit_position = None  # Позиция выхода

    def generate(self):
        """Генерация лабиринта алгоритмом поиска в глубину"""
        # Инициализируем сетку стенами
        self.setka = [[CellType.wall for _ in range(self.width)]
                     for _ in range(self.height)]

        # Начальная точка для генерации
        stack = [(1, 1)]
        self.setka[1][1] = CellType.visited

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
                        self.setka[next_x][next_y] == CellType.wall):
                    possible_dirs.append((dx, dy, next_x, next_y))

            if possible_dirs:
                # Выбираем случайное направление
                dx, dy, next_x, next_y = random.choice(possible_dirs)

                # Убираем стену между текущей и следующей клеткой
                wall_x = current_x + dx // 2
                wall_y = current_y + dy // 2
                self.setka[wall_x][wall_y] = CellType.visited
                self.setka[next_x][next_y] = CellType.visited

                stack.append((next_x, next_y))
            else:
                # Если нет возможных направлений, возвращаемся назад
                stack.pop()

        # Преобразуем посещенные клетки в проходы
        for i in range(self.height):
            for j in range(self.width):
                if self.setka[i][j] == CellType.visited:
                    self.setka[i][j] = CellType.path

        # Устанавливаем стартовую позицию и выход
        self.setka[1][1] = CellType.player
        self.exit_position = (self.height - 2, self.width - 2)
        self.setka[self.exit_position[0]][self.exit_position[1]] = CellType.exit

        return self.setka

    def is_valid_move(self, x, y):
        """Проверка возможности перемещения в указанную клетку"""
        return (0 <= x < self.height and
                0 <= y < self.width and
                self.setka[x][y] != CellType.wall)

    def get_cell(self, x, y):
        """Получение типа клетки по координатам"""
        return self.setka[x][y]

    def update_cell(self, x, y, cell_type):
        """Обновление типа клетки"""
        self.setka[x][y] = cell_type


# Класс игры, управляющий основным процессом
class Game:
    def __init__(self):
        self.current_level = 1  # Текущий уровень
        self.max_levels = 5  # Максимальное количество уровней
        self.player = None  # Объект игрока
        self.maze = None  # Объект лабиринта
        self.is_running = True  # Флаг работы игры
        self.level_scores = {1: 100, 2: 200, 3: 300, 4: 400, 5: 500}  # Очки за уровни


    def display_menu(self):
        """Отображение главного меню"""
        print("1. Начать новую игру")
        print("2. Продолжить (если доступно)")
        print("3. Выход")
        print("=" * 40)

        while True:
            choice = input("Выберите пункт меню (1-3): ")
            if choice in ['1', '2', '3']:
                return choice
            print("Неверный ввод. Пожалуйста, выберите 1, 2 или 3.")

    def display_game_ui(self):
        """Отображение игрового интерфейса"""
        print(f"Уровень: {self.current_level}")
        print(f"Счет: {self.player.score}")
        print("Управление: W-вверх, S-вниз, A-влево, D-вправо, M-меню")
        print("=" * (self.maze.width + 2))

        # Отображение лабиринта
        for row in self.maze.setka:
            print('|' + ''.join(cell.value for cell in row) + '|')

        print("=" * (self.maze.width + 2))

    def handle_input(self):
        """Обработка пользовательского ввода"""
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
                    self.maze.update_cell(old_x, old_y, CellType.path)
                    self.maze.update_cell(self.player.x, self.player.y, CellType.player)
                    return 'moved'
                else:
                    print("Не могу переместиться! Стена на пути.")
            else:
                print("Неверная команда! Используйте W,A,S,D для движения или M для меню.")

    def check_win_condition(self):
        """Проверка достижения выхода"""
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

    def generate_level(self):
        """Генерация нового уровня"""
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
                if self.maze.get_cell(i, j) == CellType.player:
                    self.player = Player(i, j)
                    break

    def run(self):
        """Основной игровой цикл"""
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

    def play_game(self):
        """Игровой процесс"""
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


# Точка входа в программу
if __name__ == "__main__":
    # Создаем экземпляр игры и запускаем ее
    game = Game()
    game.run()