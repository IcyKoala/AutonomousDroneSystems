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

    def rotateLineFormation(self,droneAmount, length, center, rotationTime):
        pass

    def rotateSqauareFormation(self, droneAmount, sideLength, center, rotationTime):
        if droneAmount < 4:
            return self.rotateLineFormation(droneAmount, sideLength, center, rotationTime)
        targets = []
        corners = [(1,1) , (1, -1), (-1, -1), (-1, 1)]
        pheta = (int(time()) % rotationTime) / rotationTime * 2 * math.pi
        for i in range(4):
            drones = droneAmount // 4
            if i < droneAmount % 4:
                drones += 1
            for j in range(drones):
                
                x = (corners[i][0] * sideLength / 2 + (corners[i-1][0] - corners[i][0]) * j/drones * sideLength /2)
                y = (corners[i][1] * sideLength / 2 + (corners[i-1][1] - corners[i][1]) * j/drones * sideLength /2)
                rotatedX = x *math.cos(pheta) - y * math.sin(pheta)
                rotatedy = x * math.sin(pheta) + y* math.cos(pheta)
                targets.append((int(rotatedX + center[0]), int(rotatedy + center[1])))
        
        
        return targets
            
        

    def RotateCircleFormation(self, droneAmount, radius, center, Rotationtime):
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



            



        
