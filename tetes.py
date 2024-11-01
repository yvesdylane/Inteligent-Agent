import csv
import random

# Check movement validity function
def check_move(layer, dir, x, y):
    x_new, y_new = x, y

    # Update coordinates based on direction
    if dir == 1:
        y_new += 1  # Move down
    elif dir == 2:
        x_new -= 1  # Move left
    elif dir == 3:
        x_new += 1  # Move right
    elif dir == 4:
        y_new -= 1  # Move up

    # Check if movement is within bounds and not blocked
    if 0 <= x_new < len(layer) and 0 <= y_new < len(layer[0]):
        if layer[x_new][y_new] is not None and layer[x_new][y_new] != 2:  # Avoid obstacles
            return x_new, y_new
    return False

# Move function that looks ahead for 3 tiles
def move(layer, x, y, previous, dir):
    directions = [1, 2, 3, 4]  # 1: Down, 2: Left, 3: Right, 4: Up

    # Remove the previous direction unless valid_moves is empty at the end
    if previous in directions:
        directions.remove(previous)

    valid_moves = []  # To store all valid movement patterns for 3 consecutive tiles

    # Loop until all directions have been checked
    while directions:
        next_move = random.choice(directions)
        directions.remove(next_move)

        path = []  # To store the valid movement in this direction
        current_x, current_y = x, y

        # Check for possible movement in this direction for 3 tiles
        for _ in range(3):
            new_position = check_move(layer, next_move, current_x, current_y)
            if new_position:
                current_x, current_y = new_position
                path.append((current_x, current_y))
            else:
                break  # Stop if movement is not possible

        # If the path is exactly 3 tiles long, it's a valid move sequence
        if len(path) == 3:
            valid_moves.append(path)

    # If no valid moves were found, add back previous direction and check again
    if not valid_moves and previous:
        directions = [previous]
        next_move = previous
        current_x, current_y = x, y
        path = []

        for _ in range(3):
            new_position = check_move(layer, next_move, current_x, current_y)
            if new_position:
                current_x, current_y = new_position
                path.append((current_x, current_y))
            else:
                break

        if len(path) == 3:
            valid_moves.append(path)

    # Choose a random movement pattern from valid_moves
    if valid_moves:
        moving = True
        movement = random.choice(valid_moves)

        # Move to the first tile in the path (only move 1 tile)
        if movement[0][0] < x:
            previous = 3  # Moved to the right
            dir = 2
        elif movement[0][0] > x:
            previous = 2  # Moved to the left
            dir = 3
        if movement[0][1] < y:
            previous = 1  # Moved upward
            dir = 4
        elif movement[0][1] > y:
            previous = 4  # Moved downward
            dir = 1

        x, y = movement[0]
        print(f"move() Position: ({x}, {y})")
    else:
        print("no path")

    return x, y, previous, dir

# Single move function
def single_move(layer, x, y, previous, dir):
    directions = [1, 2, 3, 4]  # 1: Down, 2: Left, 3: Right, 4: Up

    if previous in directions:
        directions.remove(previous)

    valid_moves = []

    while directions:
        next_move = random.choice(directions)
        directions.remove(next_move)

        path = check_move(layer, next_move, x, y)
        if path:
            valid_moves.append(path)

    if not valid_moves and previous:
        path = check_move(layer, previous, x, y)
        if path:
            valid_moves.append(path)

    if valid_moves:
        movement = random.choice(valid_moves)
        moving = True

        if movement[0] < x:
            previous = 3  # Moved to the right
            dir = 2
        elif movement[0] > x:
            previous = 2  # Moved to the left
            dir = 3
        if movement[1] < y:
            previous = 1  # Moved upward
            dir = 4
        elif movement[1] > y:
            previous = 4  # Moved downward
            dir = 1

        x, y = movement
        print(f"single_move() Position: ({x}, {y})")
    else:
        moving = False
        print("no path")

    return x, y, previous, dir

# Load world data from CSV
current_layer = []
with open('world_data.csv', 'r') as csv_in:
    csv_reader = csv.reader(csv_in)
    for row in csv_reader:
        current_layer.append([int(tile) if tile else None for tile in row])

# Initialize starting position and direction
x, y = 17, 2  # Starting position
previous_dir, current_dir = None, 1  # Start by moving down

# Run the single_move function 10 times
print("\nRunning single_move function:")
for _ in range(10):
    x, y, previous_dir, current_dir = single_move(current_layer, x, y, previous_dir, current_dir)
    print(f"Current Position: X = {x}, Y = {y}")

# Reset the position and direction
x, y = 17, 2
previous_dir, current_dir = None, 1

# Run the move function 10 times
print("\nRunning move function:")
for _ in range(10):
    x, y, previous_dir, current_dir = move(current_layer, x, y, previous_dir, current_dir)
    print(f"Current Position: X = {x}, Y = {y}")
