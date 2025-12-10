from subprocess import check_call
import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_INVINCIBILITY_TIME,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    SHOT_RADIUS,
)
from constants import LINE_WIDTH
from constants import PLAYER_TURN_SPEED
from constants import PLAYER_SPEED
from constants import PLAYER_SHOT_SPEED
from constants import PLAYER_LIVES
from constants import PLAYER_DEAD_TIME


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.invincibility_cooldown = 0
        self.draw_cooldown = 0
        self.laser_sound = pygame.mixer.Sound(
            "./Sounds/mixkit-short-laser-gun-shot-1670.wav"
        )
        self.engine_on = pygame.mixer.Sound(
            "./Sounds/mixkit-fast-rocket-whoosh-1714.wav"
        )
        self.lives = PLAYER_LIVES
        # self.is_invincible = False
        self.is_drawn = True

    def draw(self, screen):
        if self.draw_cooldown > 0:
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)
        if self.invincibility_cooldown > 0:
            pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    # If the player is invincible, return false, there's no need to check
    # for an actual collision. Otherwise, check for a collision, and if true
    # set the invincibility_cooldown time, and return True. If at this point
    # there has been no collision, we can just return False as normal
    def collides_with(self, other):
        if self.draw_cooldown > 0 or self.invincibility_cooldown > 0:
            return False
        if super().collides_with(other):
            self.invincibility_cooldown = PLAYER_INVINCIBILITY_TIME + PLAYER_DEAD_TIME
            self.draw_cooldown = PLAYER_DEAD_TIME
            return True
        return False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt
        self.invincibility_cooldown -= dt
        self.draw_cooldown -= dt
        if self.draw_cooldown > 0:
            return
        # print(f"cooldown: {self.invincibility_cooldown}")
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.engine_on.play()

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        speed = pygame.Vector2(0, 1)
        speed = speed.rotate(self.rotation)
        speed *= PLAYER_SHOT_SPEED
        shot.velocity = speed
        self.laser_sound.play()
