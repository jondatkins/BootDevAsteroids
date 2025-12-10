import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] | None = None

    def __init__(self, x, y, radius):
        # we will be using this later
        # if hasattr(self, "containers"):
        #     super().__init__(self.containers)
        # else:
        #     super().__init__()
        if self.containers:
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    # Returns true if this circle collides with another circle,
    # false otherwise.
    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        if distance < self.radius + other.radius:
            return True
        return False

    def draw(self, screen):
        # must override
        pass

    def update(self, dt):
        # must override
        pass

    def clamp_to_rect(self, rect):
        # Clamp center so the circle never crosses boundary
        self.position.x = max(
            rect.left + self.radius, min(self.position.x, rect.right - self.radius)
        )
        self.position.y = max(
            rect.top + self.radius, min(self.position.y, rect.bottom - self.radius)
        )
        # print(f"{self.radius}")
