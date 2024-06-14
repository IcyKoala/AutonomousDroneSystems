import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from camera import CameraDetector
import math
import cv2
import time
import threading
import pathPlanning
import astar
from random import randrange
import time

manualMovementDistance = 0.1
redURI = 'radio://0/80/2M/E7E7E7E7E7'
redDone = threading.Event()
greenDone = threading.Event()
greenURI = 'radio://0/20/2M/E7E7E7E7E7'
cflib.crtp.init_drivers(enable_debug_driver=False)

def take_off(scf):
    commander= scf.cf.high_level_commander

    commander.takeoff(0.2, 2.0)
    time.sleep(3)

def land(scf):
    commander= scf.cf.high_level_commander

    commander.land(0.0, 2.0)
    time.sleep(2)

    commander.stop()

def goPosition(scf, color, pos, direc, target):
    while True:
        commander= scf.cf.high_level_commander

        droneDir = direc
        dronePos = pos
                    


        targetRad = math.atan2(target[1] - dronePos[1], target[0] - dronePos[0])
        
       

        droneRad = math.atan2(droneDir[1], droneDir[0])
       
 
        change = targetRad - droneRad
 
        

        if (pos[0] > target[0] - 100 and pos[0] < target[0] + 100) and (
            pos[1] > target[1] - 100 and pos[1] < target[1] + 100):
            if color == "red":
                redDone.set()
            else:
                greenDone.set()
            break
            

        elif abs(change) > 25:
            commander.go_to(0,0,0,change, 2, relative=True)
            time.sleep(2)
        else:
            commander.go_to(0.1,0,0,0, 0.5, relative=True)
            time.sleep(0.5)



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
        factory = CachedCfFactory(rw_cache='./cache')

        with Swarm({greenURI}, factory= factory) as swarm:
                swarm.parallel_safe(take_off)
                time.sleep(1)
                
                while autoControl:
                    frame = detector.get_frame()
                    if frame is None:
                        continue

                    center_r, dir_r, frame_with_triangles, center_g, dir_g = detector.detectTriangle(frame)
                    redDone.clear()
                    greenDone.clear()
                    targetPos = planning.RotateCircleFormation(2,250,(500,300), 30)
                    for target in targetPos:
                        cv2.rectangle(frame_with_triangles, target, target, (0, 0, 255), 10)
                    if center_r is not None and dir_r is not None and center_g is not None and dir_g is not None:
                        args = { redURI : ["red", center_r, dir_r, targetPos[0]], greenURI : ["green", center_g, dir_g, targetPos[1]]}


                        
                        swarm.parallel_safe(goPosition, args_dict = args)

                            
                        while(not greenDone.is_set()):
                            time.sleep(1)

                        cv2.imshow('frame', frame_with_triangles)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            swarm.parallel_safe(land)
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
