import pygame
import math

WIDTH, HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/icon.png')
BACKGROUND = pygame.image.load('Assets/background.jpg')
CHARACTER = pygame.image.load('Assets/char_still.png')
CHAR_DIM = 128
SPEED = 3
pygame.display.set_caption("Moon Mayhem 2")
pygame.display.set_icon(ICON)
FPS = 60


class Player():
    """The player character in the game
    
    This class handles the drawing and movement of the character in the game, as well
    as the amount of ammo they have, money they've earned, and waves they've survived.

    === Public Attributes ==
    sprite:
        The sprite surface for the character
    character:
        The pygame rectangle representing the character
    """
    sprite: pygame.Surface
    rect: pygame.Rect

    def __init__(self, CHARACTER: pygame.Surface) -> None:
        self.rect = pygame.Rect(WIDTH // 2 - CHAR_DIM // 2,  # astro
                        HEIGHT // 2 - CHAR_DIM // 2, CHAR_DIM, CHAR_DIM)
        self.sprite = CHARACTER
    
    def move(self, key_pressed) -> None:
        """Move the character depending on which keys are pressed in key_pressed
        """
        if key_pressed[pygame.K_a] and self.rect.left >= 0:
            self.rect.x -= SPEED
        if key_pressed[pygame.K_d] and self.rect.right <= WIDTH:
            self.rect.x += SPEED
        if key_pressed[pygame.K_w] and self.rect.top >= 0:
            self.rect.y -= SPEED
        if key_pressed[pygame.K_s] and self.rect.bottom <= HEIGHT:
            self.rect.y += SPEED

    def get_rotated(self, rotation: float) -> pygame.Surface:
        """Rotate the character surface acording to the <rotation> value and return
        this surface
        """
        return pygame.transform.rotate(pygame.transform.scale(CHARACTER, (CHAR_DIM,
                                        CHAR_DIM)), rotation)


def draw_window(char: Player, rotation: float):
    WINDOW.blit(BACKGROUND, (0, 0))
    curr_char = char.get_rotated(rotation)
    WINDOW.blit(curr_char, (char.rect.x, char.rect.y))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player(CHARACTER)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key_pressed = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()
        dif_x, dif_y = mx - char.rect.centerx, my - char.rect.centery
        rotation = (180 / math.pi) * -math.atan2(dif_y, dif_x) - 90
        char.move(key_pressed)
        draw_window(char, rotation)
    pygame.quit()


if __name__ == "__main__":
    main()