import pygame
import random

pygame.init()
WIDTH, HEIGHT = 1280, 720
ENEMY_HIT = pygame.mixer.Sound('Assets/sounds/enemy_hit.wav')
ENEMY_DEATH = pygame.mixer.Sound('Assets/sounds/enemy_death.wav')
ENEMY_SPEED = 1
GREEN = (0, 128, 0)
RED = (255, 0, 0)

def init_enemy_sprites() -> tuple:
    worm_sprites = []
    for i in range(1, 10):
        sprite = pygame.image.load('Assets/enemies/worm/worm' + str(i) + '.png')
        sprite = pygame.transform.scale(sprite, (100, 100))
        worm_sprites.append(sprite)

    bat_sprites = []
    for i in range(1, 9):
        sprite = pygame.image.load('Assets/enemies/bat/bat' + str(i) + '.png')
        sprite = pygame.transform.scale(sprite, (82, 66))
        bat_sprites.append(sprite)

    hit_sprites = []
    for i in range(1, 29):
        sprite = pygame.image.load('Assets/enemies/enemy_hit/' + str(i) +
                                    '.png')
        sprite = pygame.transform.scale(sprite, (300, 300))
        hit_sprites.append(sprite)

    death_sprites = []
    for i in range(1, 31):
        sprite = pygame.image.load('Assets/enemies/enemy_death/' + str(i) +
                                    '.png')
        sprite = pygame.transform.scale(sprite, (300, 300))
        death_sprites.append(sprite)

    return (worm_sprites, bat_sprites, hit_sprites, death_sprites)

WORM_SPRITES, BAT_SPRITES, HIT_SPRITES, DEATH_SPRITES = init_enemy_sprites()


class Enemy:
    """ The enemy class for this game.

    Do not instantiate this class, it is an abstract class.

    === Public Attributes ===
    rect:
         The pygame rectangle for this enemy
    curr_sprite:
         The sprite which is currently selected and is being displayed on the
         screen
    health:
         The amount of health, or lives, this enemy has
    play_hit_animation:
         A boolean variable that is checked to see if the enemy hit animation
         should be played
    dead:
         A boolean indicating whether the enemy is dead (True) or alive (false)
    remove:
         A boolean indicating whether this enemy should be removed from the
         enemy list in the main() function
    """
    # === Private Attributes ===
    # _enemy_sprites:
    #     A list containing the various sprites of the enemies
    # _facing:
    #     A string that represents the direction this enemy's sprite is
    #     currently facing
    # _last_updated:
    #     An integer mean to keep track of the frame when this enemy's
    #     animation was last updated
    # _curr_frame_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_enemy_sprites> is selected
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
    #     An integer meant to signify the index of which sprite in
    #     <_hit_sprites> is selected
    # _curr_death_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_death_sprites> is selected

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _death_sprites: list[pygame.Surface]
    _enemy_sprites: list[pygame.Surface]
    _hit_sprites: list[pygame.Surface]

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
        self._hit_sprites = HIT_SPRITES
        self._death_sprites = DEATH_SPRITES
        self.play_hit_animation = False

    def spawn(self) -> None:
        """ Spawn in this enemy somewhere outside of the viewable screen
        """
        x, y = 0, 0
        while (0 <= x <= WIDTH) and (0 <= y <= HEIGHT):
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
            self._curr_frame_sprite = (self._curr_frame_sprite + 1) % len(
                self._enemy_sprites)
            if self._facing == 'right':
                self.curr_sprite = self._enemy_sprites[self._curr_frame_sprite]
            else:
                self.curr_sprite = pygame.transform.flip(self._enemy_sprites[
                                        self._curr_frame_sprite], True, False)

            if x < self.rect.x and self._facing == 'right':
                self.curr_sprite = pygame.transform.flip(self.curr_sprite, True,
                                                         False)
                self._facing = 'left'
            elif x > self.rect.x and self._facing == 'left':
                self.curr_sprite = pygame.transform.flip(self.curr_sprite, True,
                                                         False)
                self._facing = 'right'

    def hit_animation(self, window: pygame.Surface) -> None:
        now = pygame.time.get_ticks()

        if now - self._last_update_hit > 25:
            self._last_update_hit = now
            self._curr_hit_sprite = (self._curr_hit_sprite + 1) % len(
                self._hit_sprites)

        x, y = self.rect.topleft
        x -= 80
        y -= 80
        window.blit(self._hit_sprites[self._curr_hit_sprite], (x, y))

        if self._curr_hit_sprite == 27:
            self.play_hit_animation = False

    def death_animation(self, window: pygame.Surface) -> None:
        now = pygame.time.get_ticks()

        if now - self._last_update_dead > 25:
            self._last_update_dead = now
            self._curr_death_sprite = (self._curr_death_sprite + 1) % len(
                self._death_sprites)

        x, y = self.rect.topleft
        x -= 60
        y -= 60
        window.blit(self._death_sprites[self._curr_death_sprite], (x, y))

        if self._curr_death_sprite == 29:
            self.remove = True


class Worm(Enemy):
    """The Worm Enemy class for this game.

    This class handles the drawing of, spawning in, and health and damage
    caused by this enemy.

    === Public Attributes ===
    rect:
         The pygame rectangle for this enemy
    curr_sprite:
         The sprite which is currently selected and is being displayed on the
         screen
    health:
         The amount of health, or lives, this enemy has
    play_hit_animation:
         A boolean variable that is checked to see if the enemy hit animation
         should be played
    dead:
         A boolean indicating whether the enemy is dead (True) or alive (false)
    remove:
         A boolean indicating whether this enemy should be removed from the
         enemy list in the main() function
    """
    # === Private Attributes ===
    # _enemy_sprites:
    #     A list containing the various sprites of the enemies
    # _facing:
    #     A string that represents the direction this enemy's sprite is
    #     currently facing
    # _last_updated:
    #     An integer mean to keep track of the frame when this enemy's
    #     animation was last updated
    # _curr_frame_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_enemy_sprites> is selected
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
    #     An integer meant to signify the index of which sprite in
    #     <_hit_sprites> is selected
    # _curr_death_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_death_sprites> is selected

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _death_sprites: list[pygame.Surface]
    _enemy_sprites: list[pygame.Surface]
    _hit_sprites: list[pygame.Surface]

    def __init__(self) -> None:
        Enemy.__init__(self)
        self._enemy_sprites = WORM_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.spawn()


class Bat(Enemy):
    """The Bat Enemy class for this game.

    This class handles the drawing of, spawning in, and health and damage
    caused by this enemy.

    === Public Attributes ===
    rect:
         The pygame rectangle for this enemy
    curr_sprite:
         The sprite which is currently selected and is being displayed on the
         screen
    health:
         The amount of health, or lives, this enemy has
    play_hit_animation:
         A boolean variable that is checked to see if the enemy hit animation
         should be played
    dead:
         A boolean indicating whether the enemy is dead (True) or alive (false)
    remove:
         A boolean indicating whether this enemy should be removed from the
         enemy list in the main() function
    """
    # === Private Attributes ===
    # _enemy_sprites:
    #     A list containing the various sprites of the enemies
    # _facing:
    #     A string that represents the direction this enemy's sprite is
    #     currently facing
    # _last_updated:
    #     An integer mean to keep track of the frame when this enemy's
    #     animation was last updated
    # _curr_frame_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_enemy_sprites> is selected
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
    # _last_update_movement:
    #     An integer mean to keep track of the frame when this enemy's
    #     movement was last updated
    # _curr_hit_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_hit_sprites> is selected
    # _curr_death_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_death_sprites> is selected

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _last_update_movement: int
    _death_sprites: list[pygame.Surface]
    _enemy_sprites: list[pygame.Surface]
    _hit_sprites: list[pygame.Surface]

    def __init__(self) -> None:
        Enemy.__init__(self)
        self._enemy_sprites = BAT_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self._last_update_movement = 0
        self._target_x, self._target_y = WIDTH // 2, HEIGHT // 2
        self._movement_update = random.randint(3000, 5000)
        self.spawn()

    def move(self, x: int, y: int) -> None:
        now = pygame.time.get_ticks()

        if now - self._last_update_movement > self._movement_update:
            self._last_update_movement = now
            self._movement_update = random.randint(3000, 5000)
            self._target_x = random.randint(x - 100, x + 100)
            self._target_y = random.randint(y - 100, y + 100)

        if self.rect.x <= self._target_x:
            self.rect.x += ENEMY_SPEED + 1
        else:
            self.rect.x -= ENEMY_SPEED + 1

        if self.rect.y <= self._target_y:
            self.rect.y += ENEMY_SPEED + 1
        else:
            self.rect.y -= ENEMY_SPEED + 1