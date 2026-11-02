import pygame
import os

from settings import TILE_SIZE, PLAYER_COLOR, IMAGE_DIR


class Player:

    def __init__(self, start_position):

        self.x, self.y = start_position
        self.has_key = False

        image_path = os.path.join(IMAGE_DIR, "player.png")

        if os.path.exists(image_path):
            image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(
                image, (TILE_SIZE, TILE_SIZE)
            )
        else:
            self.image = None

    def move(self, dx, dy, maze):

        new_x = self.x + dx
        new_y = self.y + dy

        if maze.can_enter(new_x, new_y, self.has_key):

            self.x = new_x
            self.y = new_y
            return True

        return False

    def draw(self, screen):

        if self.image:
            screen.blit(
                self.image,
                (self.x * TILE_SIZE, self.y * TILE_SIZE)
            )
        else:
            pygame.draw.rect(
                screen,
                PLAYER_COLOR,
                (
                    self.x * TILE_SIZE + 5,
                    self.y * TILE_SIZE + 5,
                    TILE_SIZE - 10,
                    TILE_SIZE - 10
                )
            )