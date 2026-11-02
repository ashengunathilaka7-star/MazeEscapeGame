# main.py

import os
import sys

import pygame

pygame.mixer.init()

victory_path = os.path.join("assets", "sounds", "victory.wav")
victory_sound = pygame.mixer.Sound(victory_path) if os.path.exists(victory_path) else None

from settings import (
    BLACK,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TOTAL_MISSIONS,
    WHITE,
)
from levels import get_level_info
from maze import Maze
from player import Player

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Escape Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 18)

current_mission = 1
score = 0
game_state = "playing"
maze = None
player = None
MOVE_INTERVAL = 130
next_move_time = 0


def load_mission():
    global maze, player, game_state, next_move_time
    maze = Maze(current_mission)
    player = Player(maze.start)
    game_state = "playing"
    next_move_time = 0


def draw_text(text, font_style, color, x, y, center=False):
    image = font_style.render(text, True, color)
    if center:
        rect = image.get_rect(center=(x, y))
        screen.blit(image, rect)
    else:
        screen.blit(image, (x, y))


def draw_hud():
    info = get_level_info(current_mission)
    pygame.draw.rect(screen, BLACK, (0, 608, SCREEN_WIDTH, 64))
    draw_text(f"Mission: {current_mission}/{TOTAL_MISSIONS}", small_font, WHITE, 12, 620)
    draw_text(f"Score: {score}", small_font, WHITE, 190, 620)
    draw_text(
        f"Crystals: {player.crystals_collected}/{len(maze.crystal_positions)}",
        small_font,
        WHITE,
        320,
        620,
    )
    draw_text(f"Key: {'Yes' if player.has_key else 'No'}", small_font, WHITE, 525, 620)
    if info:
        draw_text(info["difficulty"], small_font, WHITE, 690, 620)


def draw_game():
    screen.fill(BLACK)
    maze.draw(screen)
    player.draw(screen)
    draw_hud()
    pygame.display.flip()


def draw_victory():
    screen.fill(BLACK)

    if current_mission == TOTAL_MISSIONS:
        draw_text("THE KINGDOM IS SAVED!", font, WHITE, SCREEN_WIDTH // 2, 230, center=True)
        draw_text("You recovered the magical crystal!", small_font, WHITE, SCREEN_WIDTH // 2, 280, center=True)
        draw_text(f"Final Score: {score}", font, WHITE, SCREEN_WIDTH // 2, 340, center=True)
        draw_text("Press ESC to exit", small_font, WHITE, SCREEN_WIDTH // 2, 420, center=True)
    else:
        info = get_level_info(current_mission)
        draw_text("MISSION COMPLETED!", font, WHITE, SCREEN_WIDTH // 2, 220, center=True)
        draw_text(info["chapter"], small_font, WHITE, SCREEN_WIDTH // 2, 280, center=True)
        draw_text(f"Score: {score}", font, WHITE, SCREEN_WIDTH // 2, 330, center=True)
        draw_text("Press SPACE for the next mission", small_font, WHITE, SCREEN_WIDTH // 2, 410, center=True)

    pygame.display.flip()


def handle_movement(dx, dy):
    global score, game_state
    if not player.move(dx, dy, maze):
        return

    tile = maze.grid[player.y][player.x]
    if tile == "K":
        player.has_key = True
        maze.remove_object(player.x, player.y)
        if "collect" in maze.sounds:
            maze.sounds["collect"].play()
    elif tile == "C":
        player.crystals_collected += 1
        score += 100
        maze.remove_object(player.x, player.y)
        if "collect" in maze.sounds:
            maze.sounds["collect"].play()
    elif tile == "D" and player.has_key:
        maze.remove_object(player.x, player.y)
        if "door" in maze.sounds:
            maze.sounds["door"].play()
    elif tile == "E":
        score += 1000
        game_state = "completed"
        if victory_sound:
            victory_sound.play()


def main():
    global current_mission, score, next_move_time

    load_mission()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_state == "completed":
                    if event.key == pygame.K_SPACE and current_mission < TOTAL_MISSIONS:
                        current_mission += 1
                        load_mission()

        if game_state == "playing":
            keys = pygame.key.get_pressed()
            direction_keys = (
                (pygame.K_UP, pygame.K_w, 0, -1),
                (pygame.K_DOWN, pygame.K_s, 0, 1),
                (pygame.K_LEFT, pygame.K_a, -1, 0),
                (pygame.K_RIGHT, pygame.K_d, 1, 0),
            )
            direction = next(
                (
                    (dx, dy)
                    for arrow, wasd, dx, dy in direction_keys
                    if keys[arrow] or keys[wasd]
                ),
                None,
            )
            now = pygame.time.get_ticks()
            if direction and now >= next_move_time:
                dx, dy = direction
                handle_movement(dx, dy)
                next_move_time = now + MOVE_INTERVAL
            elif not direction:
                next_move_time = 0
            draw_game()
        elif game_state == "completed":
            draw_victory()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()







    