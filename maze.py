# maze.py

import os
import random
from collections import deque

import pygame

from settings import (
    DOOR_COLOR,
    EXIT_COLOR,
    FLOOR_COLOR,
    IMAGE_DIR,
    KEY_COLOR,
    MAZE_COLS,
    MAZE_ROWS,
    SOUND_DIR,
    TILE_SIZE,
    WALL_COLOR,
)


class Maze:
    def load_image(self, filename):
        if not pygame.display.get_init():
            pygame.display.init()
            pygame.display.set_mode((1, 1))

        path = os.path.join(IMAGE_DIR, filename)
        if os.path.exists(path):
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return None

    def __init__(self, level_number):
        self.cols = MAZE_COLS if MAZE_COLS % 2 == 1 else MAZE_COLS - 1
        self.rows = MAZE_ROWS if MAZE_ROWS % 2 == 1 else MAZE_ROWS - 1
        self.random = random.Random(level_number * 100)
        self.grid = [["#" for _ in range(self.cols)] for _ in range(self.rows)]
        self.start = (1, 1)
        self.exit_position = self.start

        self.images = {
            "#": self.load_image("wall.png"),
            " ": self.load_image("floor.png"),
            "K": self.load_image("key.png"),
            "D": self.load_image("door.png"),
            "E": self.load_image("exit.png"),
        }

        self.sounds = {}
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        for name in ("collect", "door"):
            path = os.path.join(SOUND_DIR, f"{name}.wav")
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)

        self.generate_maze()
        self.place_objects()

    def generate_maze(self):
        stack = [self.start]
        self.grid[self.start[1]][self.start[0]] = " "

        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

        while stack:
            x, y = stack[-1]
            neighbours = []

            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if 1 <= nx < self.cols - 1 and 1 <= ny < self.rows - 1 and self.grid[ny][nx] == "#":
                    neighbours.append((nx, ny, dx, dy))

            if neighbours:
                nx, ny, dx, dy = self.random.choice(neighbours)
                self.grid[y + dy // 2][x + dx // 2] = " "
                self.grid[ny][nx] = " "
                stack.append((nx, ny))
            else:
                stack.pop()

    def find_path(self, start, end):
        queue = deque([start])
        parents = {start: None}

        while queue:
            current = queue.popleft()
            if current == end:
                break

            x, y = current
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx = x + dx
                ny = y + dy
                neighbour = (nx, ny)
                if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == " " and neighbour not in parents:
                    parents[neighbour] = current
                    queue.append(neighbour)

        if end not in parents:
            return []

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()
        return path

    def place_objects(self):
        queue = deque([self.start])
        parents = {self.start: None}

        while queue:
            x, y = queue.popleft()
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                nx = x + dx
                ny = y + dy
                neighbour = (nx, ny)
                if 0 <= nx < self.cols and 0 <= ny < self.rows and self.grid[ny][nx] == " " and neighbour not in parents:
                    parents[neighbour] = (x, y)
                    queue.append(neighbour)

        exit_position = max(parents, key=lambda position: self.distance(parents, position))
        path = self.find_path(self.start, exit_position)

        if len(path) < 5:
            raise ValueError("Generated maze path is too short.")

        key_index = max(1, len(path) // 3)
        door_index = max(key_index + 1, (len(path) * 2) // 3)
        if door_index >= len(path) - 1:
            door_index = len(path) - 2

        key_x, key_y = path[key_index]
        door_x, door_y = path[door_index]
        exit_x, exit_y = exit_position

        self.grid[key_y][key_x] = "K"
        self.grid[door_y][door_x] = "D"
        self.grid[exit_y][exit_x] = "E"
        self.exit_position = exit_position

    @staticmethod
    def distance(parents, position):
        distance = 0
        current = position
        while parents[current] is not None:
            distance += 1
            current = parents[current]
        return distance

    def can_enter(self, x, y, has_key):
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return False

        tile = self.grid[y][x]
        if tile == "#":
            return False
        if tile == "D" and not has_key:
            return False
        return True

    def remove_object(self, x, y):
        self.grid[y][x] = " "

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                tile = self.grid[y][x]
                image = self.images.get(tile)

                if image:
                    screen.blit(image, (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    colors = {
                        "#": WALL_COLOR,
                        " ": FLOOR_COLOR,
                        "K": KEY_COLOR,
                        "D": DOOR_COLOR,
                        "E": EXIT_COLOR,
                    }
                    pygame.draw.rect(
                        screen,
                        colors.get(tile, FLOOR_COLOR),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )