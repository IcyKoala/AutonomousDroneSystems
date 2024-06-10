import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from camera import CameraDetector
import math
import cv2
import time

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
                            mc.land()
                            manualControl = False
                            break

    def findCenter(self):
        detector = CameraDetector()
        print('Automatic control')
        autoControl = True

        with SyncCrazyflie(URI) as scf:
            with MotionCommander(scf, 0.1) as mc:
                while autoControl:
                    frame = detector.get_frame()
                    if frame is None:
                        continue

                    center, orientation_vector, frame_with_triangles = detector.detectTriangle(frame)

                    if center is not None:
                        if center[0] < 850:
                            mc.left(0.1)
                        else:
                            mc.right(0.1)
                        if center[1] < 500:
                            mc.forward(0.1)
                        else:
                            mc.back(0.1)

                    center = None

                    cv2.imshow('frame', frame_with_triangles)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        autoControl = False
                        break

                detector.release()
                cv2.destroyAllWindows()

    def lookAtCenter(self):
        detector = CameraDetector()
        print('Automatic control')
        autoControl = True

        with SyncCrazyflie(URI) as scf:
            with MotionCommander(scf, 0.2) as mc:
                time.sleep(3)
                while autoControl:
                    frame = detector.get_frame()
                    if frame is None:
                        continue

                    center, orientation_vector, frame_with_triangles = detector.detectTriangle(frame)


                    droneDir = orientation_vector
                    dronePos = center
                    targetPos = [100,100]

                    targetRad = math.atan2(targetPos[1]-dronePos[1], targetPos[0]-dronePos[0])
                    targetAngle = math.degrees (targetRad)
                    print(targetAngle)

                    droneRad = math.atan2(droneDir[1], droneDir[0])
                    droneAngle = math.degrees (droneRad)
                    print(droneAngle)
                    change = targetAngle-droneAngle
                    print(change)
                    if abs(change) > 180:
                        change += 360
                    if change > 25:
                        mc.turn_right(change)
                        time.sleep(0.5)
                    elif change < -25:
                        mc.turn_left(abs(change))
                        time.sleep(0.5)
                    else:
                        mc.forward(0.05)

                    if (center[0] > targetPos[0] - 50 and center[0] < targetPos[0] + 50) and (center[1] > targetPos[1] - 50 and center[1] < targetPos[1] + 50):
                        autoControl = False
                        print('WINNNNNNNNNNNNNNNNNNNNNNNNjkewhf;oishfhdakdhauisdNNNN')

                    cv2.imshow('frame', frame_with_triangles)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                detector.release()
                cv2.destroyAllWindows()

        
       


class Drone:
    def __init__(self, colour) -> None:
        self.position = (0, 0)
        self.target = (0, 0)
        self.colour = colour

    def getPosition(self):
        return self.position

    def getTarget(self):
        return self.target

    def setPosition(self, position):
        self.position = position

    def setTarget(self, target):
        self.target = target

if __name__ == '__main__':
    controller = DroneController()
    controller.lookAtCenter()