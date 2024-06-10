import threading
from astar import Astar
from Drone import Drone
from pathPlanning import PathPlanning
from flask import Flask, request, jsonify




gridSize = [8,8]
pathPlanning = PathPlanning()

host_name = "0.0.0.0"
port = 23336
app = Flask(__name__)

def maptogrid(x,y):
    return (x,y)
    return (int(x/8*100), int(y/8*100))

def gridtomap(x,y):
    return (x,y)
    return (int(x/100*8), int(y/100*8))

@app.route('/', methods = ['POST']) 
def index():
    drones = [Drone(i) for i in range(5)]
    pathplanning = PathPlanning()
    star = Astar()
    data = request.get_json()
    print(data)

    for drone in data:
        drones[drone['id']].setPosition(maptogrid(drone['x'], drone['y']))
    
    pathplanning = PathPlanning()
    targets = pathplanning.RotateCircleFormation(len(drones), 35, (50,50), 40)
    drones = star.calc_targets(drones, targets)
    json = []
    for index in range(len(drones)):
        path = star.findPath(drones[index].getPosition(), drones[index].getTarget())
        x, y = gridtomap(path[0], path[1])
        json.append({'id': index, "x" : x, "y" : y})
    print (json)
    return jsonify(json)


    
    

if __name__ == "__main__":
      threading.Thread(target=lambda: app.run(host=host_name, port=port, debug=True, use_reloader=False)).start()


    


