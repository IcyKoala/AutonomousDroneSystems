import threading
from astar import Astar
from Drone import Drone
from pathPlanning import PathPlanning
from flask import Flask, request
from json import JSONDecoder



gridSize = [8,8]
pathPlanning = PathPlanning()

host_name = "145.137.1.94"
port = 8080
app = Flask(__name__)

def maptogrid(x,y):
    #return (x,y)
    return (int(x/8*100), int(y/8*100))

def gridtomap(x,y):
    #return (x,y)
    return ((x/100*8), (y/100*8))

@app.route('/', methods = ['POST']) 
def index():
    
    
    drones = [Drone(i) for i in range(5)]
    pathplanning = PathPlanning()
    star = Astar()
    data = request.get_json()
   
   

    for drone in data:
        drones[drone['droneID']].setPosition(maptogrid(drone['x'], drone['z']))
    
    pathplanning = PathPlanning()
    targets = pathplanning.RotateCircleFormation(len(drones), 35, (50,50), 40)
    drones = star.calc_targets(drones, targets)
    json = []
    for index in range(len(drones)):
        path = star.findPath(drones[index].getPosition(), drones[index].getTarget())
        x, y = gridtomap(path[0], path[1])
        json.append({'droneID': index, "x" : x, "z" : y , "y": 1})
    
    return json


    
    

if __name__ == "__main__":
      threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()


    


