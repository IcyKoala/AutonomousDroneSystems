from Drone import DroneController
from PathPlanning import PathPlanning
from enum import Enum

class DroneManager:
    
    def __init__(self) -> None:
        self.controller = DroneController()
        self.pathPlanner = PathPlanning()
        self.droneList = []
        self.patterns = Enum('Patterns', ['DONUT'])
        self.controlSelect()  # Call controlSelect method here

    def fetchPaths(self):
        for drone in self.droneList:
            self.pathPlanner.calcPath(drone) 

    def controlSelect(self):
        controlMode = input("Select operation mode: \n 1 - Manual \n 2 - Automatic\n Selected: ")
        validInput = False
        while not validInput:
            if controlMode == "1":
                validInput = True
                self.controller.manualControl()
            elif controlMode == "2":
                validInput = False
                self.patternSelect()
            else:
                input("incorrect input, please try again")

    def patternSelect(self):
        controlMode = input("Select Patterd: \n 1 - Donut \n Selected: ")
        validInput = False
        while not validInput:
            if controlMode == "1":
                validInput = True
                self.instructDrones(self.patterns.DONUT)
            else:
                input("incorrect input, please try again: ")

    def instructDrones(self):
        finishedPattern = False
        while not finishedPattern:
            self.fetchPaths()

# Create an instance of DroneManager
manager = DroneManager()




# def checkDrones():
#         #function to check the drones
#         cameraController.checkDrone()
#         pass

#     def moveDrone(drone): #dis a thread
#         pathplanning.findpath(drone)
#         #function to move the drone
#         if droneType == physical:
#             droneController.move()
#         else:
#             unityController.move()
#         pass