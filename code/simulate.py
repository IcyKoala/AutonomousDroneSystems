import pygame
from Drone import Drone
from astar import Astar
import pathPlanning
import random

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

drones = [Drone(i) for i in range(20)]
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


    # Update game logic

    # Render the screen
    screen.fill((0, 0, 0))
    planning = pathPlanning.PathPlanning()
    if mode:
        targets = planning.rotateSqauareFormation(len(drones), 35, (50,50), 40)
    else:
        targets = planning.RotateCircleFormation(len(drones), 35, (50,50), 100)
    
    
    for target in targets:
        drawSquare(target[0], target[1], 2)
    drones = star.calc_targets(drones, targets)
    
   


    for drone in drones:
        path = star.findPath(drone.getPosition(), drone.getTarget())
   
        drawSquare(drone.getPosition()[0], drone.getPosition()[1], 0)
        drone.setPosition(path)
        drawSquare(drone.getPosition()[0], drone.getPosition()[1], 1)

    pygame.display.flip()

# Quit pygame
pygame.quit()