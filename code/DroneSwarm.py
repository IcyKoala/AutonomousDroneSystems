import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from camera import CameraDetector
import math
import cv2
import time
import pathPlanning
import astar
from random import randrange


from cflib.crazyflie import syncCrazyflie
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm


manualMovementDistance = 0.1
uris = [
    'radio://0/20/2M/E7E7E7E7E7',
    'radio://0/80/2M/E7E7E7E7E7',
    # Add more URIs if you want more copters in the swarm
]
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
                return uris[1]
            case "GREEN":
                return uris[0]
            
    def take_off(scf):
        commander= scf.cf.high_level_commander

        commander.takeoff(0.5, 2.0)
        time.sleep(3)

    def land(scf):
        commander= scf.cf.high_level_commander

        commander.land(0.0, 2.0)
        time.sleep(2)

        commander.stop()

    def goToCoord(scf: syncCrazyflie.SyncCrazyflie, sequence):
        cf = scf.cf

        for arguments in sequence:
            commander = scf.cf.high_level_commander
            

            x, y, z = arguments[0], arguments[1], arguments[2]
            duration = arguments[3]

            print('Setting position {} to cf {}'.format((x, y, z), cf.link_uri))
            commander.go_to(x, y, z, 0, duration, relative=True)
            time.sleep(duration)


    def startDrones(self):
        detector = CameraDetector()
        frame = detector.get_frame()
        autoControl = True
        planning = pathPlanning.PathPlanning()
        duration = 2

        cflib.crtp.init_drivers()
        factory = CachedCfFactory(rw_cache='./cache')
        with Swarm(uris, factory=factory) as swarm:
            print('Connected to  Crazyflies')
            swarm.reset_estimators()

            swarm.parallel_safe(self.take_off)
            

        while autoControl:
            if frame is None:
                continue

            center, dir2, frame_with_triangles = detector.detectTriangle(frame)
            updatedFrame = True

            

            if center is not None and dir2 is not None:
                while(updatedFrame):

                    targets = planning.RotateCircleFormation(2,250,(500,300), 30)
                    for target in targets:
                        cv2.rectangle(frame_with_triangles, target, target, (0, 0, 255), 10)

                    seq_args = {
                        uris[0]: [targets[0], 0.0, duration],
                        uris[1]: [targets[1], 0.0, duration],
                    }
                    swarm.parallel_safe(self.goToCoord, args_dict=seq_args)

                    updatedFrame = False

                cv2.imshow('frame', frame_with_triangles)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    swarm.parallel_safe(self.land)
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

