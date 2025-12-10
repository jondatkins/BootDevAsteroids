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
from constants import GAME_RECT_WIDTH
from constants import GAME_RECT_HEIGHT
from constants import GAME_RECT_WIDTH_OFFSET
from constants import GAME_RECT_HEIGHT_OFFSET


def show_score(x, y, screen, font, score):
    score = font.render(f"Score : {999}", True, (255, 255, 255))
    screen.blit(score, (400, 400))


# Draws a border inside the pygame window.
def draw_game_border(screen, width, height):
    colour = (255, 0, 0)
    # width_offset = 200
    # height_offset = 200
    game_box_width = width - GAME_RECT_WIDTH_OFFSET
    game_box_height = height - GAME_RECT_HEIGHT_OFFSET
    x_pos = GAME_RECT_WIDTH_OFFSET // 2
    y_pos = GAME_RECT_HEIGHT_OFFSET // 2
    game_rect = pygame.Rect(x_pos, y_pos, game_box_width, game_box_height)
    pygame.draw.rect(
        screen,
        colour,
        game_rect,
        4,
    )
    return game_rect


def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("AsteroidsGame")
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    # make_hyprland_window_float(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    # make_hyprland_window_float_2(
    #     "AsteroidsGame", constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT
    # )
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    player = Player(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 2)

    asteroid_field = AsteroidField(
        draw_game_border(screen, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    )
    clock = pygame.time.Clock()
    dt = 0
    # font = pygame.font.Font("freesansbold.ttf", 32)
    score = 0
    score_increment = 10
    game_over = False
    running = True

    # print(f"widt: {w} height: {h}")
    while running:
        log_state()
        font = pygame.font.Font(None, 36)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("quitting")
                running = False

        screen.fill("black")
        w, h = pygame.display.get_surface().get_size()
        draw_game_border(screen, w, h)

        if not game_over:
            for sprite in drawable:
                sprite.draw(screen)

            updatable.update(dt)

            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    log_event("player_hit")
                    if player.lives < 1:
                        # print("Game Over!")
                        # game_over = font.render(f"Game Over!", True, (255, 255, 255))
                        # screen.blit(game_over, (400, 400))
                        game_over = True
                    else:
                        # player.lives -= 1
                        print(f"player now has {player.lives}")

            for asteroid in asteroids:
                for shot in shots:
                    if shot.collides_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        asteroid.split()
                        score += score_increment

            # Draw the score to the screen
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            player_lives = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            screen.blit(player_lives, (700, 10))
            pygame.display.flip()
            time = clock.tick(60)
            dt = time / 1000
        else:
            screen.fill("black")
            game_over = font.render(f"Game Over!", True, (255, 255, 255))
            screen.blit(game_over, (400, 400))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_y] or keys[pygame.K_SPACE]:
                player.lives = 3
                game_over = False
                score = 0
            if keys[pygame.K_q] or keys[pygame.K_SPACE]:
                pygame.quit()
                # sys.exit()
                running = False


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
