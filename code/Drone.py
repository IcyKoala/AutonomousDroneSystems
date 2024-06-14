import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from camera import CameraDetector
import math
import cv2
import time
import threading
import pathPlanning
import astar
from random import randrange

manualMovementDistance = 0.1
redURI = 'radio://0/80/2M/E7E7E7E7E7'
greenURI = 'radio://0/20/2M/E7E7E7E7E7'
cflib.crtp.init_drivers(enable_debug_driver=False)


class DroneController:
    def __init__(self) -> None:
        redDrone = Drone("RED")
        greenDrone = Drone("GREEN")
        self.droneList = [greenDrone, redDrone]
        pass

    def setUri(self, drone):
        match drone.getColour():
            case "RED":
                return redURI
            case "GREEN":
                return greenURI

    def startDrones(self):
        for drone in self.droneList:
            self.lock = threading.Lock()
            # Start the drone thread
            self.capture_thread = threading.Thread(target=self.controlDrone(drone), daemon=True)
            self.capture_thread.start()

    def controlDrone(self, drone):
         print(self.setUri(drone))
         with SyncCrazyflie(self.setUri(drone)) as scf:
            with MotionCommander(scf, 0.5) as mc:
                print("Stop complaining")
                time.sleep(5)

    
            

    def move(drone, direction, range):
        # function to move the drone
        pass

    def manualControl(self):
        print('Manual control')
        manualControl = True

        with SyncCrazyflie(redURI) as scf:
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

        with SyncCrazyflie(redURI) as scf:
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

    def generateCor(self):
        x = randrange(100, 800)
        y = randrange(100, 600)
        return [x, y]


    def lookAtCenter(self):
        detector = CameraDetector()
        a_star = astar.Astar()
        planning = pathPlanning.PathPlanning()
        print('Automatic control')
        autoControl = True

        with SyncCrazyflie(redURI) as scf:
            with MotionCommander(scf, 0.2) as mc:
                time.sleep(1)
                targetPos = planning.RotateCircleFormation(1,250,(500,300), 30)
                while autoControl:
                    frame = detector.get_frame()
                    if frame is None:
                        continue

                    center, dir2, frame_with_triangles = detector.detectTriangle(frame)
                    updatedFrame = True

                    cv2.rectangle(frame_with_triangles, targetPos, targetPos, (0, 0, 255), 10)

                    if center is not None and dir2 is not None:
                        while(updatedFrame):
                            droneDir = dir2
                            dronePos = center


                            targetRad = math.atan2(targetPos[1] - dronePos[1], targetPos[0] - dronePos[0])
                            targetAngle = math.degrees(targetRad)
                            print(targetAngle)

                            droneRad = math.atan2(droneDir[1], droneDir[0])
                            droneAngle = math.degrees(droneRad)
                            print(droneAngle)
                            change = targetAngle - droneAngle
                            print(change)
                            if abs(change) > 180:
                                change += 360


                            if (center[0] > targetPos[0] - 100 and center[0] < targetPos[0] + 100) and (
                                    center[1] > targetPos[1] - 100 and center[1] < targetPos[1] + 100):
                                # autoControl = False
                                targetPos = planning.RotateCircleFormation(1,250,(500,300), 30)

                            elif change > 25:
                                mc.turn_right(change)
                            elif change < -25:
                                mc.turn_left(abs(change))
                            else:
                                mc.forward(0.1)
                                # distancex = abs(center[0] - targetPos[0])
                                # distancey = abs(center[1] - targetPos[1])
                                # distance = (math.sqrt(distancex**2 + distancey**2) / 3.84) * 100
                                # mc.forward(distance)



                            mc.stop()

                            updatedFrame = False

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

    def getColour(self):
        return self.colour

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
