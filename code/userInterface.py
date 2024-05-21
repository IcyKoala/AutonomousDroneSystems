from enum import Enum
from Drone import DroneController
from DroneManager import DroneManager

class userInterface:
    def __init__(self) -> None:
        self.controller = DroneController()
        self.droneManager = DroneManager()
        self.patterns = Enum('Patterns', ['DONUT'])
        self.controlSelect()

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
                self.droneManager.instructDrones(self.patterns.DONUT)
            else:
                controlMode = input("incorrect input, please try again: ")

# Create an instance of DroneManager
manager = userInterface()
