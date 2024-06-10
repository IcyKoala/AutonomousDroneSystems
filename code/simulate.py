import pygame
from Drone import Drone
from astar import Astar
import pathPlanning
import random
import requests

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("My Game")

def drawSquare(x, y, color = 0):
    if color == 0:
        pygame.draw.rect(screen, (0, 0, 0), (x*10, y*10, 10, 10))
    elif color == 2:
        pygame.draw.rect(screen, (255, 0, 0), (x*10, y*10, 10, 10))
    else:
        pygame.draw.rect(screen, (255, 255, 255), (x*10, y*10, 10, 10))

drones = [Drone(i) for i in range(5)]
for drone in drones:
    drone.setPosition((random.randint(0,99), random.randint(0,99)))


# Game loop
running = True
star = Astar()
mode = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            mode = not mode

    # Update the display
    screen.fill((0, 0, 0))
    json = [] 
    
    for index in range(len(drones)):
        json.append({'id': index, 'x': drones[index].getPosition()[0], 'y': drones[index].getPosition()[1]})
    print("test")
    response = requests.post('http://localhost:23336/', json=json)
    print(response)
    data = response.json()
    for drone in data:
        drones[drone['id']].setPosition((drone['x'], drone['y']))
    for drone in drones:
        drawSquare(drone.getPosition()[0], drone.getPosition()[1], 1)
        
    pygame.display.flip()

# Quit pygame
pygame.quit()