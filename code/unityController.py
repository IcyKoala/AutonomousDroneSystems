import threading
from astar import Astar
from coolerDrone import Drone
from pathPlanning import PathPlanning
from flask import Flask, request
from json import JSONDecoder
import coolerDrone



flag = threading.Event()

flag.clear()

controller = coolerDrone.DroneController()

gridSize = [8,8]
pathPlanning = PathPlanning()

host_name = "145.24.238.156"
port = 8080
app = Flask(__name__)

def maptogrid(x,y):
    #return (x,y)
    return (int(x/8*100), int(y/8*100))

def gridtomap(x,y):
    #return (x,y)
    return ((x/100*8), (y/100*8))

#create 2 functions that map a 1080x1080 grid to a 100x100 grid
#and vice versa
def cameraToGrid(x,y):
    return (int(x/1080*100), int(y/1080*100))

def gridToCamera(x,y):
    return (int(x/100*1000), int(y/100*600))

def dronesToLocAndDone(green, red):
    controller.dronesToLoc(green, red)
    flag.clear()
            

@app.route('/', methods = ['POST']) 
def index():
  
    if flag.is_set():

        return "busy"
    flag.set()

    
    
    drones = [Drone(i) for i in range(5)]
    pathplanning = PathPlanning()
    star = Astar()
    data = request.get_json()

    for drone in data:
        drones[drone['droneID']].setPosition(maptogrid(drone['x'], drone['z']))
    
    pathplanning = PathPlanning()
    targets = pathplanning.RotateCircleFormation(len(drones), 30, (50,50), 180)
    drones = star.calc_targets(drones, targets)

    greentarget = gridToCamera(drones[0].getTarget()[0], drones[0].getTarget()[1])
    redtarget = gridToCamera(drones[1].getTarget()[0], drones[1].getTarget()[1])
    threading.Thread(target=dronesToLocAndDone, args=(greentarget, redtarget)).start()
    print("test")

    json = []
    for index in range(len(drones)):
        path = star.findPath(drones[index].getPosition(), drones[index].getTarget())
        x, y = gridtomap(drones[index].getTarget()[0], drones[index].getTarget()[1])
        json.append({'droneID': index, "x" : x, "z" : y , "y": 0.2})
 
    return json


    
    

if __name__ == "__main__":
    app.run(host=host_name, port=port, debug=True, use_reloader=False)
      #threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()


    


