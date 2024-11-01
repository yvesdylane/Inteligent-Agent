import pygame.draw

from AiAgent import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intelligent🦊️ Agent🤖️")

running = True
agent_move = True
ai_move = False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((200, 200, 200))
    display_world(screen)
    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Check if the mouse is clicked
    if mouse_click[0]:  # Check if the left mouse button is clicked
        # Check for START button
        if Start_rectM.collidepoint(mouse_pos) and not START:
            START = True
            print("start")
        else:
            START = False
            print("no started or stop")
        # Check for Agent selection
        if Ag.collidepoint(mouse_pos):
            agent_move = True
            ai_move = False

        # Check for AI selection
        if EAg.collidepoint(mouse_pos):
            agent_move = False
            ai_move = True

    pygame.draw.rect(screen, GREEN, ((WIDTH-300, 0),(300, HEIGHT)))
    if ai_move:
        Ag = pygame.draw.rect(screen, N_GREEN, Agent_rect, border_radius=5)
        screen.blit(Agent_text, (WIDTH - 190, 20))
        EAg =pygame.draw.rect(screen, BLUE, AI_rect, border_radius=5)
        screen.blit(AI_text, (WIDTH - 250, Agent_text.get_height() + 60))
    else:
        Ag = pygame.draw.rect(screen, BLUE, Agent_rect, border_radius=5)
        screen.blit(Agent_text, (WIDTH - 190, 20))
        EAg =pygame.draw.rect(screen, N_GREEN, AI_rect, border_radius=5)
        screen.blit(AI_text, (WIDTH - 250, Agent_text.get_height() + 60))

    Start_rectM = pygame.draw.rect(screen, ST, Start_rect, border_radius=5)
    screen.blit(Start_text, (WIDTH - 190, HEIGHT//2 + 10))
    if START:
        if agent_move:
            Agent.update(world)
        elif ai_move:
            AI.update(world)
    pygame.display.update()
pygame.quit()