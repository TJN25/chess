# Pygame test scrit
import pygame


height = 800
width = 600

def game():
    pygame.init()
    screen = pygame.display.set_mode((height, width))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    game()



