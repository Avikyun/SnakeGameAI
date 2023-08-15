import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Dimensions
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20

class Snake:
    def __init__(self):
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)  # (x, y)

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % (WIDTH // CELL_SIZE), (head_y + dir_y) % (HEIGHT // CELL_SIZE))
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % (WIDTH // CELL_SIZE), (head_y + dir_y) % (HEIGHT // CELL_SIZE))
        self.body = [new_head] + self.body

    def set_direction(self, direction):
        self.direction = direction

    def get_head(self):
        return self.body[0]

    def collides_with_self(self):
        return self.get_head() in self.body[1:]

class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1), random.randint(0, (HEIGHT // CELL_SIZE) - 1))

    def respawn(self):
        self.position = (random.randint(0, (WIDTH // CELL_SIZE) - 1), random.randint(0, (HEIGHT // CELL_SIZE) - 1))

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def safe_move(snake, direction):
    head_x, head_y = snake.get_head()
    dir_x, dir_y = direction
    new_head = ((head_x + dir_x) % (WIDTH // CELL_SIZE), (head_y + dir_y) % (HEIGHT // CELL_SIZE))
    if new_head in snake.body:
        return False
    return True

def snake_ai(snake, food):
    best_direction = snake.direction
    shortest_distance = float('inf')
    
    for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # UP, DOWN, LEFT, RIGHT
        head_x, head_y = snake.get_head()
        dir_x, dir_y = direction
        new_head = ((head_x + dir_x) % (WIDTH // CELL_SIZE), (head_y + dir_y) % (HEIGHT // CELL_SIZE))
        
        distance = manhattan_distance(new_head, food.position)
        if distance < shortest_distance and safe_move(snake, direction):
            best_direction = direction
            shortest_distance = distance
    
    return best_direction

def draw_game(screen, snake, food):
    screen.fill(BLACK)

    # Draw snake
    for index, segment in enumerate(snake.body):
        color = (
            max(0, GREEN[0] - index*2),
            max(0, GREEN[1] - index*2),
            max(0, GREEN[2] - index*2)
        )
        pygame.draw.rect(screen, color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw eyes and mouth for the head
        if index == 0:
            dir_x, dir_y = snake.direction
            # Eyes
            if snake.direction == (1, 0):  # Right
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 15, segment[1]*CELL_SIZE + 5), 3)
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 15, segment[1]*CELL_SIZE + 15), 3)
            elif snake.direction == (-1, 0):  # Left
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 5, segment[1]*CELL_SIZE + 5), 3)
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 5, segment[1]*CELL_SIZE + 15), 3)
            elif snake.direction == (0, 1):  # Down
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 5, segment[1]*CELL_SIZE + 15), 3)
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 15, segment[1]*CELL_SIZE + 15), 3)
            elif snake.direction == (0, -1):  # Up
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 5, segment[1]*CELL_SIZE + 5), 3)
                pygame.draw.circle(screen, WHITE, (segment[0]*CELL_SIZE + 15, segment[1]*CELL_SIZE + 5), 3)
            
            # Mouth
            mouth_length = 5
            if snake.direction == (1, 0):  # Right
                pygame.draw.line(screen, BLACK, (segment[0]*CELL_SIZE + CELL_SIZE, segment[1]*CELL_SIZE + CELL_SIZE//2),
                                 (segment[0]*CELL_SIZE + CELL_SIZE, segment[1]*CELL_SIZE + CELL_SIZE//2 + mouth_length))
            elif snake.direction == (-1, 0):  # Left
                pygame.draw.line(screen, BLACK, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE + CELL_SIZE//2),
                                 (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE + CELL_SIZE//2 + mouth_length))
            elif snake.direction == (0, 1):  # Down
                pygame.draw.line(screen, BLACK, (segment[0]*CELL_SIZE + CELL_SIZE//2, segment[1]*CELL_SIZE + CELL_SIZE),
                                 (segment[0]*CELL_SIZE + CELL_SIZE//2 + mouth_length, segment[1]*CELL_SIZE + CELL_SIZE))
            elif snake.direction == (0, -1):  # Up
                pygame.draw.line(screen, BLACK, (segment[0]*CELL_SIZE + CELL_SIZE//2, segment[1]*CELL_SIZE),
                                 (segment[0]*CELL_SIZE + CELL_SIZE//2 + mouth_length, segment[1]*CELL_SIZE))

    # Draw food as an apple
    pygame.draw.circle(screen, RED, (food.position[0] * CELL_SIZE + CELL_SIZE // 2, food.position[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
    # Apple stem
    pygame.draw.rect(screen, (139, 69, 19), (food.position[0] * CELL_SIZE + CELL_SIZE // 2 - 2, food.position[1] * CELL_SIZE, 4, 6))
    # Apple shine effect
    pygame.draw.circle(screen, WHITE, (food.position[0] * CELL_SIZE + CELL_SIZE // 3, food.position[1] * CELL_SIZE + CELL_SIZE // 3), 3)

    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Avikun snake with dumb Ai")
    
    clock = pygame.time.Clock()
    ai_mode = True  # Set this to True or False to toggle AI mode

    while True:  # Outer loop to restart the game
        snake = Snake()
        food = Food()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Exit the entire game
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        snake.set_direction((0, -1))
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        snake.set_direction((0, 1))
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        snake.set_direction((-1, 0))
                    if event.key in [pygame.K_RIGHT, pygame.K_d]:
                        snake.set_direction((1, 0))

            if ai_mode:
                new_direction = snake_ai(snake, food)
                snake.set_direction(new_direction)

            snake.move()

            if snake.get_head() == food.position:
                snake.grow()
                food.respawn()

            if snake.collides_with_self():
                running = False

            draw_game(screen, snake, food)
            clock.tick(10)

if __name__ == "__main__":
    main()
