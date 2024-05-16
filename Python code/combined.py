"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

import cv2 as cv
from cv2 import aruco
import numpy as np
import asyncio


URI = 'radio://0/80/2M/E7E7E7E7E7'
cflib.crtp.init_drivers(enable_debug_driver=False)

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

target = {"x"  : 60, "y" : 14}
x = 0
y = 0

flightHeight = 0.5

targetX = 0
inaccuracy = 1
droneX = 10

# load in the calibration data
calib_data_path = "C:/Users/yario/Downloads/OpenCV-main/Distance Estimation/calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 6  # centimeters (measure your printed marker size)

marker_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL) #DICT_5X5_250

param_markers = aruco.DetectorParameters()

cap = cv.VideoCapture(0)

async def camCheck():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        marker_corners, marker_IDs, reject = aruco.detectMarkers(
            gray_frame, marker_dict, parameters=param_markers
        )
        if marker_corners:
            rVec, tVec, _ = aruco.estimatePoseSingleMarkers(
                marker_corners, MARKER_SIZE, cam_mat, dist_coef
            )
            total_markers = range(0, marker_IDs.size)
            for ids, corners, i in zip(marker_IDs, marker_corners, total_markers):
                cv.polylines(
                    frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
                )
                corners = corners.reshape(4, 2)
                corners = corners.astype(int)
                top_right = corners[0].ravel()
                top_left = corners[1].ravel()
                bottom_right = corners[2].ravel()
                bottom_left = corners[3].ravel()

                # Calculating the distance
                distance = np.sqrt(
                    tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
                )
                #print(distance)
                # Draw the pose of the marker
                point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i], 4, 4)
                cv.putText(
                    frame,
                    f"id: {ids[0]} Dist: {round(distance, 2)}",
                    top_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.3,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                cv.putText(
                    frame,
                    f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ",
                    bottom_right,
                    cv.FONT_HERSHEY_PLAIN,
                    1.0,
                    (0, 0, 255),
                    2,
                    cv.LINE_AA,
                )
                x = round(tVec[i][0][0],1)
                y = round(tVec[i][0][1],1)
                print(f"x:{round(tVec[i][0][0],1)} y: {round(tVec[i][0][1],1)} ")
        cv.imshow("frame", frame)

        if x > 0:
            mc.back(0.1)
        else:
            mc.forward(0.1)

        # if y > 0:
        #     mc.right(0.1)
        # else:
        #     mc.left(0.1)

        key = cv.waitKey(1)
        if key == ord("q"):
            mc.down(1.6)
            mc.land
            break
        cap.release()
        cv.destroyAllWindows()

async def droneControl():
    with SyncCrazyflie(URI) as scf:
        with MotionCommander(scf, 1.7) as mc:
            



#target 1 60 14, -35 -14
            
            
                