import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from camera import CameraDetector
import math
import cv2
import time
import threading

manualMovementDistance = 0.1
redURI = 'radio://0/80/2M/E7E7E7E7E7'
p1 = "radio://0/"
p2 = "/2M/E7E7E7E7E7"
cflib.crtp.init_drivers(enable_debug_driver=False)

for i in range (100):
    if i == 80:
        continue
    try:
        with SyncCrazyflie(p1 + str(i) + p2) as scf:
            print(i)
            break

    except:
        pass