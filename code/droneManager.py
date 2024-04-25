
class droneManager:
    def __init__(self) -> None:
        pass

    def checkDrones():
        #function to check the drones
        cameraController.checkDrone()
        pass

    def moveDrone(drone): #dis a thread
        pathplanning.findpath(drone)
        #function to move the drone
        if droneType == physical:
            droneController.move()
        else:
            unityController.move()
        pass