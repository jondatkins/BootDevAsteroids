import pygame
import constants
from logger import log_state
from logger import log_event
import subprocess
import time
import os
import json
import sys
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.display.set_caption("AsteroidsGame")
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    make_hyprland_window_float(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()
    clock = pygame.time.Clock()
    dt = 0
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                # print("Game Over!")
                # sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()

        pygame.display.flip()
        time = clock.tick(60)
        dt = time / 1000


def make_hyprland_window_float(width: int, height: int):
    """Float and resize the Pygame window if Hyprland is running."""
    # Check if Hyprland is running
    if not os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
        print("Hyprland not detected — skipping window float.")
        return

    try:
        # Give Hyprland time to register the new window
        time.sleep(0.3)

        # Float, resize, and center the focused window
        subprocess.run(["hyprctl", "dispatch", "togglefloating"], check=False)
        subprocess.run(
            ["hyprctl", "dispatch", "resizeactive", f"{width} {height}"], check=False
        )
        subprocess.run(["hyprctl", "dispatch", "centerwindow"], check=False)
    except Exception as e:
        print("Hyprland window adjustment failed:", e)


def make_hyprland_window_float_2(title: str, width: int, height: int):
    """Find the Pygame window by title and float + resize it in Hyprland."""
    # Check if Hyprland is running
    if not os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
        print("Hyprland not detected — skipping window float.")
        return

    try:
        # Give Hyprland time to register the new window
        time.sleep(0.5)

        # Query all windows in JSON format
        result = subprocess.run(
            ["hyprctl", "clients", "-j"], capture_output=True, text=True, check=False
        )
        clients = json.loads(result.stdout or "[]")

        # Find window whose title matches (exact or case-insensitive)
        target = next(
            (c for c in clients if c.get("title", "").lower() == title.lower()), None
        )
        if not target:
            print(f"Could not find window titled '{title}'")
            return

        address = target["address"]

        # Float, resize, and center that window explicitly
        subprocess.run(
            ["hyprctl", "dispatch", "togglefloating", f"address:{address}"], check=False
        )
        subprocess.run(
            [
                "hyprctl",
                "dispatch",
                "resizewindowpixel",
                f"address:{address}",
                f"{width} {height}",
            ],
            check=False,
        )
        subprocess.run(
            ["hyprctl", "dispatch", "centerwindow", f"address:{address}"], check=False
        )

        print(f"Floated and resized window '{title}' ({width}x{height})")

    except Exception as e:
        print("Hyprland window adjustment failed:", e)


if __name__ == "__main__":
    main()
