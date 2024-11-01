import pygame

def load_images(number_of_image):
    img_list = []

    for i in range (1, number_of_image+1):
        img = pygame.image.load(f'images/{i}.png')

        img_list.append(img)

    return  img_list