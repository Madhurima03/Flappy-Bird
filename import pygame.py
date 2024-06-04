import pygame
import random
pygame.init()
WIDTH = 500
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BIRD_WIDTH = 64
BIRD_HEIGHT = 64
PIPE_WIDTH = 100
PIPE_GAP = 200
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        original_image = pygame.image.load('bird.png').convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (BIRD_WIDTH, BIRD_HEIGHT))
        self.image = pygame.transform.scale(scaled_image, (32, 32))  # Set desired width and height for the bird image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.velocity = 0
        
    def update(self):
        self.velocity += 0.5
        self.rect.y += self.velocity
        self.rect.x += 5 
        if self.rect.left > WIDTH:
            self.rect.right = 0

    def jump(self):
        self.velocity = -8

    def update(self):
        self.velocity += 0.5
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = -8
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, HEIGHT), pygame.SRCALPHA)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.top_height = random.randint(100, HEIGHT // 2 - 100)
        self.bottom_height = HEIGHT - self.top_height - PIPE_GAP

    def update(self):
        self.rect.x -= 5


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
background = pygame.image.load('background.png').convert()
bird_group = pygame.sprite.Group()
bird = Bird()  
bird_group.add(bird)  
pipe_group = pygame.sprite.Group()
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_group.sprites()[0].jump()

    screen.blit(background, (0, 0))

    bird_group.update()
    bird_group.draw(screen)

    pipe_group.update()
    pipe_group.draw(screen)

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        game_over()
        running = False

    if bird_group.sprites()[0].rect.y >= HEIGHT or bird_group.sprites()[0].rect.y <= 0:
        game_over()
        running = False

    if len(pipe_group) < 3:
        if len(pipe_group) == 0:
            new_pipe_x = WIDTH + 10
        else:
            new_pipe_x = pipe_group.sprites()[-1].rect.x + PIPE_WIDTH + 200

        pipe_group.add(Pipe(new_pipe_x))

    if pipe_group.sprites()[0].rect.x <= -PIPE_WIDTH:
        pipe_group.remove(pipe_group.sprites()[0])
        score += 1

    pygame.display.flip()

pygame.quit()
