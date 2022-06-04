import pygame
import math

WIDTH, HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/icon.png')
BACKGROUND = pygame.image.load('Assets/background.jpg')
CHARACTER_SMALL = pygame.image.load('Assets/char_still.png')
CHAR_DIM = 128
SPEED = 3
pygame.display.set_caption("Moon Mayhem 2")
pygame.display.set_icon(ICON)
FPS = 60


def draw_window(astro, rotation: float):
    WINDOW.blit(BACKGROUND, (0, 0))
    curr_char = pygame.transform.rotate(pygame.transform.scale(CHARACTER_SMALL, (CHAR_DIM,
                                        CHAR_DIM)), rotation)
    WINDOW.blit(curr_char, (astro.x, astro.y))
    pygame.display.update()


def char_movement(key_pressed, astro) -> None:
    if key_pressed[pygame.K_a] and astro.left >= 0:
            astro.x -= SPEED
    if key_pressed[pygame.K_d] and astro.right <= WIDTH:
            astro.x += SPEED
    if key_pressed[pygame.K_w] and astro.top >= 0:
            astro.y -= SPEED
    if key_pressed[pygame.K_s] and astro.bottom <= HEIGHT:
            astro.y += SPEED


def main():
    astro = pygame.Rect(WIDTH // 2 - CHAR_DIM // 2, 
                        HEIGHT // 2 - CHAR_DIM // 2, CHAR_DIM, CHAR_DIM)

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key_pressed = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()
        dif_x, dif_y = mx - astro.centerx, my - astro.centery
        rotation = (180 / math.pi) * -math.atan2(dif_y, dif_x) - 90
        char_movement(key_pressed, astro)
        draw_window(astro, rotation)
    pygame.quit()


if __name__ == "__main__":
    main()