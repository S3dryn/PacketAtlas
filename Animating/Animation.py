import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True
xcoords = 300
ycoords = 400
while running:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                      running = False
                if event.key == pygame.K_w:
                      ycoords += 1
                elif event.key == pygame.K_s:
                      ycoords -= 1
                elif event.key == pygame.K_a:
                      xcoords -= 1
                elif event.key == pygame.K_d:
                      xcoords += 1
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(50,50,50),pygame.Rect(xcoords,ycoords,30,30))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()

    