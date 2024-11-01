from AiAgent.Enhance_agent import EAgent
from AiAgent.images import load_images
from AiAgent.world_loader import world_loader, draw_world
import pygame
from  AiAgent.agent import Agent
import copy

pygame.init()


FPS = 10
clock = pygame.time.Clock()

scale = 0.35
MAX_ROWS = 26
MAX_COLS = 36
TILE_SIZE = int(82*scale)
number_of_image = 88
player_layer = 5

WIDTH = MAX_COLS * TILE_SIZE + 300
HEIGHT = MAX_ROWS * TILE_SIZE

WHITE = (255, 255, 255)
N_GREEN = (40, 150, 60)
ST = (60, 190, 80)
GREEN = (50, 90, 80)
BLUE = (40, 90, 160)
START = False
font = pygame.font.SysFont("Poppins",36)
Agent_text = font.render("Agent🦊️",True ,WHITE)
AI_text = font.render("Enhance Agent🤖️",True ,WHITE)
Agent_rect = ((WIDTH - 200, 10), (Agent_text.get_width()+20, Agent_text.get_height() + 20))
AI_rect = ((WIDTH - 260, Agent_text.get_height() + 50), (AI_text.get_width()+20, AI_text.get_height() + 20))
Start_text = font.render("START",True ,WHITE)
Start_rect = ((WIDTH - 200, HEIGHT//2), (Start_text.get_width()+20, Start_text.get_height() + 20))

world = world_loader()
image_list =load_images(number_of_image)

Agent = Agent(image_list[83], 17, 1, scale+0.21, TILE_SIZE)
AI = EAgent(image_list[83], 17, 1, scale+0.21, TILE_SIZE)

def display_world(sur):
    draw_world(world, image_list, TILE_SIZE, MAX_ROWS, MAX_COLS, player_layer, sur, scale, Agent, AI)
