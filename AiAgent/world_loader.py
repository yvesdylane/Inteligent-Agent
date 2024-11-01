import pickle
import csv
import os
import pygame


def world_loader():
    world_data = []
    for layer_index in range(10):  # Assuming you have 10 layers
        # Load from .EE file if exists
        file_name_ee = f'layers/layer_{layer_index + 1}_data.EE'
        if os.path.exists(file_name_ee):  # Check if the file exists
            with open(file_name_ee, 'rb') as pickle_in:  # Open file for reading
                current_layer = pickle.load(pickle_in)  # Load layer data
                world_data.append(current_layer) # Update the world_data
        else:
            print(f"Layer {layer_index + 1} EE file does not exist. Checking CSV.")

            # Load from CSV file if EE file does not exist
            file_name_csv = f'layers/layer_{layer_index + 1}_data.csv'
            if not os.path.exists(file_name_ee) and os.path.exists(file_name_csv):
                with open(file_name_csv, 'r') as csv_in:  # Open file for reading
                    csv_reader = csv.reader(csv_in)
                    current_layer = []
                    for row in csv_reader:
                        # Convert row from string to the appropriate type (if needed)
                        current_layer.append([int(tile) if tile else None for tile in row])
                    world_data.append(current_layer)  # Update the world_data
            else:
                if not os.path.exists(file_name_csv):
                    print(f"Layer {layer_index + 1} CSV file does not exist. Skipping.")

    return world_data

def draw_world(world_data, image_list, TILE_SIZE, MAX_ROWS, MAX_COLS, player_layer, sur, scale, agent, ai):
    for index, layer in enumerate(world_data):  # Iterate over all layers
        for y in range(MAX_ROWS):
            for x in range(MAX_COLS):
                tile = layer[y][x]
                if tile is not None:
                    if index == player_layer    :
                        agent.draw(sur)
                        ai.draw(sur)
                    else:
                        img = pygame.transform.scale(
                            image_list[tile],
                            (int(image_list[tile].get_width() * scale), int(image_list[tile].get_height() * scale))
                        )
                        sur.blit(img, (x * TILE_SIZE, y * TILE_SIZE))