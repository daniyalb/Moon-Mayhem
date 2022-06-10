import pygame
import math
import random

WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/misc/icon.png')
BACKGROUND = pygame.image.load('Assets/misc/background.jpg')
LASER = pygame.image.load('Assets/misc/laser.png')
HEART = pygame.transform.scale(pygame.image.load('Assets/misc/heart.png'), (32, 32))
pygame.mixer.init()
LASER_SOUND = pygame.mixer.Sound('Assets/sounds/laser_sound.wav')
LASER_SOUND.set_volume(0.2)
CHARACTER_STILL = pygame.image.load('Assets/character/char_still.png')
CHARACTER_RIGHT = pygame.image.load('Assets/character/char_right.png')
CHARACTER_LEFT = pygame.image.load('Assets/character/char_left.png')
CHAR_DIM = 128
SPEED = 5
BULL_VEL = 5
ENEMY_SPEED = 1
pygame.display.set_caption("Moon Mayhem 2")
pygame.display.set_icon(ICON)
FPS = 60


class Player():
    """The player character in the game.

    This class handles the drawing and movement of the character in the game, as
    well as the amount of ammo they have, money they've earned, and waves
    they've survived.

    === Public Attributes ==
    sprite:
         The sprite surface for the character
    rect:
         The pygame rectangle representing the character
    """
    # === Private Attributes ==
    # _move_sprites:
    #     a list of the two image surfaces that represent the character moving
    # _curr_move_sprite
    #     An index number for which movement sprite is currently selected
    # _last_updated:
    #     An integer mean to keep track of the frame when the character
    #     animation was last updated

    sprite: pygame.Surface
    rect: pygame.Rect
    health: int

    def __init__(self) -> None:
        self.sprite = CHARACTER_STILL
        self._move_sprites = [CHARACTER_RIGHT, CHARACTER_LEFT]
        self._curr_move_sprite = 0
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self._last_updated = 0
        self.bullets = []
        self.health = 5

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
        """Animate the character by moving its legs when the character is
        moving
        """
        now = pygame.time.get_ticks()
        if now - self._last_updated > 200:
            self._last_updated = now
            self._curr_move_sprite = (self._curr_move_sprite + 1) % len(
                self._move_sprites)
            self.sprite = self._move_sprites[self._curr_move_sprite]

    def get_rotated(self, rotation: float) -> pygame.Surface:
        """Rotate the character surface acording to the <rotation> value and
        return
        this surface
        """
        return pygame.transform.rotate(self.sprite, rotation)

    def shoot_bullet(self, mx: int, my: int) -> None:
        """Handle the shooting of a bullet"""
        bullet = LASER.get_rect()
        x, y = self.rect.center
        bullet.center = x, y
        angle = math.atan2(y - my, x - mx)
        x_vel = math.cos(angle) * BULL_VEL
        y_vel = math.sin(angle) * BULL_VEL
        LASER_SOUND.play()
        self.bullets.append((bullet, x_vel, y_vel))

    def _handle_bullets(self, bullet) -> None:
        """Handle bullet collisions
        """
        if bullet[0].x <= 0 or bullet[0].x >= WIDTH or bullet[0].y <= 0 or bullet[0].y >= HEIGHT:
            self.bullets.remove(bullet)

    def draw_bullets(self, window: pygame.surface) -> None:
        """Draws the bullets at their current location
        """
        for bullet in self.bullets:
            bullet[0].x -= bullet[1]
            bullet[0].y -= bullet[2]
            window.blit(LASER, (bullet[0].x, bullet[0].y))
            self._handle_bullets(bullet)

    def draw_hearts(self, window: pygame.surface) -> None:
        """Display the hearts representing the player's health
        """
        x, y = WIDTH - 48, HEIGHT - 48
        for i in range(1, self.health + 1):
            window.blit(HEART, (x, y))
            x -= 48


class Enemy:
    """The Enemy class for this game.

    This class handles the drawing of, spawning in, and health and damage
    caused by the enemies.

    === Public Attributes ===
    enemy_sprite:
         A list containing the various sprites of the enemies
    rect:
         The pygame rectangle for this enemy
    curr_sprite:
         The sprite which is currently selected and is being displayed on the screen
    """
    # === Private Attributes ===
    # _last_updated:
    #     An integer mean to keep track of the frame when the enemy
    #     animation was last updated
    # _curr_frame_sprite:
    #     An integer meant to signify the index of which sprite in <enemy_sprite>
    #     is selected

    enemy_sprites: list
    rect: pygame.Rect
    curr_sprite: pygame.Surface
    _last_updated: int
    _curr_frame_sprite: int

    def __init__(self, char_x: int, char_y: int) -> None:
        self._last_updated = 0
        self._curr_frame_sprite = 0
        self.init_sprites()
        self.curr_sprite = self.enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.spawn(char_x, char_y)

    def init_sprites(self) -> None:
        """ Initialize the sprite with all of its animations into a list 
        <self.enemy_sprites>
        """
        # add a randomizer to select a different sprite
        self.enemy_sprites = []
        for i in range(1, 10):
            sprite = pygame.image.load('Assets/enemies/worm' + str(i) + '.png')
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.enemy_sprites.append(sprite)

    def spawn(self, char_x: int, char_y: int) -> None:
        """ Spawn in this enemy somewhere outside of the viewable screen
        """
        x, y = 0, 0
        while (x >= 0 and x <= WIDTH) and (y >= 0 and y <= HEIGHT):
            x = random.randint(-500, WIDTH + 500)
            y = random.randint(-500, HEIGHT + 500)
        self.rect.center = (x, y)

    def move(self, x: int, y: int) -> None:
        if self.rect.x <= x:
            self.rect.x += ENEMY_SPEED
        else:
            self.rect.x -= ENEMY_SPEED

        if self.rect.y <= y:
            self.rect.y += ENEMY_SPEED
        else:
            self.rect.y -= ENEMY_SPEED

    def animate(self, x: int, y: int) -> None:
        """ Animate the enemy by cycling through it's animation as it moves
        """
        now = pygame.time.get_ticks()
        if now - self._last_updated > 200:
            self._last_updated = now
            self._curr_frame_sprite = (self._curr_frame_sprite + 1) % len(self.enemy_sprites)
            self.curr_sprite = self.enemy_sprites[self._curr_frame_sprite]


    # Continue building this class


def draw_window(char: Player, rotation: float, enemy: Enemy):
    WINDOW.blit(BACKGROUND, (0, 0))
    curr_char = char.get_rotated(rotation)
    char.draw_bullets(WINDOW)
    WINDOW.blit(curr_char, (char.rect.x, char.rect.y))
    WINDOW.blit(enemy.curr_sprite, (enemy.rect.x, enemy.rect.y))
    char.draw_hearts(WINDOW)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player()
    enemy = Enemy(char.rect.x, char.rect.y)
    pygame.mixer.music.load('Assets/sounds/background_music.wav')
    pygame.mixer.music.play(-1)
    while run:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        dif_x, dif_y = mx - char.rect.centerx, my - char.rect.centery
        rotation = (180 / math.pi) * -math.atan2(dif_y, dif_x) - 90
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    char.shoot_bullet(mx, my)
        key_pressed = pygame.key.get_pressed()
        char.move(key_pressed)
        enemy.animate(char.rect.x, char.rect.y)
        enemy.move(char.rect.x, char.rect.y)
        draw_window(char, rotation, enemy)
    pygame.quit()


if __name__ == "__main__":
    main()
