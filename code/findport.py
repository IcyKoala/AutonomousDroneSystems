import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie


manualMovementDistance = 0.1
redURI = 'radio://0/80/2M/E7E7E7E7E7'
p1 = "radio://0/"
p2 = "/2M/E7E7E7E7E7"
cflib.crtp.init_drivers(enable_debug_driver=False)
test = []

for i in range (125):
    try:
        with SyncCrazyflie(p1 + str(i) + p2) as scf:
            print("connected")
            test +=[i]
            break

    except:
        pass

print(test)