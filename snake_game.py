import pygame
import random
import sys

# تهيئة pygame
pygame.init()

# الألوان
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# إعدادات اللعبة
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# الاتجاهات
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_position)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = GREEN
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
    
    def grow(self):
        self.length += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, rect, 1)

def main():
    # إعداد النافذة
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('لعبة الأفعى - استخدم الأسهم للتحكم')
    clock = pygame.time.Clock()
    
    # إنشاء الكائنات
    snake = Snake()
    food = Food()
    
    # اللعبة الرئيسية
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
        
        snake.move()
        
        if snake.get_head_position() == food.position:
            snake.grow()
            food.randomize_position()
            while food.position in snake.positions:
                food.randomize_position()
        
        screen.fill(WHITE)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        
        font = pygame.font.SysFont('arial', 20)
        score_text = font.render(f'النقاط: {snake.score}', True, BLACK)
        screen.blit(score_text, (10, 10))
        
        instructions = font.render('استخدم مفاتيح الأسهم للتحكم', True, BLACK)
        screen.blit(instructions, (10, HEIGHT - 30))
        
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
