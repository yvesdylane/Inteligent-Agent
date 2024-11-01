import pygame.transform
import random
import os
import pickle


class Agent():
    def __init__(self, image, x, y, scale, tile_size):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.x = x
        self.y = y
        self.width = self.image.get_width() // 4
        self.height = self.image.get_height() // 4
        self.moving = False
        self.dir = 1
        self.previous_dir = 0
        self.col = 0
        self.row = 0
        self.tile_size =  tile_size
        self.world = self.layers()
        # Extract the first image (top-left corner of the sprite sheet)
        self.current_image = self.image.subsurface((self.row, self.col, self.width, self.height))

    def draw(self, sur):
        sur.blit(self.current_image, (self.x, self.y-5))

    def update(self):
        self.single_move()
        if self.dir == 2 and not self.moving: # facing left
            self.row = 1
        if self.dir == 3 and not self.moving: # facing right
            self.row = 2
        if self.dir == 4 and not self.moving: # facing up
            self.row = 3
        if self.dir == 1 and not self.moving:
            self.row = 0
        if not self.moving:
            self.col = 0
        else:
            self.is_moving()

    def is_moving(self):
        if self.row <=3:
            self.row += 1
        else:
            self.row = 0

    def check_move(self, dir, x, y):
        x_new = x
        y_new = y

        # Update coordinates based on direction
        if dir == 1:
            y_new = y + 1  # Move sown (assuming grid directions)
        elif dir == 2:
            x_new = x - 1  # Move left
        elif dir == 3:
            x_new = x + 1  # Move right
        else:
            y_new = y - 1  # Move up
        # Check if movement is allowed (assuming world is a 3D grid)
        if self.world[0][y_new][x_new] is not None and self.world[1][y_new][x_new] is None:
            return (x_new, y_new)
        else:
            return False

    def move(self):
        x = self.x // self.tile_size
        y = self.y // self.tile_size
        directions = [1, 2, 3, 4]  # 1: Down, 2: Left, 3: Right, 4: Up

        # Remove the previous direction unless valid_moves is empty at the end
        if self.previous_dir in directions:
            directions.remove(self.previous_dir)

        valid_moves = []  # To store all valid movement patterns for 3 consecutive tiles

        # Loop until all directions have been checked
        while directions:
            # Randomly choose a direction
            next_move = random.choice(directions)
            directions.remove(next_move)  # Remove this direction to avoid repeating

            path = []  # To store the valid movement in this direction
            current_x, current_y = x, y  # Starting point for this direction

            # Check for possible movement in this direction for 3 tiles
            for _ in range(3):
                new_position = self.check_move(next_move, current_x, current_y)
                if new_position:
                    current_x, current_y = new_position
                    path.append((current_x, current_y))
                else:
                    break  # Stop if movement is not possible

            # If the path is exactly 3 tiles long, it's a valid move sequence
            if len(path) == 3:
                valid_moves.append(path)

        # If no valid moves were found, add back previous direction and check again
        if not valid_moves and self.previous_dir:
            directions = [self.previous_dir]
            next_move = self.previous_dir  # Check only in the previous direction
            current_x, current_y = x, y  # Starting point

            path = []  # Reset path

            for _ in range(3):
                new_position = self.check_move(next_move, current_x, current_y)
                if new_position:
                    current_x, current_y = new_position
                    path.append((current_x, current_y))
                else:
                    break  # Stop if movement is not possible

            # Add this path if it's exactly 3 tiles long
            if len(path) == 3:
                valid_moves.append(path)

        # Choose a random movement pattern from valid_moves
        if valid_moves:
            self.moving = True
            movement = random.choice(valid_moves)

            # Move to the first tile in the path (only move 1 tile)
            if movement[0][0] * self.tile_size < self.x:
                self.previous_dir = 3  # Moved to the right
                self.dir = 2
            elif movement[0][0] * self.tile_size > self.x:
                self.previous_dir = 2  # Moved to the left
                self.dir = 3
            if movement[0][1] * self.tile_size < self.y:
                self.previous_dir = 1  # Moved upward
                self.dir = 4
            elif movement[0][1] * self.tile_size > self.y:
                self.previous_dir = 4  # Moved downward
                self.dir = 1

            # Update the current position
            self.x = movement[0][0] * self.tile_size
            self.y = movement[0][1] * self.tile_size
        else:
            self.moving = False
            print("no path")

    def single_move(self):
        x = self.x // self.tile_size
        y = self.y // self.tile_size
        directions = [1, 2, 3, 4]  # 1: Down, 2: Left, 3: Right, 4: Up

        # Remove the previous direction unless valid_moves is empty at the end
        if self.previous_dir in directions:
            directions.remove(self.previous_dir)

        valid_moves = []  # To store all valid movement patterns for 3 consecutive tiles

        # Loop until all directions have been checked
        while directions:
            # Randomly choose a direction
            next_move = random.choice(directions)
            directions.remove(next_move)  # Remove this direction to avoid repeating

            path = self.check_move(next_move, x, y)

            if path:
                valid_moves.append(path)

        if not valid_moves and self.previous_dir:
            path = self.check_move(self.previous_dir, x, y)

            if path:
                valid_moves.append(path)

        if valid_moves:
            self.moving = True
            movement = random.choice(valid_moves)

            # Move to the first tile in the path (only move 1 tile)
            if movement[0][0] * self.tile_size < self.x:
                self.previous_dir = 3  # Moved to the right
                self.dir = 2
            elif movement[0][0] * self.tile_size > self.x:
                self.previous_dir = 2  # Moved to the left
                self.dir = 3
            if movement[0][1] * self.tile_size < self.y:
                self.previous_dir = 1  # Moved upward
                self.dir = 4
            elif movement[0][1] * self.tile_size > self.y:
                self.previous_dir = 4  # Moved downward
                self.dir = 1

            # Update the current position
            self.x = movement[0][0] * self.tile_size
            self.y = movement[0][1] * self.tile_size
        else:
            self.moving = False
            print("no path")

    def layers(self):
        world_data = []
        layer = [2,8,3]
        for layer_index in layer:  # Assuming you have 10 layers
            # Load from .EE file if exists
            file_name_ee = f'layers/layer_{layer_index}_data.EE'
            if os.path.exists(file_name_ee):  # Check if the file exists
                with open(file_name_ee, 'rb') as pickle_in:  # Open file for reading
                    current_layer = pickle.load(pickle_in)  # Load layer data
                    world_data.append(current_layer)  # Update the world_data

        return world_data