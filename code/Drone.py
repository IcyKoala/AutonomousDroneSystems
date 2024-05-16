# import cflib.crtp
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.positioning.motion_commander import MotionCommander

import cv2 as cv

manualMovementDistance = 0.1

class DroneController:
    def __init__(self) -> None:
       pass

    def move(drone, direction, range):
        #function to move the drone
        pass

    def manualControl(self):
        manualControl = True
        while manualControl == True:
            # with SyncCrazyflie(URI) as scf:
            #     with MotionCommander(scf, 1.7) as mc:
                    instruction = input("Next instruction: ").upper()
                    print(instruction)
                    match instruction:
                        case "W":                            
                            print("going forward")
                            # mc.forward(manualMovementDistance)
                        case "S":
                            print("going backwards")
                            # mc.back(manualMovementDistance)
                        case "A":
                            print("turning left")
                            
                        case "D":
                            print("turning right")

                        case "I":
                            # mc.down(1.6)
                            # mc.land
                            manualControl = False
                            break
    
class Drone:
    def __init__(self, colour) -> None:
        self.colour = colour
        pass