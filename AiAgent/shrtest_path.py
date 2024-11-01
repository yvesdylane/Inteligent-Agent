def Enhance_move(self, world):
    movements = [1, 2, 3, 4]  # 1: down, 2: left, 3: right, 4: up

    # If backtracking, prioritize up and down first
    if self.back:
        if self.previous_dir in movements:
            movements.remove(self.previous_dir)
        if self.Edir in movements:
            movements.remove(self.Edir)

    x = self.x
    y = self.y

    # Randomly pick a new direction if not already set
    if not self.Edir:
        self.Edir = random.choice(movements)

    # Adjust coordinates based on the chosen direction
    if self.Edir == 1:
        y += 1  # Move down
    elif self.Edir == 4:
        y -= 1  # Move up
    elif self.Edir == 3:
        x += 1  # Move right
    else:
        x -= 1  # Move left

    # Try to move to the new coordinates
    point = self.valid_move(self.Edir, x, y, world)

    if point:
        # Set previous_dir to the opposite direction of movement
        if self.Edir == 1:
            self.previous_dir = 4  # Moved down, so previous is up
        elif self.Edir == 4:
            self.previous_dir = 1  # Moved up, so previous is down
        elif self.Edir == 3:
            self.previous_dir = 2  # Moved right, so previous is left
        else:
            self.previous_dir = 3  # Moved left, so previous is right

        # Update the agent's position and mark the point as visited
        self.x, self.y = point
        self.visited.append(point)
        self.back = False  # Stop backtracking since a valid move was found

    else:
        # If no valid move, backtrack to the last visited point
        if self.visited:
            self.x, self.y = self.visited[-1]
            self.visited.pop()
            self.back = True  # Set backtracking mode
            # Prioritize up/down when backtracking
            if self.Edir == 1 or self.Edir == 4:
                movements = [3, 2]  # Prioritize left/right next
            else:
                movements = [1, 4]  # Prioritize up/down next


def valid_move_in_scope(self, dir, x, y, world):
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
        return (x_new, y_new)
    return False


def check_in_scope(self, scope, world):
    for point in scope:
        if world[2][point[1]][point[0]] is not None:
            return point
        return False

    def move_with_eyes(self, world):
        eyes = 3
        movement = [1, 2, 3, 4]
        possible_destination = [[] for _ in range(eyes)]
        dest = 0

        # Remove the previous direction from available moves
        if self.previous_dir in movement:
            movement.remove(self.previous_dir)

        chosen_dir = random.choice(movement)
        # Create scope for chosen direction
        scope_change = [-1, 0, 1]

        # Determine direction and setup previous direction
        if chosen_dir in (1, 4):  # Vertical move
            self.dir = chosen_dir
            self.previous_dir = 4 if chosen_dir == 1 else 1
            for i in range(1, eyes + 1):
                # Reset and extend scope_change based on eye range
                scope_change = [-1, 0, 1]
                if i > 1:
                    scope_change.extend([scope_change[0] - i, scope_change[-1] + i])

                for scope in scope_change:
                    path = self.valid_move_in_scope(chosen_dir, self.x + scope, self.y, world)
                    if path:
                        possible_destination[i - 1].append(path)

        elif chosen_dir in (2, 3):  # Horizontal move
            self.dir = chosen_dir
            self.previous_dir = 3 if chosen_dir == 2 else 2
            for i in range(1, eyes + 1):
                # Reset and extend scope_change based on eye range
                scope_change = [-1, 0, 1]
                if i > 1:
                    scope_change.extend([scope_change[0] - i, scope_change[-1] + i])

                for scope in scope_change:
                    path = self.valid_move_in_scope(chosen_dir, self.x, self.y + scope, world)
                    if path:
                        possible_destination[i - 1].append(path)

        # Backup: Explore previous direction if no other destination found
        if not any(possible_destination) and self.previous_dir:
            scope_change = [-1, 0, 1]
            if self.previous_dir == 1 or self.previous_dir == 4:
                for i in range(1, eyes + 1):
                    if i > 1:
                        scope_change.extend([scope_change[0] - i, scope_change[-1] + i])

                    for scope in scope_change:
                        path = self.valid_move_in_scope(self.previous_dir, self.x + scope, self.y, world)
                        if path:
                            possible_destination[i - 1].append(path)

        # Choose destination based on available paths
        if possible_destination[2]:
            dest = possible_destination[2]
        elif possible_destination[1]:
            dest = possible_destination[1]
        elif possible_destination[0]:
            dest = possible_destination[0]

        end_point = self.check_in_scope(dest, world)
        destination = end_point if end_point else random.choice(dest)

        # Set the movement path to the shortest path found
        self.movement = find_shortest_path((self.x, self.y), destination, dest)

    def moving_through_movement(self):
        if self.movement:
            self.x, self.y = self.movement[0]
            print(self.movement)
            self.movement.pop(0)
            return True
        return False





# Possible moves (up, down, left, right)
moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# BFS
def find_shortest_path(start, end, points):
    points_set = set(points)
    queue = [(start, [start])]  # List to store (current_point, path_so_far)
    visited = [start]  # List to track visited points

    while queue:
        current, path = queue.pop(0)  # Pop the first item (FIFO for BFS)

        # Check if we've reached the target
        if current == end:
            return path

        # Explore neighbors
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])

            if neighbor in points_set and neighbor not in visited:
                visited.append(neighbor)  # Mark as visited
                queue.append((neighbor, path + [neighbor]))  # Add to queue with updated path

    return None  # Return None if no path found