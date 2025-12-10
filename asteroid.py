import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, game_rect):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.explosion = pygame.mixer.Sound(
            "./Sounds/mixkit-arcade-game-explosion-1699.wav"
        )
        self.game_rect = game_rect
        self.clamp_to_rect(self.game_rect)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.clamp_to_rect(self.game_rect)

    def rotate(self, rot):
        self.rotation += rot

    # Immediately .kill() itself (think about it: this asteroid is always destroyed, but maybe we'll spawn new smaller ones, depending on its size).
    # If the radius of the asteroid is less than or equal to ASTEROID_MIN_RADIUS, just return; this was a small asteroid and we're done.
    # Otherwise, we need to spawn 2 new asteroids like so:
    #
    #     Call log_event("asteroid_split") (be sure to import log_event at the top of the file).
    #     Call random.uniform to generate a random angle between 20 and 50 degrees (be sure to import the standard random library at the top of the file).
    #     Call the .rotate method on the asteroid's velocity vector to create a new vector representing the first new asteroids movement.
    #     Call the .rotate again for the second new asteroid, but this time rotate it in the opposite direction (negative angle).
    #     Compute the new radius of the smaller asteroids using the formula old_radius - ASTEROID_MIN_RADIUS.
    #     Create two new Asteroid objects at the current asteroid position with the new radius.
    #     Set the first's .velocity to the first new vector, but make it move faster by scaling it up (multiplying) by 1.2.
    #     Do the same for the second asteroid, but with the second new vector.
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.explosion.play()
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        new_vector_one = self.velocity.rotate(random_angle)
        new_vector_two = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_one = Asteroid(
            self.position.x, self.position.y, new_radius, self.game_rect
        )
        asteroid_two = Asteroid(
            self.position.x, self.position.y, new_radius, self.game_rect
        )
        asteroid_one.velocity = new_vector_one * 1.2
        asteroid_two.velocity = new_vector_two * 1.2
        self.explosion.play()
