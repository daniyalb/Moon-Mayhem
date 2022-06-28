from re import I
from numpy import square
import pygame, math, random

pygame.init()
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/misc/icon.png')
BACKGROUND = pygame.image.load('Assets/misc/background.jpg')
BAR = pygame.image.load('Assets/misc/bar.png')
BAR = pygame.transform.scale(BAR, (WIDTH, 50))
LASER = pygame.image.load('Assets/misc/laser.png')
HEALTH = pygame.transform.scale(pygame.image.load('Assets/misc/health_title.png'
                                                  ), (103, 19))
HEART = pygame.transform.scale(pygame.image.load('Assets/misc/heart.png'), (32,
                                                                            32))
CHEST = pygame.transform.scale(pygame.image.load('Assets/misc/chest.png'), (66, 64))
PLATFORM = pygame.transform.scale(pygame.image.load('Assets/misc/platform.png'), (188, 144))
PLATFORM_RECT = PLATFORM.get_rect()
PLATFORM_RECT.topleft = (WIDTH // 2 - 94, 30)
LASER_SOUND = pygame.mixer.Sound('Assets/sounds/laser_sound.wav')
LASER_SOUND.set_volume(0.2)
RELOAD_SOUND = pygame.mixer.Sound('Assets/sounds/reload.wav')
BUY_SOUND = pygame.mixer.Sound('Assets/sounds/buy.wav')
EXPLOSION_SOUND = pygame.mixer.Sound('Assets/sounds/explosion_sound.wav')
TIMER_SOUND = pygame.mixer.Sound('Assets/sounds/timer.wav')
WAVE_START = pygame.mixer.Sound('Assets/sounds/wave_start.wav')
WAVE_FINISH = pygame.mixer.Sound('Assets/sounds/wave_complete.wav')
CHARACTER_STILL = pygame.image.load('Assets/character/char_still.png')
CHARACTER_RIGHT = pygame.image.load('Assets/character/char_right.png')
CHARACTER_LEFT = pygame.image.load('Assets/character/char_left.png')
CHAR_HIT = pygame.mixer.Sound('Assets/sounds/player_hit.wav')
NO_AMMO = pygame.mixer.Sound('Assets/sounds/no_ammo.wav')
CHAR_DIM = 128
SPEED = 5
BULL_VEL = 6
GUN_AMMO = 32
AMMO_COST = 20
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
pygame.display.set_caption("Moon Mayhem 2")
pygame.display.set_icon(ICON)
FPS = 60
FONT = pygame.font.Font('Assets/misc/font.ttf', 34)
FONT_SMALL = pygame.font.Font('Assets/misc/font.ttf', 24)
FONT_BOLD = pygame.font.Font('Assets/misc/bold_font.ttf', 34)
FONT_BOLD_LARGE = pygame.font.Font('Assets/misc/bold_font.ttf', 54)


def init_enemy_sprites() -> tuple[list]:
    """ Initialize the sprites for enemies as well as their animations and return
    them in a tuple of lists.
    """
    worm_sprites = get_sprites(9, 'Assets/enemies/worm/worm', '.png', 100, 100)
    bat_sprites = get_sprites(8, 'Assets/enemies/bat/bat', '.png', 82, 66)
    mushroom_sprites = get_sprites(8, 'Assets/enemies/mushroom/mushroom', '.png', 63, 98)
    mushroom_explode_sprites = get_sprites(4, 'Assets/enemies/mushroom/exploding/explode',
                                             '.png', 63, 98)
    explosion_sprites = get_sprites(12, 'Assets/enemies/mushroom/explosion/explosion', '.png', 189, 192)
    hit_sprites = get_sprites(28, 'Assets/enemies/enemy_hit/', '.png', 300, 300)
    death_sprites = get_sprites(30, 'Assets/enemies/enemy_death/', '.png', 300, 300)

    return (worm_sprites, bat_sprites, mushroom_sprites, mushroom_explode_sprites, explosion_sprites, hit_sprites, death_sprites)


def get_sprites(number_images: int, dir: str, type: str, x_dim: int, y_dim: int) -> list:
    """ A helper function for init_enemy_sprites() which takes the number of images 
    <number_images> of the sprtie, the directory <dir> of these images, their file 
    type <type>, as well as the x and y dimensions of the actual enemy sprite, 
    <x_dim> and <y_dim> respectively. The function loads these images and adds them
    to a list with the proper scaling, and returns this list.
    """
    sprite_list = []
    for i in range(1, number_images + 1):
        sprite = pygame.image.load(dir + str(i) + type)
        sprite = pygame.transform.scale(sprite, (x_dim, y_dim))
        sprite_list.append(sprite)
    return sprite_list


WORM_SPRITES, BAT_SPRITES, MUSHROOM_SPRITES, MUSHROOM_EXPLODE_SPRITES, EXPLOSION_SPRTIES, HIT_SPRITES, DEATH_SPRITES = init_enemy_sprites()
ENEMY_HIT = pygame.mixer.Sound('Assets/sounds/enemy_hit.wav')
ENEMY_DEATH = pygame.mixer.Sound('Assets/sounds/enemy_death.wav')
ENEMY_SPEED = 1


class Bullet:
    """ The bullet class in this game.
    
    This class handles the creation of a bullet to be used in the Player
    class.

    === Public Attributes ===
    rect: 
         the pygame rectangle for this bullet
    x_vel:
         The velocity of this bullet in the x direction
    y_vel:
         The velocity of this bullet in the y direction
    """

    rect: pygame.Rect
    x_vel: float
    y_vel: float

    def __init__(self, char_center, mx, my) -> None:
        self.rect = LASER.get_rect()
        x, y = char_center
        self.rect.center = char_center
        angle = math.atan2(y - my, x - mx)
        self.x_vel = math.cos(angle) * BULL_VEL
        self.y_vel = math.sin(angle) * BULL_VEL
        LASER_SOUND.play()


class Player:
    """ The player character in the game.

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
    money:
         An integer representing the amount of money the player currently has
    ammo:
         The total amount of ammo this player has remaining
    curr_ammo:
         The amount of ammo in the player's gun right now
    need_reload:
         A boolean variable to track if the player needs to reload their gun
    out_of_ammo:
         A boolean variable to track if the player is out of ammo
    at_buy_platform:
         A boolean variable to track if the player is standing within the
         buy platform
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
    # _last_update_health:
    #     An integer that tracks when the last time player health checked and
    #     increased if it was less than 5
    # _money_gain:
    #     A list containing tuples indicating where an enemy was killed in
    #     order to display the money gained for this kill at that spot

    sprite: pygame.Surface
    rect: pygame.Rect
    health: int
    bullets: list[Bullet]
    money: int
    ammo: int
    curr_ammo: int
    need_reload: bool
    out_of_ammo: bool
    at_buy_platform: bool
    has_funds: bool
    _move_sprites: list[pygame.Surface]
    _curr_move_sprite: int
    _death_sprites: list[pygame.Surface]
    _last_updated: int
    _last_update_damage: int
    _last_update_health: int
    _money_gain: list[tuple]

    def __init__(self) -> None:
        self.sprite = CHARACTER_STILL
        self._move_sprites = [CHARACTER_RIGHT, CHARACTER_LEFT]
        self._curr_move_sprite = 0
        self._get_death_sprites()
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self._last_updated = 0
        self._last_update_damage = 0
        self._last_update_health = 0
        self._money_gain = []
        self.bullets = []
        self.health = 5
        self.money = 0
        self.ammo = GUN_AMMO * 2
        self.curr_ammo = GUN_AMMO
        self.need_reload = False
        self.out_of_ammo = False
        self.at_buy_platform = False
        self.has_funds = False

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
        if key_pressed[pygame.K_s] and self.rect.bottom <= HEIGHT - 50:
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

    def _get_death_sprites(self) -> None:
        """ Load in the sprites representing blood when the character dies
        and place them all into a list <self._death_sprties>
        """
        self._death_sprites = []
        for i in range(1, 23):
            sprite = pygame.image.load('Assets/character/character_death/' + str(
                i) + '.png')
            self._death_sprites.append(sprite)

    def get_rotated(self, rotation: float) -> pygame.Surface:
        """Rotate the character surface according to the <rotation> value and
        return
        this surface
        """
        return pygame.transform.rotate(self.sprite, rotation)

    def _no_ammo(self) -> None:
        if self.ammo < 1:
            self.out_of_ammo = True
        else:
            self.need_reload = True

        NO_AMMO.play()

    def shoot_bullet(self, mx: int, my: int) -> None:
        """Handle the shooting of a bullet"""
        if self.curr_ammo > 0:
            bullet = Bullet(self.rect.center, mx, my)
            self.curr_ammo -= 1
            if self.ammo > 0:
                self.ammo -= 1
            self.bullets.append(bullet)
        else:
            self._no_ammo()

    def _handle_bullets(self, bullet: Bullet,
                        enemies: list) -> None:
        """Handle bullet collisions
        """
        if bullet.rect.x <= 0 or bullet.rect.x >= WIDTH or bullet.rect.y <= 0 or \
                bullet.rect.y >= HEIGHT:
            self.bullets.remove(bullet)
        else:
            removed_once = False
            for enemy in enemies:
                if not removed_once and enemy.rect.colliderect(bullet.rect) and not enemy.dead:
                    enemy.damage()
                    if enemy.dead:
                        self.add_money()
                        self._money_gain.append((enemy.rect.x, enemy.rect.y, 100))
                    self.bullets.remove(bullet)
                    removed_once = True

    def draw_bullets(self, enemies: list) -> None:
        """Draws the bullets at their current location
        """
        for bullet in self.bullets:
            bullet.rect.x -= bullet.x_vel
            bullet.rect.y -= bullet.y_vel
            WINDOW.blit(LASER, (bullet.rect.x, bullet.rect.y))
            self._handle_bullets(bullet, enemies)

    def draw_ammo(self) -> None:
        ammo_text = FONT.render('Ammo: ' + str(self.curr_ammo) + ' / ' + str(GUN_AMMO), False, WHITE)
        WINDOW.blit(ammo_text, (WIDTH - 225, HEIGHT - 130))
        total_text = FONT_SMALL.render('Total Ammo: ' + str(self.ammo), False, WHITE)
        WINDOW.blit(total_text, (WIDTH - 195, HEIGHT - 90))

        if self.need_reload:
            reload_text = FONT_SMALL.render('PRESS "R" TO RELOAD!', False, RED)
            WINDOW.blit(reload_text, (WIDTH - 235, HEIGHT - 155))
        elif self.out_of_ammo:
            reload_text = FONT_SMALL.render('OUT OF AMMO! BUY MORE!', False, RED)
            WINDOW.blit(reload_text, (WIDTH - 285, HEIGHT - 155))

    def reload(self) -> None:
        if self.ammo <= 32:
            self.curr_ammo += self.ammo
        else:
            self.curr_ammo = 32

        self.need_reload = False
        RELOAD_SOUND.play()

    def draw_hearts(self) -> None:
        """Display the hearts representing the player's health
        """
        x, y = WIDTH - 48, HEIGHT - 40
        for i in range(1, self.health + 1):
            WINDOW.blit(HEART, (x, y))
            x -= 48

    def check_damage(self, enemy) -> None:
        """ Check if this <enemy> has collided with the player, and if they
        did, lower the players health"""
        now = pygame.time.get_ticks()

        if isinstance(enemy, Mushroom) and self.rect.colliderect(enemy) and \
             enemy.exploded and not enemy.player_damaged:
            self.health -= enemy.player_damage
            enemy.player_damaged = True
        elif now - self._last_update_damage > 1000:
            if self.rect.colliderect(enemy) and not enemy.dead:
                self.health -= enemy.player_damage
                CHAR_HIT.play()
                self._last_update_damage = now

    def update_health(self) -> None:
        """ Use a clock to determine when the player's health should be increased
        and only increase health if self.health < 5
        """
        now = pygame.time.get_ticks()
        if now - self._last_update_health > 3000:
            self._last_update_health = now
            if self.health < 5:
                self.health += 1

    def add_money(self) -> None:
        """ Add money to this player for killing an enemy
        """
        self.money += 10

    def display_money(self) -> None:
        money_text = FONT.render('Money: $' + str(self.money), False, WHITE)
        WINDOW.blit(money_text, (20, HEIGHT - 50))

        for i in range(len(self._money_gain)):
            kill_text = FONT_SMALL.render('+ $10', False, YELLOW)
            WINDOW.blit(kill_text, (self._money_gain[i][0], self._money_gain[i][1]))
            self._money_gain[i] = (self._money_gain[i][0], self._money_gain[i][1], self._money_gain[i][2] - 1)

        for kill in self._money_gain:
            if kill[2] == 0:
                self._money_gain.remove(kill)

    def check_buy(self) -> None:
        self.at_buy_platform = False
        self.has_funds = False

        if self.rect.colliderect(PLATFORM_RECT):
            if self.money >= AMMO_COST:
                buy_text = FONT_SMALL.render('PRESS "B" TO BUY ' + str(GUN_AMMO) + ' AMMO ($' + str(AMMO_COST) + ')', False, YELLOW)
                x, y = PLATFORM_RECT.bottomleft
                x -= 70
                WINDOW.blit(buy_text, (x, y))
                self.at_buy_platform = True
                self.has_funds = True
            else:
                no_fund_text = FONT_SMALL.render('NOT ENOUGH MONEY FOR AMMO, NEED $' + str(AMMO_COST), False, YELLOW)
                x, y = PLATFORM_RECT.bottomleft
                x -= 130
                WINDOW.blit(no_fund_text, (x, y))
                self.at_buy_platform = True

    def buy_ammo(self) -> None:
        self.ammo += GUN_AMMO
        self.curr_ammo = GUN_AMMO
        self.money -= AMMO_COST
        self.out_of_ammo = False
        BUY_SOUND.play()


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
    player_damage:
         The amount of damage this enemy causes to the player
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
    # _update_animation:
    #    An integer that represents the amount of frames between when
    #    the sprite animations are changed

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    player_damage: int
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _update_animation: int
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
        self._update_animation = 200
        self.health = 3
        self.player_damage = 1
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

        if now - self._last_updated > self._update_animation:
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
    player_damage:
         The amount of damage this enemy causes to the player
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
    # _update_animation:
    #    An integer that represents the amount of frames between when
    #    the sprite animations are changed

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    player_damage: int
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _update_animation: int
    _death_sprites: list[pygame.Surface]
    _enemy_sprites: list[pygame.Surface]
    _hit_sprites: list[pygame.Surface]

    def __init__(self) -> None:
        Enemy.__init__(self)
        self._enemy_sprites = WORM_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.spawn()

    def move(self, x: int, y: int) -> None:
        if self.rect.x <= x:
            self.rect.x += ENEMY_SPEED
        else:
            self.rect.x -= ENEMY_SPEED

        if self.rect.y <= y:
            self.rect.y += ENEMY_SPEED
        else:
            self.rect.y -= ENEMY_SPEED


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
    player_damage:
         The amount of damage this enemy causes to the player
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
    # _update_animation:
    #    An integer that represents the amount of frames between when
    #    the sprite animations are changed

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    player_damage: int
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _last_update_movement: int
    _update_animation: int
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

class Mushroom(Enemy):
    """The Mushroom Enemy class for this game.

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
    player_damage:
         The amount of damage this enemy causes to the player
    exploded:
         A boolean which indicates whether this enemy has began their
         explosion or not
    player_damaged:
         A boolean to track if this enemy's explosion has damaged the player
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
    # _last_update_explode:
    #     An integer mean to keep track of the frame when this enemy's
    #     explosion timer was last updated
    # _curr_hit_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_hit_sprites> is selected
    # _curr_death_sprite:
    #     An integer meant to signify the index of which sprite in
    #     <_death_sprites> is selected
    # _update_animation:
    #    An integer that represents the amount of frames between when
    #    the sprite animations are changed
    # _sprite_changed:
    #    A boolean variable that tracks if this enemy's sprite list in
    #    <self._enemy_sprites> has been changed or not
    # _close:
    #    A boolean which tracks if this enemy is within 100 pixels of the
    #    player

    rect: pygame.Rect
    curr_sprite: pygame.Surface
    health: int
    play_hit_animation: bool
    dead: bool
    remove: bool
    player_damage: int
    exploded: bool
    player_damaged: bool
    _facing: str
    _last_updated: int
    _curr_frame_sprite: int
    _curr_hit_sprite: int
    _curr_death_sprite: int
    _last_update_hit: int
    _last_update_dead: int
    _last_update_explode: int
    _update_animation: int
    _sprite_changed: bool
    _close: bool
    _death_sprites: list[pygame.Surface]
    _enemy_sprites: list[pygame.Surface]
    _hit_sprites: list[pygame.Surface]

    def __init__(self) -> None:
        Enemy.__init__(self)
        self._enemy_sprites = MUSHROOM_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.exploded = False
        self.player_damaged = False
        self._update_animation = 150
        self._last_update_explode = 0
        self._sprite_changed = False
        self._close = False
        self.spawn()

    def move(self, x: int, y: int) -> None:
        self._close_to_player(x, y)

        if not self._close:
            if self.rect.x <= x:
                self.rect.x += ENEMY_SPEED
            else:
                self.rect.x -= ENEMY_SPEED

            if self.rect.y <= y:
                self.rect.y += ENEMY_SPEED
            else:
                self.rect.y -= ENEMY_SPEED
        else:
            self._change_sprite()
            self._explode()

    def _close_to_player(self, x: int, y: int) -> bool:
        """ Return whether this mushroom enemy is close enough
        to the player to explode
        """
        dx = abs(self.rect.x - x)
        dy = abs(self.rect.y - y)
        dist = math.sqrt((dx**2) + (dy**2))
        if dist <= 100.0:
            self._close = True

    def _change_sprite(self) -> None:
        """ Change the enemies sprites in <self._enemy_sprites> to
        a different list of sprites only once, also update the
        <self._last_update_explode> timer to the current frame
        """
        if not self._sprite_changed:
            self._enemy_sprites = MUSHROOM_EXPLODE_SPRITES
            self._last_update_explode = pygame.time.get_ticks()
            TIMER_SOUND.play()
            self._sprite_changed = True

    def _explode(self) -> None:
        """ A helper method that tracks the remaining frames left until
        this enemy explodes
        """
        now = pygame.time.get_ticks()

        if now - self._last_update_explode > 3000 and not self.exploded and not self.dead:
            self.player_damage = 3
            x, y = self.rect.center
            self._death_sprites = EXPLOSION_SPRTIES
            self.rect = self._death_sprites[0].get_rect()
            self.rect.center = (x, y)
            EXPLOSION_SOUND.play()
            self.dead = True
            self.exploded = True

    def death_animation(self, window: pygame.Surface) -> None:
        TIMER_SOUND.stop()
        if self.exploded:
            now = pygame.time.get_ticks()
            window.blit(self._death_sprites[self._curr_death_sprite], self.rect.topleft)
            if now - self._last_update_dead > 60:
                self._last_update_dead = now
                self._curr_death_sprite = (self._curr_death_sprite + 1) % len(
                    self._death_sprites)
            if self._curr_death_sprite == 11:
                self.remove = True
        else:
            Enemy.death_animation(self, window)

    
class Wave:
    """ The Wave class for this game.
    
    This class is responsible for the starting and ending of waves, 
    determining the number of enemies to spawn, and tracking how many 
    enemies are left.

    === Public Attributes ===
    wave:
         An integer which tracks which wave the game is currently on
    enemies:
         A list of enemies of the Enemy class that are spawned in the 
         current wave
    """
    # === Private Attributes ===
    # _last_update_start:
    #    An integer meant ot keep track of the frame in which the wave
    #    start animation was last updated
    # _last_update_complete:
    #    An integer meant ot keep track of the frame in which the wave
    #    completion animation was last updated

    wave: int
    enemies: list
    begin: bool
    start_wave_anim: bool
    wave_complete: bool

    def __init__(self) -> None:
        self.wave = 0
        self.enemies = []
        self.begin = False
        self.start_wave_anim = False
        self.wave_complete = False
        self.wave_commenced = False
        self._last_update_start = 0
        self._last_update_complete = 0
        self.curr_enemies = 0

    def begin_waves(self) -> None:
        self.begin = True
        self.start_wave()

    def request_wave_start(self) -> None:
        wave = str(self.wave + 1)
        if wave[-1] == '0':
            wave += 'TH'
        elif len(wave) > 1 and wave == '11' or wave == '12' or wave == '13':
            wave += 'TH'
        elif wave[-1] == '1':
            wave += 'ST'
        elif wave[-1] == '2':
            wave += 'ND'
        elif wave[-1] == '3':
            wave += 'RD'
        else:
            wave += 'TH'
        wave_start_text = FONT_BOLD.render('PRESS "SPACEBAR" TO START THE ' + wave + ' WAVE', False, YELLOW)
        WINDOW.blit(wave_start_text, (10, 620))

    def start_wave(self) -> None:
        self.wave += 1
        self.start_wave_anim = True
        self._init_enemies()
        self.wave_commenced = True
        self._last_update_start = pygame.time.get_ticks()
        WAVE_START.play()

    def wave_start_animation(self) -> None:
        start_text_back = FONT_BOLD_LARGE.render('STARTING WAVE ' + str(self.wave), False, BLACK)
        WINDOW.blit(start_text_back, (410, 605))
        start_text = FONT_BOLD_LARGE.render('STARTING WAVE ' + str(self.wave), False, WHITE)
        WINDOW.blit(start_text, (415, 600))
        
        now = pygame.time.get_ticks()
        if now - self._last_update_start > 4000:
            self.start_wave_anim = False

    def _init_enemies(self) -> None:
        num_enemies = self.wave + 2
        i = 0
        while i < num_enemies:
            random_num = random.randint(1, 3)
            if random_num == 1:
                self.enemies.append(Worm())
            elif random_num == 2:
                self.enemies.append(Bat())
            else:
                self.enemies.append(Mushroom())
            i += 1

        self.curr_enemies = len(self.enemies)

    def handle_enemies(self, char: Player) -> None:
        for enemy in self.enemies:
            if enemy.remove:
                self.enemies.remove(enemy)
            else:
                enemy.animate(char.rect.x, char.rect.y)
                enemy.move(char.rect.centerx, char.rect.centery)
                char.check_damage(enemy)

        self.curr_enemies = len(self.enemies)

        if not self.wave_complete:
            self._wave_status()

    def _wave_status(self) -> None:
        if len(self.enemies) == 0:
            self.wave_complete = True
            self.wave_commenced = False
            self._last_update_complete = pygame.time.get_ticks()
            WAVE_FINISH.play()

    def enemy_animations(self) -> None:
        for enemy in self.enemies:
            if not enemy.dead:
                WINDOW.blit(enemy.curr_sprite, (enemy.rect.x, enemy.rect.y))
                enemy.draw_health(WINDOW)
                if enemy.play_hit_animation:
                    enemy.hit_animation(WINDOW)
            else:
                enemy.death_animation(WINDOW)

    def wave_complete_anim(self) -> None:
        complete_text_back = FONT_BOLD_LARGE.render('WAVE COMPLETE!', False, BLACK)
        WINDOW.blit(complete_text_back, (410, 605))
        complete_text = FONT_BOLD_LARGE.render('WAVE COMPLETE!', False, WHITE)
        WINDOW.blit(complete_text, (415, 600))
        
        now = pygame.time.get_ticks()
        if now - self._last_update_complete > 4000:
            self.wave_complete = False
            self.begin = False

    def show_remaining(self) -> None:
        remaining_text = FONT.render('Enemies Remaining: ' + str(self.curr_enemies), False, WHITE)
        WINDOW.blit(remaining_text, (375, 670))


def draw_window(wave: Wave, char: Player, rotation: float):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(PLATFORM, PLATFORM_RECT.topleft)
    WINDOW.blit(CHEST, (WIDTH // 2 - 33, 60))
    curr_char = char.get_rotated(rotation)
    char.draw_bullets(wave.enemies)
    WINDOW.blit(curr_char, char.rect.topleft)
    wave.enemy_animations()
    WINDOW.blit(BAR, (0, HEIGHT - 50))
    WINDOW.blit(HEALTH, (WIDTH - 355, HEIGHT - 35))
    char.check_buy()
    char.draw_hearts()
    char.display_money()
    char.draw_ammo()
    if not wave.begin:
        wave.request_wave_start()
    elif wave.start_wave_anim:
        wave.wave_start_animation()
    elif wave.wave_commenced:
        wave.show_remaining()
    elif wave.wave_complete:
        wave.wave_complete_anim()
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player()
    wave = Wave()
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not wave.begin:
                    wave.begin_waves()
                if event.key == pygame.K_r and char.need_reload:
                    char.reload()
                if event.key == pygame.K_b and char.at_buy_platform and char.has_funds:
                    char.buy_ammo()

        key_pressed = pygame.key.get_pressed()
        char.move(key_pressed)
        char.update_health()

        if wave.wave_commenced:
            wave.handle_enemies(char)

        draw_window(wave, char, rotation)
    pygame.quit()


if __name__ == "__main__":
    main()
