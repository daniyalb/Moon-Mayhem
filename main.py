import pygame
import math
from enemy import Worm, Bat

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
pygame.display.set_caption("Moon Mayhem 2")
pygame.display.set_icon(ICON)
FPS = 60
FONT = pygame.font.Font('Assets/misc/font.ttf', 34)
FONT_SMALL = pygame.font.Font('Assets/misc/font.ttf', 24)


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
        WINDOW.blit(ammo_text, (WIDTH - 175, HEIGHT - 100))
        total_text = FONT_SMALL.render('Total Ammo: ' + str(self.ammo), False, WHITE)
        WINDOW.blit(total_text, (WIDTH - 165, HEIGHT - 72))

        if self.need_reload:
            reload_text = FONT_SMALL.render('PRESS "R" TO RELOAD!', False, RED)
            WINDOW.blit(reload_text, (WIDTH - 205, HEIGHT - 115))
        elif self.out_of_ammo:
            reload_text = FONT_SMALL.render('OUT OF AMMO! BUY MORE!', False, RED)
            WINDOW.blit(reload_text, (WIDTH - 235, HEIGHT - 115))

    def reload(self) -> None:
        if self.ammo <= 32:
            self.curr_ammo += self.ammo
            self.ammo = 0
        else:
            self.ammo -= 32
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
        if now - self._last_update_damage > 1000:
            if self.rect.colliderect(enemy) and not enemy.dead:
                self.health -= 1
                CHAR_HIT.play()
            self._last_update_damage = now

    def update_health(self) -> None:
        """ Use a clock to determine when the player's health should be increased
        and only increase health if self.health < 5
        """
        now = pygame.time.get_ticks()
        if now - self._last_update_health > 2000:
            self._last_update_health = now
            if self.health < 5:
                self.health += 1

    def add_money(self) -> None:
        """ Add money to this player for killing an enemy
        """
        self.money += 10

    def display_money(self) -> None:
        money_text = FONT.render('Money: $' + str(self.money), False, WHITE)
        WINDOW.blit(money_text, (20, HEIGHT - 40))

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
                x -= 50
                WINDOW.blit(buy_text, (x, y))
                self.at_buy_platform = True
                self.has_funds = True
            else:
                no_fund_text = FONT_SMALL.render('NOT ENOUGH MONEY FOR AMMO, NEED $' + str(AMMO_COST), False, YELLOW)
                x, y = PLATFORM_RECT.bottomleft
                x -= 90
                WINDOW.blit(no_fund_text, (x, y))
                self.at_buy_platform = True

    def buy_ammo(self) -> None:
        self.ammo += GUN_AMMO + self.curr_ammo
        self.curr_ammo = GUN_AMMO
        self.money -= AMMO_COST
        self.out_of_ammo = False
        BUY_SOUND.play()


def draw_window(char: Player, rotation: float, enemies: list):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(PLATFORM, PLATFORM_RECT.topleft)
    WINDOW.blit(CHEST, (WIDTH // 2 - 33, 60))
    curr_char = char.get_rotated(rotation)
    char.draw_bullets(enemies)
    WINDOW.blit(curr_char, char.rect.topleft)
    for enemy in enemies:
        if not enemy.dead:
            WINDOW.blit(enemy.curr_sprite, (enemy.rect.x, enemy.rect.y))
            enemy.draw_health(WINDOW)
            if enemy.play_hit_animation:
                enemy.hit_animation(WINDOW)
        else:
            enemy.death_animation(WINDOW)
    WINDOW.blit(BAR, (0, HEIGHT - 50))
    WINDOW.blit(HEALTH, (WIDTH - 355, HEIGHT - 35))
    char.check_buy()
    char.draw_hearts()
    char.display_money()
    char.draw_ammo()
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    char = Player()
    enemies = [Worm(), Worm(), Bat(), Bat()]
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
                if event.key == pygame.K_r and char.need_reload:
                    char.reload()
                if event.key == pygame.K_b and char.at_buy_platform and char.has_funds:
                    char.buy_ammo()

        key_pressed = pygame.key.get_pressed()
        char.move(key_pressed)
        char.update_health()

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
