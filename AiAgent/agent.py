import pygame
import random

class Agent:
    def __init__(self, image, x, y, scale, tile_size):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.pos_x = self.x * tile_size
        self.pos_y = self.y * tile_size
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.col = 0
        self.row = 0
        self.dir = 1
        self.block_dir = 0
        self.previous_dir = 0
        self.visited = [(x, y)]  # Start with the current position as visited
        self.moving = True
        self.attain_objective = False
        self.width = self.image.get_width() // 4
        self.height = self.image.get_height() // 4
        # Extract the first image (top-left corner of the sprite sheet)
        self.current_image = self.image.subsurface((self.row, self.col, self.width, self.height))

    def draw(self, surface):
        self.pos_x = self.x * self.tile_size
        self.pos_y = self.y * self.tile_size
        surface.blit(self.current_image, (self.pos_x-4, self.pos_y - 8))

    def verify_objective(self, world):
        if world[2][self.y][self.x]:
            self.attain_objective = True

    def is_moving(self):
        if self.row <= 3:
            self.row += 1
        else:
            self.row = 0

    def update(self, world):
        self.verify_objective(world)
        if not self.attain_objective:
            self.move(world)
            if self.dir == 2 and not self.moving:  # facing left
                self.row = 1
            if self.dir == 3 and not self.moving:  # facing right
                self.row = 2
            if self.dir == 4 and not self.moving:  # facing up
                self.row = 3
            if self.dir == 1 and not self.moving:  # facing down
                self.row = 0
            if not self.moving:
                self.col = 0
            else:
                self.is_moving()
        else:
            self.moving = True

    def valid_move(self, dir, x, y, world, allow_visited=False):
        x_new = x
        y_new = y

        # Update coordinates based on direction
        if dir == 1:
            y_new = y + 1  # Move down
        elif dir == 2:
            x_new = x - 1  # Move left
        elif dir == 3:
            x_new = x + 1  # Move right
        else:
            y_new = y - 1  # Move up

        # Check if movement is allowed
        if world[1][y_new][x_new] is not None and world[7][y_new][x_new] is None:
            if allow_visited or (x_new, y_new) not in self.visited:
                return (x_new, y_new)
        return False

    def move(self, world):
        directions = [1, 2, 3, 4]
        unvisited_moves = []
        visited_moves = []

        # Remove blocked or previous directions
        if self.previous_dir in directions:
            directions.remove(self.previous_dir)
        if self.block_dir:
            directions.remove(self.block_dir)

        # First, look for unvisited valid moves
        for direction in directions:
            path = self.valid_move(direction, self.x, self.y, world)
            if path:
                unvisited_moves.append(path)
            else:
                # Check if it's a valid move through a visited tile
                path = self.valid_move(direction, self.x, self.y, world, allow_visited=True)
                if path:
                    visited_moves.append(path)

        # If no unvisited moves, fallback to visited moves
        if not unvisited_moves and visited_moves:
            unvisited_moves = visited_moves

        # If no valid unvisited or visited moves, try backtracking
        if not unvisited_moves:
            path = self.valid_move(self.previous_dir, self.x, self.y, world, allow_visited=True)
            if path:
                unvisited_moves.append(path)

        # If valid moves are found, choose one
        if unvisited_moves:
            movement = random.choice(unvisited_moves)
            self.moving = True
            if movement[0] < self.x:
                self.previous_dir = 3  # Moved to the right
                self.dir = 2
            elif movement[0] > self.x:
                self.previous_dir = 2  # Moved to the left
                self.dir = 3
            if movement[1] < self.y:
                self.previous_dir = 1  # Moved upward
                self.dir = 4
            elif movement[1] > self.y:
                self.previous_dir = 4  # Moved downward
                self.dir = 1

            # Update the agent's position and mark the tile as visited
            self.x, self.y = movement
            self.visited.append(movement)
        else:
            # No valid moves, set block_dir to prevent moving back immediately
            self.block_dir = self.dir