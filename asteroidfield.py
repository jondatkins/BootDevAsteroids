import pygame
import random
from asteroid import Asteroid
import asteroid
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.asteroids = []

    # sets up a rectangle in side the pygame window surface, so I can see
    # where the asteroids are spawing and dynamically resize the game area
    def set_game_rect(self, game_rect):
        self.game_rect = game_rect
        self.edges = [
            [
                pygame.Vector2(1, 0),  # from left edge moving right
                lambda y: pygame.Vector2(
                    self.game_rect.left - ASTEROID_MAX_RADIUS,
                    self.game_rect.top + y * self.game_rect.height,
                ),
            ],
            [
                pygame.Vector2(-1, 0),  # from right edge moving left
                lambda y: pygame.Vector2(
                    self.game_rect.right + ASTEROID_MAX_RADIUS,
                    self.game_rect.top + y * self.game_rect.height,
                ),
            ],
            [
                pygame.Vector2(0, 1),  # from top moving down
                lambda x: pygame.Vector2(
                    self.game_rect.left + x * self.game_rect.width,
                    self.game_rect.top - ASTEROID_MAX_RADIUS,
                ),
            ],
            [
                pygame.Vector2(0, -1),  # from bottom moving up
                lambda x: pygame.Vector2(
                    self.game_rect.left + x * self.game_rect.width,
                    self.game_rect.bottom + ASTEROID_MAX_RADIUS,
                ),
            ],
        ]

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius, self.game_rect)
        asteroid.velocity = velocity
        return asteroid

    def update(self, dt):
        self.spawn_timer += dt
        if (
            self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS
            and len(self.asteroids) < MAX_NUM_ASTEROIDS
        ):
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            # edge = self.edges[3]
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            asteroid = self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
            self.asteroids.append(asteroid)
