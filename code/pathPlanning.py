from time import time
import math

class PathPlanning:
    # map<shape, coords<int, int>>
    def __init__(self) -> None:
        pass

    def formFormation():
        changeFromation();

        #loop
        currentFormation;
        store = rotateFormation();
        for point in currentFormation:
            calcPath(point, store[point]);


    def changeFormation(shape):
        #function to change the formation of the drones
        pass

    def rotateFormation(angle):
        #function to rotate the formation of the drones
        pass

    def calcPath(start, end):
        #function to calculate the path from start to end
        pass
    
    def findPath(drone):
        #function to find the path for the drones
        #return path for drone
        pass

    def RotateCircleFormation(droneAmount, radius, center, Rotationtime):
        #function to rotate the drones in a circle
        targets = []
        for i in range(droneAmount):
            timeRotation = (int(time()) % Rotationtime) / Rotationtime * 2 * math.pi
            droneRotation = (2 * math.pi / droneAmount) * i
            totalRotation = timeRotation + droneRotation

            x = center[0] + radius * math.cos(totalRotation)
            y = center[1] + radius * math.sin(totalRotation)
            targets.append((int(x), int(y)))
        return targets



            



        