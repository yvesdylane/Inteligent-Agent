import pygame
import random
from collections import deque

class EAgent:
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
        self.visited = [(x, y)]
        self.moving = True
        self.attain_objective = False
        self.width = self.image.get_width() // 4
        self.height = self.image.get_height() // 4
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
            if self.dir == 2 and not self.moving:
                self.row = 1
            if self.dir == 3 and not self.moving:
                self.row = 2
            if self.dir == 4 and not self.moving:
                self.row = 3
            if self.dir == 1 and not self.moving:
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

        if dir == 1:
            y_new = y + 1
        elif dir == 2:
            x_new = x - 1
        elif dir == 3:
            x_new = x + 1
        else:
            y_new = y - 1

        if world[1][y_new][x_new] is not None and world[7][y_new][x_new] is None:
            if allow_visited or (x_new, y_new) not in self.visited:
                return (x_new, y_new)
        return False

    def find_shortest_path(self, start, end, world):
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()
            if current == end:
                return path

            for dir in [1, 2, 3, 4]:
                next_pos = self.valid_move(dir, *current, world)
                if next_pos and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [next_pos]))
        return []

    def move(self, world):
        objective_position = None
        for row in range(len(world[2])):
            for col in range(len(world[2][row])):
                if world[2][row][col]:  # Objective tile
                    objective_position = (col, row)

        if objective_position:
            path = self.find_shortest_path((self.x, self.y), objective_position, world)
            if path:
                next_step = path[1]  # Move to the next step on the path
                self.x, self.y = next_step
                self.visited.append(next_step)
                self.moving = True
                return

        # Fallback to current movement method if no path to objective
        directions = [1, 2, 3, 4]
        unvisited_moves = []
        visited_moves = []

        if self.previous_dir in directions:
            directions.remove(self.previous_dir)
        if self.block_dir:
            directions.remove(self.block_dir)

        for direction in directions:
            path = self.valid_move(direction, self.x, self.y, world)
            if path:
                unvisited_moves.append(path)
            else:
                path = self.valid_move(direction, self.x, self.y, world, allow_visited=True)
                if path:
                    visited_moves.append(path)

        if not unvisited_moves and visited_moves:
            unvisited_moves = visited_moves

        if not unvisited_moves:
            path = self.valid_move(self.previous_dir, self.x, self.y, world, allow_visited=True)
            if path:
                unvisited_moves.append(path)

        if unvisited_moves:
            movement = random.choice(unvisited_moves)
            self.moving = True
            if movement[0] < self.x:
                self.previous_dir, self.dir = 3, 2
            elif movement[0] > self.x:
                self.previous_dir, self.dir = 2, 3
            if movement[1] < self.y:
                self.previous_dir, self.dir = 1, 4
            elif movement[1] > self.y:
                self.previous_dir, self.dir = 4, 1

            self.x, self.y = movement
            self.visited.append(movement)
        else:
            self.block_dir = self.dir
