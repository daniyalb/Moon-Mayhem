from lib2to3.pygram import python_grammar_no_print_statement
import py
import pygame
import math
import random

pygame.init()
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/misc/icon.png')
BACKGROUND = pygame.image.load('Assets/misc/background.jpg')
BAR = pygame.image.load('Assets/misc/bar.png')
BAR = pygame.transform.scale(BAR, (WIDTH, 50))
LASER = pygame.image.load('Assets/misc/laser.png')
HEART = pygame.transform.scale(pygame.image.load('Assets/misc/heart.png'), (32, 32))
LASER_SOUND = pygame.mixer.Sound('Assets/sounds/laser_sound.wav')
LASER_SOUND.set_volume(0.2)
ENEMY_HIT = pygame.mixer.Sound('Assets/sounds/enemy_hit.wav')
ENEMY_DEATH = pygame.mixer.Sound('Assets/sounds/enemy_death.wav')
CHARACTER_STILL = pygame.image.load('Assets/character/char_still.png')
CHARACTER_RIGHT = pygame.image.load('Assets/character/char_right.png')
CHARACTER_LEFT = pygame.image.load('Assets/character/char_left.png')
CHAR_HIT = pygame.mixer.Sound('Assets/sounds/player_hit.wav')
CHAR_DIM = 128
SPEED = 5
BULL_VEL = 6
ENEMY_SPEED = 1
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
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
    bullets:
         A list containing tuples representing the bullets this player has
         shot
    """
    # === Private Attributes ==
    # _move_sprites:
    #     a list of the two image surfaces that represent the player moving
    # _curr_move_sprite:
    #     An index number for which movement sprite is currently selected
    # _death_sprites:
    #    A list of sprites representing blood when the player dies
    # _last_updated:
    #     An integer mean to keep track of the frame when the player
    #     animation was last updated
    # _last_update_damage:
    #     An integer that tracks when the last time collisions were detected
    #     between the player and enemies

    sprite: pygame.Surface
    rect: pygame.Rect
    health: int
    bullets: list[tuple[pygame.Rect, float, float]]
    _move_sprites: list[pygame.Surface]
    _curr_move_sprite: int
    _death_sprites: list[pygame.Surface]
    _last_updated: int
    _last_update_damage: int

    def __init__(self) -> None:
        self.sprite = CHARACTER_STILL
        self._move_sprites = [CHARACTER_RIGHT, CHARACTER_LEFT]
        self._curr_move_sprite = 0
        self._get_death_sprites()
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self._last_updated = 0
        self._last_update_damage = 0
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

    def _get_death_sprites(self) -> None:   # TODO: Implement player death
        """ Load in the sprites representing blood when the character dies
        and place them all into a list <self._death_sprties>
        """
        self._death_sprites = []
        for i in range(1, 23):
            sprite = pygame.image.load('Assets/character/character_hit/' + str(i) + '.png')
            self._death_sprites.append(sprite)

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

    def _handle_bullets(self, bullet: tuple[pygame.Rect, int, int], 
                        enemies: list) -> None:
        """Handle bullet collisions
        """
        if bullet[0].x <= 0 or bullet[0].x >= WIDTH or bullet[0].y <= 0 or bullet[0].y >= HEIGHT:
            self.bullets.remove(bullet)
        for enemy in enemies:
            if enemy.rect.colliderect(bullet[0]) and not enemy.dead:
                self.bullets.remove(bullet)
                enemy.damage()

    def draw_bullets(self, window: pygame.surface, enemies: list) -> None:
        """Draws the bullets at their current location
        """
        for bullet in self.bullets:
            bullet[0].x -= bullet[1]
            bullet[0].y -= bullet[2]
            window.blit(LASER, (bullet[0].x, bullet[0].y))
            self._handle_bullets(bullet, enemies)

    def draw_hearts(self, window: pygame.surface) -> None:
        """Display the hearts representing the player's health
        """
        x, y = WIDTH - 48, HEIGHT - 40
        for i in range(1, self.health + 1):
            window.blit(HEART, (x, y))
            x -= 48

    def check_damage(self, enemy) -> None:
        """ Check if this <enemy> has collided with the player, and if they
        did, lower the players health"""
        now = pygame.time.get_ticks()
        if now - self._last_update_damage > 1000:
            if self.rect.colliderect(enemy) and not enemy.dead:
                self.health -= 1
                CHAR_HIT.play()
            self._last_update_damage = now


class Enemy:
    """The Enemy class for this game.

    This class handles the drawing of, spawning in, and health and damage
    caused by the enemies.

    === Public Attributes ===
    rect:
         The pygame rectangle for this enemy
    curr_sprite:
         The sprite which is currently selected and is being displayed on the screen
    health:
         The amount of health, or lives, this enemy has
    play_hit_animation:
         A boolean variable that is checked to see if the enemy hit animation
         should be played
    dead:
         A boolean indicating whether the enemy is dead (True) or alive (false)
    remove:
         A boolean indicating whether this enemy should be removed from the enemy
         list in the main() function
    """
    # === Private Attributes ===
    # _enemy_sprites:
    #     A list containing the various sprites of the enemies
    # _facing:
    #     A string that represents the direction this enemy's sprite is currently facing
    # _last_updated:
    #     An integer mean to keep track of the frame when this enemy's
    #     animation was last updated
    # _curr_frame_sprite:
    #     An integer meant to signify the index of which sprite in <_enemy_sprites>
    #     is selected
    # _hit_sprites:
    #     A list of sprites representing the blood when this enemy is hot
    # _death_sprites:
    #    A list of sprites representing the blood when this enemy dies
    # _last_update_hit:
    #     An integer mean to keep track of the frame when this enemy's
    #     hit animation was last updated
    # _last_update_dead:
    #     An integer mean to keep track of the frame when this enemy's
    #     death animation was last updated
    # _curr_hit_sprite:
    #     An integer meant to signify the index of which sprite in <_hit_sprites>
    #     is selected
    # _curr_death_sprite:
    #     An integer meant to signify the index of which sprite in <_death_sprites>
    #     is selected

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    hit_sprites: list[pygame.Surface]
    dead: bool
    remove: bool
    _enemy_sprites: list
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _death_sprites: list[pygame.Surface]
    _last_update_hit: int
    _last_update_dead: int

    def __init__(self) -> None:
        self._last_updated = 0
        self._curr_frame_sprite = 0
        self._last_update_hit = 0
        self._last_update_dead = 0
        self._curr_hit_sprite = 0
        self._curr_death_sprite = 0
        self.health = 3
        self._facing = 'right'
        self.dead = False
        self.remove = False
        self._init_sprites()
        self._get_hit_sprites()
        self._get_death_sprites()
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.play_hit_animation = False
        self.spawn()

    def _get_hit_sprites(self) -> None:
        """ Initialize the sprites representing the blood when the enemy gets
        hit as pygame.Surface and place them into a list 
        <self._hit_sprites>
        """
        self.hit_sprites = []
        for i in range(1, 29):
            sprite = pygame.image.load('Assets/enemies/enemy_hit/' + str(i) + '.png')
            sprite = pygame.transform.scale(sprite, (300, 300))
            self.hit_sprites.append(sprite)

    def _init_sprites(self) -> None:
        """ Initialize the sprite with all of its animations into a list 
        <self._enemy_sprites>
        """
        self._enemy_sprites = []
        for i in range(1, 10):
            sprite = pygame.image.load('Assets/enemies/worm' + str(i) + '.png')
            sprite = pygame.transform.scale(sprite, (100, 100))
            self._enemy_sprites.append(sprite)

    def _get_death_sprites(self) -> None:
        """ Initialize the sprites representing the blood when the enemy dies
        as pygame.Surface and place them into a list <self._death_sprites>
        """
        self._death_sprites = []
        for i in range(1, 31):
            sprite = pygame.image.load('Assets/enemies/enemy_death/' + str(i) + '.png')
            sprite = pygame.transform.scale(sprite, (300, 300))
            self._death_sprites.append(sprite)

    def spawn(self) -> None:
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

    def damage(self) -> None:
        """ Register the fact that this enemy was damaged
        """
        self.health -= 1
        ENEMY_HIT.play()
        if self.health == 0:
            self.dead = True
            ENEMY_DEATH.play()
        else:
            self.play_hit_animation = True

    def hit_animation(self, window: pygame.Surface) -> None:
        now = pygame.time.get_ticks()

        if now - self._last_update_hit > 25:
            self._last_update_hit = now
            self._curr_hit_sprite = (self._curr_hit_sprite + 1) % len(self.hit_sprites)

        x, y = self.rect.topleft
        x -= 80
        y -= 80
        window.blit(self.hit_sprites[self._curr_hit_sprite], (x, y))
        
        if self._curr_hit_sprite == 27:
            self.play_hit_animation = False

    def death_animation(self, window: pygame.Surface) -> None:
        now = pygame.time.get_ticks()

        if now - self._last_update_dead > 25:
            self._last_update_dead = now
            self._curr_death_sprite = (self._curr_death_sprite + 1) % len(self._death_sprites)

        x, y = self.rect.topleft
        x -= 60
        y -= 60
        window.blit(self._death_sprites[self._curr_death_sprite], (x, y))
        
        if self._curr_death_sprite == 29:
            self.remove = True

    def draw_health(self, window: pygame.Surface) -> None:
        x1, y1 = self.rect.bottomleft
        x1 += 16
        y1 += 6
        x2, y2 = self.rect.bottomright
        x2 -= 16
        y2 += 6

        if self.health == 2:
            split = int((x2 - x1) * 0.66)
            split += x1
            pygame.draw.line(window, GREEN, (x1, y1), (split, y2), 4)
            pygame.draw.line(window, RED, (split, y1), (x2, y2), 4)
        elif self.health == 1:
            split = int((x2 - x1) * 0.33)
            split += x1
            pygame.draw.line(window, GREEN, (x1, y1), (split, y2), 4)
            pygame.draw.line(window, RED, (split, y1), (x2, y2), 4)
        else:
            pygame.draw.line(window, GREEN, (x1, y1), (x2, y2), 4)

    def animate(self, x: int, y: int) -> None:
        """ Animate the enemy by cycling through it's animation as it moves
        """
        now = pygame.time.get_ticks()

        if now - self._last_updated > 200:
            self._last_updated = now
            self._curr_frame_sprite = (self._curr_frame_sprite + 1) % len(self._enemy_sprites)
            if self._facing == 'right':
                self.curr_sprite = self._enemy_sprites[self._curr_frame_sprite]
            else:
                self.curr_sprite = pygame.transform.flip(self._enemy_sprites[self._curr_frame_sprite], True, False)
                
            if x < self.rect.x and self._facing == 'right':
                self.curr_sprite = pygame.transform.flip(self.curr_sprite, True, False)
                self._facing = 'left'
            elif x > self.rect.x and self._facing == 'left':
                self.curr_sprite = pygame.transform.flip(self.curr_sprite, True, False)
                self._facing = 'right'


def draw_window(char: Player, rotation: float, enemies: list):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(BAR, (0, HEIGHT - 50))
    curr_char = char.get_rotated(rotation)
    char.draw_bullets(WINDOW, enemies)
    WINDOW.blit(curr_char, (char.rect.x, char.rect.y))
    for enemy in enemies:
        if not enemy.dead:
            WINDOW.blit(enemy.curr_sprite, (enemy.rect.x, enemy.rect.y))
            enemy.draw_health(WINDOW)
            if enemy.play_hit_animation:
                enemy.hit_animation(WINDOW)
        else:
            enemy.death_animation(WINDOW)
    char.draw_hearts(WINDOW)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player()
    enemies = [Enemy()]
    pygame.mixer.music.load('Assets/sounds/background_music.wav')
    pygame.mixer.music.set_volume(0.6)
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

        for enemy in enemies:
            if enemy.remove:
                enemies.remove(enemy)
            else:
                enemy.animate(char.rect.x, char.rect.y)
                enemy.move(char.rect.x, char.rect.y)
                char.check_damage(enemy)
        
        draw_window(char, rotation, enemies)
    pygame.quit()


if __name__ == "__main__":
    main()