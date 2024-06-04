import math
import numpy as np

droneDir = [1,0]
dronePos = [0,2]
targetPos = [-1, 2]

# targetDir = np.subtract(targetPos, dronePos)
# value = droneDir @ targetDir
# res = math.degrees (math.acos (value))
# print(res)

targetRad = math.atan2(targetPos[1]-dronePos[1], targetPos[0]-dronePos[0])
targetAngle = math.degrees (targetRad)
print(targetAngle)

droneRad = math.atan2(droneDir[1], droneDir[0])
droneAngle = math.degrees (droneRad)
print(droneAngle)
change = targetAngle-droneAngle
if abs(change) > 180: 
    change += 360
print(change)
