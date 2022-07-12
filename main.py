import pygame
import math
import random
# Main game variables
pygame.init()
WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
ICON = pygame.image.load('Assets/misc/icon.png')
pygame.display.set_caption("Moon Mayhem")
pygame.display.set_icon(ICON)
FPS = 60
# Main menu variables
MENU_BG = pygame.image.load('Assets/menu/BG.png')
START_BTN = pygame.image.load('Assets/menu/Start_BTN.png')
START_BTN_ACTIVE = pygame.image.load('Assets/menu/Start_BTN_A.png')
EXIT_BTN = pygame.image.load('Assets/menu/Exit_BTN.png')
EXIT_BTN_ACTIVE = pygame.image.load('Assets/menu/Exit_BTN_A.png')
TUT_BTN = pygame.image.load('Assets/menu/Tut_BTN.png')
TUT_BTN_ACTIVE = pygame.image.load('Assets/menu/Tut_BTN_A.png')
TITLE = pygame.image.load('Assets/menu/title.png')
MENU_MUSIC = pygame.mixer.Sound('Assets/sounds/menu.wav')
HIGHLIGHT = pygame.mixer.Sound('Assets/sounds/highlight.wav')
GAME_START = pygame.mixer.Sound('Assets/sounds/game_start.wav')
# Game over menu variables
GAME_OVER_TEXT = pygame.image.load('Assets/game_over/g_over_text.png')
GAME_OVER_BG = pygame.image.load('Assets/game_over/g_over_bg.png')
GAME_OVER_MUSIC = pygame.mixer.Sound('Assets/sounds/g_over.wav')
REPLAY_BTN = pygame.image.load('Assets/game_over/Replay_BTN.png')
REPLAY_BTN_ACTIVE = pygame.image.load('Assets/game_over/Replay_BTN_A.png')
MAIN_MENU_BTN = pygame.image.load('Assets/game_over/Menu_BTN.png')
MAIN_MENU_BTN_A = pygame.image.load('Assets/game_over/Menu_BTN_A.png')
# Active game variables
BACKGROUND = pygame.image.load('Assets/misc/background.jpg')
BAR = pygame.image.load('Assets/misc/bar.png')
BAR = pygame.transform.scale(BAR, (WIDTH, 50))
HEALTH = pygame.transform.scale(pygame.image.load('Assets/misc/health_title.png'
                                                  ), (103, 19))
HEART = pygame.transform.scale(pygame.image.load('Assets/misc/heart.png'), (32,
                                                                            32))
CHEST = pygame.transform.scale(pygame.image.load('Assets/misc/chest.png'), (66,
                                                                            64))
PLATFORM = pygame.transform.scale(pygame.image.load('Assets/misc/platform.png'),
                                  (188, 144))
PLATFORM_RECT = PLATFORM.get_rect()
PLATFORM_RECT.topleft = (WIDTH // 2 - 94, 30)
RED_ARROW = pygame.image.load('Assets/misc/arrow.png')
RED_ARROW = pygame.transform.scale(RED_ARROW, (64, 64))
WASD = pygame.image.load('Assets/misc/keys.png')
WASD = pygame.transform.scale(WASD, (181, 97))
CURSOR = pygame.image.load('Assets/misc/cursor.png')
CURSOR = pygame.transform.scale(CURSOR, (53, 53))
LASER = pygame.image.load('Assets/misc/laser.png')
LASER_SOUND = pygame.mixer.Sound('Assets/sounds/laser_sound.wav')
LASER_SOUND.set_volume(0.2)
RELOAD_SOUND = pygame.mixer.Sound('Assets/sounds/reload.wav')
BUY_SOUND = pygame.mixer.Sound('Assets/sounds/buy.wav')
EXPLOSION_SOUND = pygame.mixer.Sound('Assets/sounds/explosion_sound.wav')
TIMER_SOUND = pygame.mixer.Sound('Assets/sounds/timer.wav')
WAVE_START = pygame.mixer.Sound('Assets/sounds/wave_start.wav')
WAVE_FINISH = pygame.mixer.Sound('Assets/sounds/wave_complete.wav')
CHAR_HIT = pygame.mixer.Sound('Assets/sounds/player_hit.wav')
CHAR_HIT.set_volume(0.5)
CHAR_DEATH = pygame.mixer.Sound('Assets/sounds/player_dead.wav')
NO_AMMO = pygame.mixer.Sound('Assets/sounds/no_ammo.wav')
CHARACTER_STILL = pygame.image.load('Assets/character/char_still.png')
CHARACTER_RIGHT = pygame.image.load('Assets/character/char_right.png')
CHARACTER_LEFT = pygame.image.load('Assets/character/char_left.png')
CHAR_DIM = 128
SPEED = 5
BULL_VEL = 6
GUN_AMMO = 32
AMMO_COST = 30
# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
# Fonts
FONT = pygame.font.Font('Assets/misc/font.ttf', 34)
FONT_SMALL = pygame.font.Font('Assets/misc/font.ttf', 24)
FONT_BOLD = pygame.font.Font('Assets/misc/bold_font.ttf', 34)
FONT_BOLD_LARGE = pygame.font.Font('Assets/misc/bold_font.ttf', 54)


def init_enemy_sprites() -> tuple:
    """ Initialize the sprites for enemies as well as their animations and
    return them in a tuple of lists.
    """
    worm_sprites = get_sprites(9, 'Assets/enemies/worm/worm', '.png', 100, 100)
    bat_sprites = get_sprites(8, 'Assets/enemies/bat/bat', '.png', 82, 66)
    mushroom_sprites = get_sprites(8, 'Assets/enemies/mushroom/mushroom',
                                   '.png', 63, 98)
    mushroom_explode_sprites = \
        get_sprites(4, 'Assets/enemies/mushroom/exploding/explode', '.png',
                    63, 98)
    explosion_sprites = \
        get_sprites(12, 'Assets/enemies/mushroom/explosion/explosion', '.png',
                    189, 192)
    hit_sprites = get_sprites(28, 'Assets/enemies/enemy_hit/', '.png', 300, 300)
    death_sprites = get_sprites(30, 'Assets/enemies/enemy_death/', '.png',
                                300, 300)

    return (worm_sprites, bat_sprites, mushroom_sprites,
            mushroom_explode_sprites, explosion_sprites, hit_sprites,
            death_sprites)


def get_sprites(number_images: int, directory: str, f_type: str, x_dim: int,
                y_dim: int) -> list:
    """ A helper function for init_enemy_sprites() which takes the number of
    images <number_images> of the sprite, the directory <directory> of these
    images, their file type <f_type>, as well as the x and y dimensions of the
    actual enemy sprite, <x_dim> and <y_dim> respectively. The function loads
    these images and adds them to a list with the proper scaling, and returns
    this list.
    """
    sprite_list = []
    for i in range(1, number_images + 1):
        sprite = pygame.image.load(directory + str(i) + f_type)
        sprite = pygame.transform.scale(sprite, (x_dim, y_dim))
        sprite_list.append(sprite)
    return sprite_list


(WORM_SPRITES, BAT_SPRITES, MUSHROOM_SPRITES, MUSHROOM_EXPLODE_SPRITES,
 EXPLOSION_SPRITES, HIT_SPRITES, DEATH_SPRITES) = init_enemy_sprites()
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

    def __init__(self, char_center: tuple[int, int], mx: int, my: int) -> None:
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
    well as the amount of ammo they have, money they've earned, purchasing of
    ammo, shooting of bullets, bullet collisions with enemies, reloading of
    ammo, and the amount of health the player has and regeneration of it.

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
    dead:
         A boolean which tracks if this player is currently alive (False), or
         dead (True)
    full_dead:
         A boolean which shows if this player's death animation is complete
         (True) and that options to quit and retry the game can be shown
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
    # _last_update_dead:
    #    An integer which tracks the last frame when this player's death
    #    animation was updated
    # _curr_death_sprite:
    #    An integer which tracks the index of the death sprite is currently
    #    being displayed in the list of <_death_sprites>

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
    dead: bool
    full_dead: bool
    _move_sprites: list[pygame.Surface]
    _curr_move_sprite: int
    _curr_death_sprite: int
    _death_sprites: list[pygame.Surface]
    _last_updated: int
    _last_update_damage: int
    _last_update_health: int
    _last_update_dead: int
    _money_gain: list[tuple]

    def __init__(self) -> None:
        """ Initialize the attributes for this player.
        """
        self.sprite = CHARACTER_STILL
        self._move_sprites = [CHARACTER_RIGHT, CHARACTER_LEFT]
        self._curr_move_sprite = 0
        self._curr_death_sprite = 0
        self._get_death_sprites()
        self.rect = self.sprite.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self._last_updated = 0
        self._last_update_damage = 0
        self._last_update_health = 0
        self._last_update_dead = 0
        self._money_gain = []
        self._buy_station_arrow = RED_ARROW.get_rect()
        self._buy_station_arrow.topleft = (WIDTH // 2 - 32, 200)
        self._arrow_movement = -1
        self.bullets = []
        self.health = 5
        self.money = 0
        self.ammo = GUN_AMMO * 2
        self.curr_ammo = GUN_AMMO
        self.need_reload = False
        self.out_of_ammo = False
        self.at_buy_platform = False
        self.has_funds = False
        self.dead = False
        self.full_dead = False

    def move(self, key_pressed) -> None:
        """Move the character depending on which keys are pressed in
        <key_pressed> by adding or subtracting the x or y value of their
        <self.rect> position. Also handles the animation of the character if
        they are moving.
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
        """Animate the character by swapping between sprites of the character's
        legs moving to simulate walking
        """
        now = pygame.time.get_ticks()
        if now - self._last_updated > 200:
            self._last_updated = now
            self._curr_move_sprite = (self._curr_move_sprite + 1) % len(
                self._move_sprites)
            self.sprite = self._move_sprites[self._curr_move_sprite]

    def _get_death_sprites(self) -> None:
        """ Load in the sprites as pygame surfaces representing blood when the
        character dies and place them all into a list <self._death_sprites>
        """
        self._death_sprites = []
        for i in range(1, 23):
            sprite = pygame.image.load('Assets/character/character_death/' +
                                       str(i) + '.png')
            sprite = pygame.transform.scale(sprite, (256, 256))
            self._death_sprites.append(sprite)

    def get_rotated(self, rotation: float) -> pygame.Surface:
        """Rotate the character surface according to the <rotation> value and
        return this surface
        """
        return pygame.transform.rotate(self.sprite, rotation)

    def _no_ammo(self) -> None:
        """ A helper method for shoot_bullet() which determines if the player
        has enough ammo to reload or is out of ammo and changes the appropriate
        boolean variable to True.
        """
        if self.ammo < 1:
            self.out_of_ammo = True
        else:
            self.need_reload = True

        NO_AMMO.play()

    def shoot_bullet(self, mx: int, my: int) -> None:
        """Handle the shooting of a bullet by creating a Bullet object which
        contains the starting position of the bullet as well as the x and y
        position of the mouse when the bullet is shot if the player has enough
        ammo. If the player does not have enough ammo, determine what they need
        to do by calling the _no_ammo() method.
        """
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
        """ Handle bullet collisions, if the bullet leaves the screen, then
        remove it from the self.bullets list. If not, check if the bullet has
        collided with any of the currently alive enemies and remove the bullet
        if it has, as well as damage the enemy. If the enemy dies from this
        bullet collision, add money to this player.
        """
        if bullet.rect.x <= 0 or bullet.rect.x >= WIDTH or bullet.rect.y <= 0 \
                or bullet.rect.y >= HEIGHT:
            self.bullets.remove(bullet)
        else:
            removed_once = False
            for enemy in enemies:
                if not removed_once and enemy.rect.colliderect(bullet.rect) and\
                        not enemy.dead:
                    enemy.damage()
                    if enemy.dead:
                        self.add_money()
                        self._money_gain.append((enemy.rect.x, enemy.rect.y,
                                                 100))
                    self.bullets.remove(bullet)
                    removed_once = True

    def draw_bullets(self, enemies: list) -> None:
        """ Moves bullets according to they x and y velocity and draws the
        bullets at their current location.
        """
        for bullet in self.bullets:
            bullet.rect.x -= bullet.x_vel
            bullet.rect.y -= bullet.y_vel
            WINDOW.blit(LASER, (bullet.rect.x, bullet.rect.y))
            self._handle_bullets(bullet, enemies)

    def _move_arrow(self):
        self._buy_station_arrow.y += self._arrow_movement
        if self._buy_station_arrow.y == 150:
            self._arrow_movement = 1
        elif self._buy_station_arrow.y == 200:
            self._arrow_movement = -1

    def draw_ammo(self) -> None:
        """ Handles the drawing of the amount of current ammo and total ammo on
        the bottom right of the screen. Also draws messages to reload or buy
        ammo if this is required.
        """
        ammo_text = FONT.render('Ammo: ' + str(self.curr_ammo) + ' / ' +
                                str(GUN_AMMO), False, WHITE)
        WINDOW.blit(ammo_text, (WIDTH - 225, HEIGHT - 130))
        total_text = FONT_SMALL.render('Total Ammo: ' + str(self.ammo), False,
                                       WHITE)
        WINDOW.blit(total_text, (WIDTH - 195, HEIGHT - 90))

        if self.need_reload:
            reload_text = FONT_SMALL.render('PRESS "R" TO RELOAD!', False, RED)
            reload_text_w = FONT_SMALL.render('PRESS "R" TO RELOAD!', False,
                                              WHITE)
            WINDOW.blit(reload_text_w, (WIDTH - 236, HEIGHT - 154))
            WINDOW.blit(reload_text, (WIDTH - 235, HEIGHT - 155))
        elif self.out_of_ammo:
            out_text = FONT_SMALL.render('OUT OF AMMO! BUY MORE!', False, RED)
            out_text_w = FONT_SMALL.render('OUT OF AMMO! BUY MORE!', False,
                                           WHITE)
            WINDOW.blit(out_text_w, (WIDTH - 286, HEIGHT - 154))
            WINDOW.blit(out_text, (WIDTH - 285, HEIGHT - 155))
            if not self.at_buy_platform:
                self._move_arrow()
                WINDOW.blit(RED_ARROW, self._buy_station_arrow.topleft)

    def reload(self) -> None:
        """ Reload this player's ammo to the appropriate amount, and make the
        boolean self.need_reload False.
        """
        if self.ammo <= 32:
            self.curr_ammo += self.ammo
        else:
            self.curr_ammo = 32

        self.need_reload = False
        RELOAD_SOUND.play()

    def draw_hearts(self) -> None:
        """ Display the hearts representing the player's health on the bottom
        right of the screen.
        """
        x, y = WIDTH - 48, HEIGHT - 40
        for i in range(1, self.health + 1):
            WINDOW.blit(HEART, (x, y))
            x -= 48

    def check_damage(self, enemy) -> None:
        """ Check if this <enemy> has collided with the player, and if they
        did, lower the player's health.
        """
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

        if self.health <= 0:
            self.dead = True
            pygame.mixer.music.stop()
            CHAR_DEATH.play()

    def update_health(self) -> None:
        """ Use a clock to determine when the player's health should be
        increased and only increase health if self.health < 5.
        """
        now = pygame.time.get_ticks()
        if now - self._last_update_health > 3000:
            self._last_update_health = now
            if self.health < 5:
                self.health += 1

    def add_money(self) -> None:
        """ Add money to this player for killing an enemy.
        """
        self.money += 10

    def display_money(self) -> None:
        """ Display text indicating the amount of money this player has on the
        bottom left of the screen, as well as indicators of money gained at the
        location enemies were killed at.
        """
        money_text = FONT.render('Money: $' + str(self.money), False, WHITE)
        WINDOW.blit(money_text, (20, HEIGHT - 50))

        for i in range(len(self._money_gain)):
            kill_text = FONT_SMALL.render('+ $10', False, YELLOW)
            WINDOW.blit(kill_text, (self._money_gain[i][0],
                                    self._money_gain[i][1]))
            self._money_gain[i] = (self._money_gain[i][0],
                                   self._money_gain[i][1],
                                   self._money_gain[i][2] - 1)

        for kill in self._money_gain:
            if kill[2] == 0:
                self._money_gain.remove(kill)

    def check_buy(self) -> None:
        """ Determine if the player is standing on the buy platform, and display
        an appropriate message to either buy ammo or inform the player that they
        do not have enough money for ammo.
        """
        self.at_buy_platform = False
        self.has_funds = False

        if self.rect.colliderect(PLATFORM_RECT):
            if self.money >= AMMO_COST:
                buy_text = FONT_SMALL.render('PRESS "B" TO BUY ' + str(GUN_AMMO)
                                             + ' AMMO ($' + str(AMMO_COST) +
                                             ')', False, YELLOW)
                x, y = PLATFORM_RECT.bottomleft
                x -= 70
                WINDOW.blit(buy_text, (x, y))
                self.at_buy_platform = True
                self.has_funds = True
            else:
                no_fund_text = FONT_SMALL.render('NOT ENOUGH MONEY FOR AMMO,' +
                                                 ' NEED $' + str(AMMO_COST),
                                                 False, YELLOW)
                x, y = PLATFORM_RECT.bottomleft
                x -= 130
                WINDOW.blit(no_fund_text, (x, y))
                self.at_buy_platform = True

    def buy_ammo(self) -> None:
        """ Handles the purchasing of ammo by adding to this player's amount of
        ammo, reducing their money, and making the boolean indicator for no
        ammo false.
        """
        self.ammo += GUN_AMMO
        self.curr_ammo = GUN_AMMO
        self.money -= AMMO_COST
        self.out_of_ammo = False
        BUY_SOUND.play()

    def death_animation(self) -> None:
        """ Plays this player's death animation by swapping through the pygame
        surfaces representing the player's blood splat and setting those as
        the current death sprite to blit onto the screen
        """
        now = pygame.time.get_ticks()

        if now - self._last_update_dead > 50:
            self._last_update_dead = now
            self._curr_death_sprite = (self._curr_death_sprite + 1) % len(
                self._death_sprites)

        x, y = self.rect.topleft
        x -= 75
        y -= 75
        WINDOW.blit(self._death_sprites[self._curr_death_sprite], (x, y))

        if self._curr_death_sprite == 21:
            self.full_dead = True
            pygame.mixer.stop()
            GAME_OVER_MUSIC.play(-1)


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
         enemy list in the Wave class
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
    #     A list of sprites representing the blood when this enemy is hit
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
        """ Initialize the attributes for this enemy.
        """
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
        """ Spawn in this enemy at a random location outside the viewable screen
        """
        x, y = 0, 0
        while (0 <= x <= WIDTH) and (0 <= y <= HEIGHT):
            x = random.randint(-500, WIDTH + 500)
            y = random.randint(-500, HEIGHT + 500)
        self.rect.center = (x, y)

    def damage(self) -> None:
        """ Register the fact that this enemy was damaged by reducing
        <self.health>, also determine if the enemy has died.
        """
        self.health -= 1
        ENEMY_HIT.play()
        if self.health == 0:
            self.dead = True
            ENEMY_DEATH.play()
        else:
            self.play_hit_animation = True

    def draw_health(self) -> None:
        """ Draw a rectangle underneath the enemy which displays the amount of
        health it has remaining. This method moves this bar to keep it under the
        enemy, and updates it by changing how it looks to show what level of
        health the enemy is at.
        """
        x1, y1 = self.rect.bottomleft
        x1 += 16
        y1 += 6
        x2, y2 = self.rect.bottomright
        x2 -= 16
        y2 += 6

        if self.health == 2:
            split = int((x2 - x1) * 0.66)
            split += x1
            pygame.draw.line(WINDOW, GREEN, (x1, y1), (split, y2), 4)
            pygame.draw.line(WINDOW, RED, (split, y1), (x2, y2), 4)
        elif self.health == 1:
            split = int((x2 - x1) * 0.33)
            split += x1
            pygame.draw.line(WINDOW, GREEN, (x1, y1), (split, y2), 4)
            pygame.draw.line(WINDOW, RED, (split, y1), (x2, y2), 4)
        else:
            pygame.draw.line(WINDOW, GREEN, (x1, y1), (x2, y2), 4)

    def animate(self, x: int) -> None:
        """ Animate the enemy by cycling through its animation as it moves.
        Also flip the pygame surface of this enemy to face them towards the
        player.
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

    def hit_animation(self) -> None:
        """ When this enemy is hit by a bullet, this method plays an animation
        of a blood splatter at the location where the enemy was hit.
        """
        now = pygame.time.get_ticks()

        if now - self._last_update_hit > 25:
            self._last_update_hit = now
            self._curr_hit_sprite = (self._curr_hit_sprite + 1) % len(
                self._hit_sprites)

        x, y = self.rect.topleft
        x -= 80
        y -= 80
        WINDOW.blit(self._hit_sprites[self._curr_hit_sprite], (x, y))

        if self._curr_hit_sprite == 27:
            self.play_hit_animation = False

    def death_animation(self) -> None:
        """ Once this enemy is killed, this method plays an animation of a blood
         splatter where the enemy died. It then sets <self.remove> to True to
         indicate to the Wave class to remove this enemy from its self.enemies
         list.
         """
        now = pygame.time.get_ticks()

        if now - self._last_update_dead > 25:
            self._last_update_dead = now
            self._curr_death_sprite = (self._curr_death_sprite + 1) % len(
                self._death_sprites)

        x, y = self.rect.topleft
        x -= 60
        y -= 60
        WINDOW.blit(self._death_sprites[self._curr_death_sprite], (x, y))

        if self._curr_death_sprite == 29:
            self.remove = True


class Worm(Enemy):
    """The Worm Enemy class for this game.

    This class handles the drawing of, spawning in, movement, health, damage,
    and animations of this enemy.

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
        """ Initialize this worm enemy by calling on its super class and
        instantiating further attributes including its sprites
        <self.enemy_sprites>, current sprite <self.curr_sprite>, and its pygame
        rectangle <self.rect>.
        """
        Enemy.__init__(self)
        self._enemy_sprites = WORM_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self.spawn()

    def move(self, x: int, y: int) -> None:
        """ Move this worm enemy towards the player's x and y coordinates by
        adding or subtracting the enemy's speed from its rectangle's x and y
        values.
        """
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

    This class handles the drawing of, spawning in, movement, health, damage,
    and animations of this enemy.

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
        """ Initialize this bat enemy by calling on its super class and
        instantiating further attributes including its sprites
        <self.enemy_sprites>, current sprite <self.curr_sprite>, its pygame
        rectangle <self.rect>, as well as attributes to track when it's movement
        was last updated <self._last_update_movement>, the player's x and y
        values <self._target_x> and <self._target_y>, and a variable to track
        when movement should be updated <self._movement_update>.
        """
        Enemy.__init__(self)
        self._enemy_sprites = BAT_SPRITES
        self.curr_sprite = self._enemy_sprites[0]
        self.rect = self.curr_sprite.get_rect()
        self._last_update_movement = 0
        self._target_x, self._target_y = WIDTH // 2, HEIGHT // 2
        self._movement_update = random.randint(3000, 5000)
        self.spawn()

    def move(self, x: int, y: int) -> None:
        """ This method handles the movement of this bat enemy, which only
        updates the coordinate that this enemy is moving towards after a
        randomly selected amount of time.
        """
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

    This class handles the drawing of, spawning in, movement, health, damage,
    and animations of this enemy.

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
         A boolean which indicates whether this enemy has begun their
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
    # _timer_sound:
    #    The sound that plays when this enemy is priming to explode

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
    _timer_sound: pygame.mixer.Sound

    def __init__(self) -> None:
        """ Initialize this Mushroom enemy by calling on the super class as well
        as instantiating further variables such as the enemy's sprites, their
        pygame rectangle, the current sprite, booleans to determine if this
        enemy damaged a player, exploded, is close to the player, and changed
        their sprite. Other attributes are instantiated to keep track of when
        this enemy's explosion effect was last updated.
        """
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
        self._timer_sound = TIMER_SOUND
        self.spawn()

    def move(self, x: int, y: int) -> None:
        """ Move this enemy towards the player's current x and y coordinates
        only if this enemy is not within a certain range of the player. If they
        are, call on helper methods to change this enemy's sprite to their
        explosion countdown sprites and start the explosion countdown.
        """
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

    def _close_to_player(self, x: int, y: int) -> None:
        """ Return whether this mushroom enemy is close enough
        to the player to explode, within 100 pixels in any direction.
        """
        dx = abs(self.rect.x - x)
        dy = abs(self.rect.y - y)
        dist = math.sqrt((dx**2) + (dy**2))
        if dist <= 100.0:
            self._close = True

    def _change_sprite(self) -> None:
        """ Change the enemies sprites in <self._enemy_sprites> to a different
        list of sprites only once, their explosion countdown sprites. Also
        update the <self._last_update_explode> timer to the current frame.
        """
        if not self._sprite_changed:
            self._enemy_sprites = MUSHROOM_EXPLODE_SPRITES
            self._last_update_explode = pygame.time.get_ticks()
            self._timer_sound.play()
            self._sprite_changed = True

    def _explode(self) -> None:
        """ A helper method that tracks the remaining frames left until
        this enemy explodes.
        """
        now = pygame.time.get_ticks()

        if now - self._last_update_explode > 3000 and not self.exploded and \
                not self.dead:
            self.player_damage = 3
            x, y = self.rect.center
            self._death_sprites = EXPLOSION_SPRITES
            self.rect = self._death_sprites[0].get_rect()
            self.rect.center = (x, y)
            EXPLOSION_SOUND.play()
            self.dead = True
            self.exploded = True

    def death_animation(self) -> None:
        """ Swap through sprites which represent this enemy's death, an
        explosion, and set <self.remove> to True once their death animation
        has finished in order to indicate to the Wave class to remove this
        enemy from its self.enemies list.
        """
        if self.exploded:
            now = pygame.time.get_ticks()
            WINDOW.blit(self._death_sprites[self._curr_death_sprite],
                        self.rect.topleft)
            if now - self._last_update_dead > 60:
                self._last_update_dead = now
                self._curr_death_sprite = (self._curr_death_sprite + 1) % len(
                    self._death_sprites)
            if self._curr_death_sprite == 11:
                self.remove = True
        else:
            self._timer_sound.stop()
            Enemy.death_animation(self)


class Wave:
    """ The Wave class for this game.

    This class is responsible for requesting the start of a wave, starting the
    wave and determining the number of enemies to spawn, and tracking how many
    enemies are left. It handles the enemies in the current wave by updating
    their animations, movement, damage, and whether they are alive or dead. This
    class also handles the animation of the on-screen messages to the player
    about the wave.

    === Public Attributes ===
    wave:
         An integer which tracks which wave the game is currently on
    enemies:
         A list of enemies of the Enemy class that are spawned in the
         current wave
    begin:
         A boolean which indicates whether the player has started the first
         wave and therefore started up the wave progression
    start_wave_anim:
         A boolean which determines if the text animation should be played to
         indicate the starting of a wave
    wave_complete:
         A boolean which indicates if a wave is complete, which happens when
         there are no more enemies remaining
    wave_commenced:
         A boolean which tracks if a wave has begun and enemies have all been
         spawned in
    curr_enemies:
         An integer which represents the number enemies remaining
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
    wave_commenced: bool
    curr_enemies: int
    _last_update_start: int
    _last_update_complete: int

    def __init__(self) -> None:
        """ Initialize the attributes for the Wave class"""
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
        """ Set <self.begin> to true to indicate that waves have begun and
        call start_wave() to set up the first wave.
        """
        self.begin = True
        self.start_wave()

    def request_wave_start(self) -> None:
        """ Display a message to the player to start the nth wave if they are
        in between waves or have just loaded up the game.
        """
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
        wave_start_text = FONT_BOLD.render('PRESS "SPACEBAR" TO START THE ' +
                                           wave + ' WAVE', False, YELLOW)
        WINDOW.blit(wave_start_text, (10, 620))

    def start_wave(self) -> None:
        """ Start the wave by updating the wave number and calling on
        _init_enemies() to choose and spawn in the enemies.
        """
        self.wave += 1
        self.start_wave_anim = True
        self._init_enemies()
        self.wave_commenced = True
        self._last_update_start = pygame.time.get_ticks()
        WAVE_START.play()

    def wave_start_animation(self) -> None:
        """ Display a message to the player indicating that the nth wave
        has started and remove this message after some time.
        """
        start_text_back = FONT_BOLD_LARGE.render('STARTING WAVE ' + str(
            self.wave), False, BLACK)
        WINDOW.blit(start_text_back, (410, 605))
        start_text = FONT_BOLD_LARGE.render('STARTING WAVE ' + str(self.wave),
                                            False, WHITE)
        WINDOW.blit(start_text, (415, 600))

        now = pygame.time.get_ticks()
        if now - self._last_update_start > 2500:
            self.start_wave_anim = False

    def _init_enemies(self) -> None:
        """ Initialize the enemies by determining the amount to spawn in this
        wave, then randomly select from the 3 types of enemies which to add
        to the <self.enemies> list in order to spawn them in this round.
        """
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
        """ Handle the enemies by removing them from <self.enemies> if they
        died, otherwise update their animations, movement, and check if they
        damaged the player. This method also calls _wave_status().
        """
        for enemy in self.enemies:
            if enemy.remove:
                self.enemies.remove(enemy)
            else:
                enemy.animate(char.rect.x)
                if not char.dead:
                    enemy.move(char.rect.centerx, char.rect.centery)
                    char.check_damage(enemy)

        self.curr_enemies = len(self.enemies)

        if not self.wave_complete:
            self._wave_status()

    def _wave_status(self) -> None:
        """ This method determines if there are no remaining enemies and
        declared if the wave is complete by changing <self.wave_complete> to
        True and <self.wave_commenced> to False.
        """
        if len(self.enemies) == 0:
            self.wave_complete = True
            self.wave_commenced = False
            self._last_update_complete = pygame.time.get_ticks()
            WAVE_FINISH.play()

    def enemy_animations(self) -> None:
        """ This method draws each enemy's sprite onto the screen along with
        their hit animation if they were hurt. If the enemy dies, this method
        draws their death animation.
        """
        for enemy in self.enemies:
            if not enemy.dead:
                WINDOW.blit(enemy.curr_sprite, (enemy.rect.x, enemy.rect.y))
                enemy.draw_health()
                if enemy.play_hit_animation:
                    enemy.hit_animation()
            else:
                enemy.death_animation()

    def wave_complete_anim(self) -> None:
        """ This method displays text on the screen indicating that a wave was
        completed for a short amount of time.
        """
        complete_text_back = FONT_BOLD_LARGE.render('WAVE COMPLETE!', False,
                                                    BLACK)
        WINDOW.blit(complete_text_back, (410, 605))
        complete_text = FONT_BOLD_LARGE.render('WAVE COMPLETE!', False, WHITE)
        WINDOW.blit(complete_text, (415, 600))

        now = pygame.time.get_ticks()
        if now - self._last_update_complete > 2500:
            self.wave_complete = False
            self.begin = False

    def show_remaining(self) -> None:
        """ This method displays text on the screen that shows the amount of
        enemies remaining in the current wave.
        """
        remaining_text = FONT.render('Enemies Remaining: ' + str(
            self.curr_enemies), False, WHITE)
        WINDOW.blit(remaining_text, (375, 670))


class GameOver:
    """ The game over screen for this game.

    This class handles the game over screen when the character dies.
    It handles the drawing of the menu and handling of the buttons
    and their function when they are pressed.

    === Public Attributes ===
    retry_btn:
         The pygame rectangle representing the retry button
    menu_btn:
         The pygame rectangle representing the menu button
    click:
         A boolean which is True when the screen is clicked and False
         otherwise
    retry_active:
         A boolean which indicates if the cursor is hovering over the
         retry button (True) or not (False)
    menu_active:
         A boolean which indicates if the cursor is hovering over the
         menu button (True) or not (False)
    play_highlight_sound:
         A boolean which tracks if the highlight sound has been played
         once
    updated_score:
         A boolean which tracks if the high score has been updated yet
    high_score:
         An integer representing the highest score achieved in the game
         out of all tries, including in previous runs of this program.
         This initially starts as 0 but is later updated to the highest
         score achieved according to scores.txt in the Assets/misc
         folder
    retry:
         A boolean which indicates if the player has chosen to retry the
         game (True) or hasn't chosen this option yet or at all (False)
    return_to_menu:
         A boolean which indicates if the player has chosen to return
         to the main menu (True) or hasn't made this decision yet or
         at all (False)
    """
    retry_btn: pygame.rect
    menu_btn: pygame.rect
    click: bool
    retry_active: bool
    menu_active: bool
    play_highlight_sound: bool
    retry: bool
    return_to_menu: bool
    updated_score: bool
    high_score: int

    def __init__(self) -> None:
        """ Initialize the pygame rectangles for the buttons as well as
        the boolean attributes for this menu.
        """
        self.retry_btn = REPLAY_BTN.get_rect()
        self.retry_btn.center = (WIDTH // 2 - 150, HEIGHT // 2 + 50)
        self.menu_btn = MAIN_MENU_BTN.get_rect()
        self.menu_btn.center = (WIDTH // 2 + 150, HEIGHT // 2 + 50)
        self.click = False
        self.retry_active = False
        self.menu_active = False
        self.play_highlight_sound = False
        self.retry = False
        self.return_to_menu = False
        self.updated_score = False
        self.high_score = 0

    def draw_menu(self) -> None:
        """ Draw the game over text as well as the buttons on the screen
        and change them to a different colour if they're being hovered
        over.
        """
        WINDOW.blit(GAME_OVER_BG, (0, 0))
        WINDOW.blit(GAME_OVER_TEXT, (WIDTH // 2 - 347, 100))
        if self.retry_active:
            WINDOW.blit(REPLAY_BTN_ACTIVE, self.retry_btn.topleft)
            retry_text = FONT.render('RETRY', False, YELLOW)
            x, y = self.retry_btn.bottomleft
            x += 55
            y += 5
            WINDOW.blit(retry_text, (x, y))
        else:
            WINDOW.blit(REPLAY_BTN, self.retry_btn.topleft)
        if self.menu_active:
            WINDOW.blit(MAIN_MENU_BTN_A, self.menu_btn.topleft)
            retry_text = FONT.render('MAIN MENU', False, YELLOW)
            x, y = self.menu_btn.bottomleft
            x += 15
            y += 5
            WINDOW.blit(retry_text, (x, y))
        else:
            WINDOW.blit(MAIN_MENU_BTN, self.menu_btn.topleft)
        high_score_text = FONT.render('CURRENT HIGH SCORE: ' + str(
            self.high_score), False, YELLOW)
        WINDOW.blit(high_score_text, (450, 600))

    def handle_buttons(self, mx: float, my: float) -> None:
        """ Handles button presses by checking where the screen was clicked
        according to <mx> and <my> mouse position coordinates,
        and if a button was clicked, handles the action this button performs
        such as retrying the game or returning to the main menu.
        """
        if self.retry_btn.collidepoint(mx, my):
            self.retry_active = True
            if not self.play_highlight_sound:
                HIGHLIGHT.play()
            self.play_highlight_sound = True
            if self.click:
                GAME_OVER_MUSIC.stop()
                self.retry = True
        elif self.menu_btn.collidepoint(mx, my):
            self.menu_active = True
            if not self.play_highlight_sound:
                HIGHLIGHT.play()
            self.play_highlight_sound = True
            if self.click:
                self.return_to_menu = True
        else:
            self.retry_active = False
            self.menu_active = False
            self.play_highlight_sound = False


def _draw_window_helper(wave: Wave, char: Player) -> None:
    """ A helper function for the draw_window() function which
    animates the enemies in the <wave> as well as the character
    <char> ammo, money, and hearts.
    """
    wave.enemy_animations()
    WINDOW.blit(BAR, (0, HEIGHT - 50))
    WINDOW.blit(HEALTH, (WIDTH - 355, HEIGHT - 35))
    char.check_buy()
    char.draw_hearts()
    char.display_money()
    char.draw_ammo()


def control_instructions() -> None:
    """ A function which displays the controls of the game to the player
    """
    control_text1 = FONT.render('Use', False, WHITE)
    control_text2 = FONT.render('to move', False, WHITE)
    control_text3 = FONT.render('Point with the mouse', False, WHITE)
    control_text4 = FONT.render('and click to shoot', False, WHITE)
    WINDOW.blit(control_text1, (40, 70))
    WINDOW.blit(WASD, (100, 20))
    WINDOW.blit(control_text2, (290, 70))
    WINDOW.blit(control_text3, (40, 130))
    WINDOW.blit(CURSOR, (310, 180))
    WINDOW.blit(control_text4, (40, 170))


def draw_window(wave: Wave, char: Player, rotation: float, game_over_menu:
                GameOver) -> None:
    """ This function is responsible for drawing every element of this game
    onto the screen.
    """
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(PLATFORM, PLATFORM_RECT.topleft)
    WINDOW.blit(CHEST, (WIDTH // 2 - 33, 60))
    curr_char = char.get_rotated(rotation)
    char.draw_bullets(wave.enemies)
    if not char.dead:
        WINDOW.blit(curr_char, char.rect.topleft)
        _draw_window_helper(wave, char)
    elif not char.full_dead:
        char.death_animation()
        _draw_window_helper(wave, char)
    else:
        game_over_menu.draw_menu()

    if wave.wave == 0:
        control_instructions()

    if not wave.begin:
        wave.request_wave_start()
    elif wave.start_wave_anim:
        wave.wave_start_animation()
    elif wave.wave_commenced and not char.full_dead:
        wave.show_remaining()
    elif wave.wave_complete:
        wave.wave_complete_anim()
    pygame.display.update()


def update_highscore(game_over_menu: GameOver, wave: Wave) -> None:
    """ This function adds the current wave achieved before dying to a text file
    containing all the highest waves achieved in each game this player has
    played. These scores are then read through and the highest one is set as the
    highest score to be displayed in the game over menu.
    """
    if not game_over_menu.updated_score:
        with open('Assets/misc/scores.txt', 'a') as scores:
            scores.write(str(wave.wave) + '\n')
        with open('Assets/misc/scores.txt', 'r') as scores:
            all_scores = scores.readlines()
            highest = int(all_scores[0])
            for curr_score in all_scores:
                if int(curr_score) > highest:
                    highest = int(curr_score)
            game_over_menu.high_score = highest
        game_over_menu.updated_score = True


def _main_event_helper(event, char: Player, wave: Wave,
                       game_over_menu: GameOver, mx: int, my: int) -> None:
    """ A helper function for the main() function which handles checking
    which event is currently occurring and performing the appropriate
    action.
    """
    if event.type == pygame.QUIT:
        pygame.quit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 and not char.dead:
            char.shoot_bullet(mx, my)
        elif event.button == 1:
            game_over_menu.click = True
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and not wave.begin:
            wave.begin_waves()
        if event.key == pygame.K_r and char.need_reload and not char.dead:
            char.reload()
        if event.key == pygame.K_b and char.at_buy_platform and \
                char.has_funds and not char.dead:
            char.buy_ammo()


def main() -> bool:
    """ This function contains the main game loop for this game and handles
    creation of the player and the wave class. It also handles inputs to the
    game, as well as the movement of the character, their health, and updating
    the enemies in the game if they are spawned in.
    """
    run = True
    clock = pygame.time.Clock()
    char = Player()
    wave = Wave()
    pygame.mixer.music.load('Assets/sounds/background_music.wav')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1)
    game_over_menu = GameOver()
    while run:
        clock.tick(FPS)
        mx, my = pygame.mouse.get_pos()
        dif_x, dif_y = mx - char.rect.centerx, my - char.rect.centery
        rotation = (180 / math.pi) * -math.atan2(dif_y, dif_x) - 90
        for event in pygame.event.get():
            _main_event_helper(event, char, wave, game_over_menu, mx, my)
        key_pressed = pygame.key.get_pressed()
        if char.full_dead:
            update_highscore(game_over_menu, wave)
            game_over_menu.handle_buttons(float(mx), float(my))
            if game_over_menu.retry:
                WAVE_FINISH.play()
                return True
            elif game_over_menu.return_to_menu:
                pygame.mixer.stop()
                return False
        elif not char.dead:
            char.move(key_pressed)
            char.update_health()
        game_over_menu.click = False

        if wave.wave_commenced:
            wave.handle_enemies(char)

        draw_window(wave, char, rotation, game_over_menu)
    return False


class MainMenu:
    """ The Main Menu class for this game.

    This class handles the creation of the menu, the movement of the
    background images, the drawing of the menu elements, and handling
    of button presses and the functions they should perform.

    === Public Attributes ===
    self.bg_rect:
         The pygame rectangle representing the menu background, meant
         to move upwards
    self.bg_rect2:
         A pygame rectangle representing the second menu background,
         meant to move up following <self.bg_rect>
    self.start_btn:
         The pygame rectangle representing the area of the start button
    self.exit_btn:
         The pygame rectangle representing the area of the exit button
    self.start_active:
         A boolean which indicates if the cursor is on the start button
         and if it should be highlighted
    self.exit_active:
         A boolean which indicates if the cursor is on the exit button
         and if it should be highlighted
    self.playing:
         A boolean which indicates if the button select sound is already
         playing
    self.click:
         A boolean which represents if the screen has been clicked
    """
    bg_rect: pygame.rect
    bg_rect2: pygame.rect
    start_btn: pygame.rect
    exit_btn: pygame.rect
    start_active: bool
    exit_active: bool
    playing: bool
    click: bool

    def __init__(self) -> None:
        """ Initialize the pygame rectangles for the background and buttons,
        as well as the boolean attributes for highlighting the buttons,
        playing the highlight sound, and clicking the screen.
        """
        self.bg_rect = MENU_BG.get_rect()
        self.bg_rect.topleft = (0, 0)
        self.bg_rect2 = MENU_BG.get_rect()
        self.bg_rect2.topleft = (0, 2277)
        self.start_btn = START_BTN.get_rect()
        self.start_btn.center = (WIDTH // 2, HEIGHT // 2 + 50)
        self.exit_btn = EXIT_BTN.get_rect()
        self.exit_btn.center = (WIDTH // 2, HEIGHT // 2 + 200)
        self.start_active = False
        self.exit_active = False
        self.playing = False
        self.click = False

    def move_bg(self) -> None:
        """ Moves the pygame rectangles representing the two
        background images upwards, following each other. When one
        background image leaves the screen, it is moved down below
        the other one to continue moving upwards onto the screen.
        """
        self.bg_rect.y -= 1
        self.bg_rect2.y -= 1
        if self.bg_rect.bottomleft == (0, -1):
            self.bg_rect.topleft = (0, 2277)
        elif self.bg_rect2.bottomleft == (0, -1):
            self.bg_rect2.topleft = (0, 2277)

    def draw_menu(self) -> None:
        """ Draw the elements of the menu such as the background images,
        The start and exit buttons, and the title. Also handles deciding
        to show the highlighted forms of the start and exit buttons if
        the cursor is on top of them.
        """
        WINDOW.blit(MENU_BG, self.bg_rect.topleft)
        WINDOW.blit(MENU_BG, self.bg_rect2.topleft)
        if self.start_active:
            WINDOW.blit(START_BTN_ACTIVE, self.start_btn.topleft)
        else:
            WINDOW.blit(START_BTN, self.start_btn.topleft)
        if self.exit_active:
            WINDOW.blit(EXIT_BTN_ACTIVE, self.exit_btn.topleft)
        else:
            WINDOW.blit(EXIT_BTN, self.exit_btn.topleft)
        WINDOW.blit(TITLE, (WIDTH // 2 - 282, 50))
        pygame.display.update()

    def _handle_start_btn(self) -> None:
        """ Handles highlighting the start button if the cursor is hovering
        over it, and starts the main game when this button is pressed.
        Continues to start the game as long as the player wants to keep
        retrying.
        """
        self.start_active = True
        if not self.playing:
            HIGHLIGHT.play()
        self.playing = True
        if self.click:
            MENU_MUSIC.stop()
            GAME_START.play()
            retry = True
            while retry:
                retry = main()
            MENU_MUSIC.play(-1)

    def _handle_exit_btn(self) -> bool:
        """ Handles playing the highlight sound when the mouse is above this
        button, as well as exiting the game if it is pressed by returning
        False.
        """
        self.exit_active = True
        if not self.playing:
            HIGHLIGHT.play()
        self.playing = True
        if self.click:
            return False
        return True

    def handle_buttons(self, mx: float, my: float) -> bool:
        """ Handles button presses by checking if the screen was clicked
        when the mouse was over a button, and then performing the
        appropriate action for that button.
        """
        if self.start_btn.collidepoint(mx, my):
            self._handle_start_btn()
        elif self.exit_btn.collidepoint(mx, my):
            return self._handle_exit_btn()
        else:
            self.start_active = False
            self.exit_active = False
            self.playing = False
        self.click = False
        return True


def main_menu() -> None:
    """ The main menu for this game. This function contains the main
    loop for the menu and calls on methods in the MainMenu class to
    control the main menu and allow it to perform its functions.
    """
    run = True
    clock = pygame.time.Clock()
    menu = MainMenu()
    MENU_MUSIC.play(-1)

    while run:
        clock.tick(FPS)
        menu.move_bg()
        menu.draw_menu()
        mx, my = pygame.mouse.get_pos()
        mx = float(mx)
        my = float(my)
        run = menu.handle_buttons(mx, my)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu.click = True
    pygame.quit()


if __name__ == "__main__":
    main_menu()
