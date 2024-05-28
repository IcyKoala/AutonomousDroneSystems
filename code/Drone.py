import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from camera import CameraDetector
import cv2

import cv2 as cv

manualMovementDistance = 0.1
URI = 'radio://0/80/2M/E7E7E7E7E7'
cflib.crtp.init_drivers(enable_debug_driver=False)


class DroneController:
    def __init__(self) -> None:
        pass

    def move(drone, direction, range):
        # function to move the drone
        pass

    def manualControl(self):
        print('Manual control')
        manualControl = True

        with SyncCrazyflie(URI) as scf:
            with MotionCommander(scf, 0.5) as mc:
                while manualControl:
                    print('Takeoff')
                    instruction = input("Next instruction: ").upper()
                    print(instruction)
                    match instruction:
                        case "W":
                            print("going forward")
                            mc.forward(manualMovementDistance)
                        case "S":
                            print("going backwards")
                            mc.back(manualMovementDistance)
                        case "A":
                            print("turning left")
                            mc.left(manualMovementDistance)

                        case "D":
                            print("turning right")
                            mc.right(manualMovementDistance)
                        case "I":
                            mc.down(0.4)
                            mc.land
                            manualControl = False
                            break


    def findCenter(self):
        detector = CameraDetector()
        print('Automatic control')
        autoControl = True

        with SyncCrazyflie(URI) as scf:
            with MotionCommander(scf, 0.2) as mc:
                while autoControl:
                    frame = detector.get_frame()
                    if frame is None:
                        continue

                    center = detector.detectTriangle(frame)

                    if center is not None:
                        cv2.imshow('frame', center)

                    if center[1] < 500:
                        mc.right(0.1)
                    else:
                        mc.left(0.1)
                    if center[0] < 500:
                        mc.forward(0.1)
                    else:
                        mc.back(0.1)


                detector.release()
                cv2.destroyAllWindows()



class Drone:
    def __init__(self, colour) -> None:
        self.colour = colour
        pass
