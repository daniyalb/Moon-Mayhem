import pygame
import math

WIDTH, HEIGHT = 700, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/icon.png')
BACKGROUND = pygame.image.load('Assets/background.jpg')
CHARACTER_STILL = pygame.image.load('Assets/char_still.png')
CHARACTER_RIGHT = pygame.image.load('Assets/char_right.png')
CHARACTER_LEFT = pygame.image.load('Assets/char_left.png')
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
    # === Private Attributes ==
    # _move_sprites:
    #     a list of the two image surfaces that represent the character moving
    # _curr_move_sprite
    #     An index number for which movement sprite is currently selected
    sprite: pygame.Surface
    rect: pygame.Rect
    last_updated: int

    def __init__(self, CHARACTER: pygame.Surface) -> None:
        self.sprite = CHARACTER_STILL
        self._move_sprites = [CHARACTER_RIGHT, CHARACTER_LEFT]
        self._curr_move_sprite = 0
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self._last_updated = 0
    
    def move(self, key_pressed) -> None:
        """Move the character depending on which keys are pressed in key_pressed
        """
        moving = False
        if key_pressed[pygame.K_a] and self.rect.left >= 0:
            self.rect.centerx -= SPEED
            moving = True
        if key_pressed[pygame.K_d] and self.rect.right <= WIDTH:
            self.rect.centerx += SPEED
            moving = True
        if key_pressed[pygame.K_w] and self.rect.top >= 0:
            self.rect.centery -= SPEED
            moving = True
        if key_pressed[pygame.K_s] and self.rect.bottom <= HEIGHT:
            self.rect.centery += SPEED
            moving = True
        if moving:
            self.animate()
        else:
            self.sprite = CHARACTER_STILL
    
    def animate(self) -> None:
        """Animate the character by moving its legs when the character is moving"""
        now = pygame.time.get_ticks()
        if now - self._last_updated > 200:
            self._last_updated = now
            self._curr_move_sprite = (self._curr_move_sprite + 1) % len(self._move_sprites)
            self.sprite = self._move_sprites[self._curr_move_sprite]


    def get_rotated(self, rotation: float) -> pygame.Surface:
        """Rotate the character surface acording to the <rotation> value and return
        this surface
        """
        return pygame.transform.rotate(pygame.transform.scale(self.sprite, (CHAR_DIM,
                                        CHAR_DIM)), rotation)


def draw_window(char: Player, rotation: float):
    WINDOW.blit(BACKGROUND, (0, 0))
    curr_char = char.get_rotated(rotation)
    WINDOW.blit(curr_char, (char.rect.x, char.rect.y))
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player(CHARACTER_STILL)
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