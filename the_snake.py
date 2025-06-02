import pygame
import random

# Константы для настройки игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""
    
    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """
        Инициализирует базовые атрибуты игрового объекта.
        
        Args:
            body_color: Цвет объекта
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""
    
    def __init__(self):
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject."""
    
    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        
        # Вычисляем новую позицию головы
        new_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверяем столкновение с собой (исключая голову и шею)
        if new_head in self.positions[2:]:
            self.reset()
            return
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Сохраняем позицию последнего сегмента для стирания
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Стираем последний сегмент, если он есть
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        
        # Рисуем все сегменты змейки
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        
        # Очищаем экран
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys():
    """Обрабатывает нажатия клавиш для изменения направления движения змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    global snake, apple
    
    # Инициализация Pygame
    pygame.init()
    
    # Создание объектов игры
    snake = Snake()
    apple = Apple()
    
    # Основной игровой цикл
    while True:
        # Обработка событий клавиш
        handle_keys()
        
        # Обновление направления движения змейки
        snake.update_direction()
        
        # Движение змейки
        snake.move()
        
        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            
            # Убеждаемся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Отрисовка объектов
        snake.draw()
        apple.draw()
        
        # Обновление экрана
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    main()
