from scipy.optimize import linear_sum_assignment
import numpy as np
from Drone import Drone

class Astar:
    def findPath(self, start, end):
        result = self.aStarSearch(start, end, 0)
        
        for i in range(3):
            for j in range(3):
                self.grid[result[0]+1-i][result[1]+1-j] = 1


        return result

    def calc_targets(self, drones, targets):
        
        self.grid = [[0 for j in range(100)] for i in range(100)]
        weights = []
        location = []

        for drone in drones:

                    self.grid[drone.getPosition()[0]][drone.getPosition()[1]] = 1

        
        if len(targets) == 0:   
            return
        for index in range(len(drones)):
            temp1 = []
            temp2 = []
            for target in targets:
                xdist = abs(drones[index].getPosition()[0] - target[0])
                ydist = abs(drones[index].getPosition()[1] - target[1])
                dist = xdist + ydist + 1
                temp1.append(dist)
                temp2.append(target)
            weights.append(temp1)
            location.append(temp2)
                
        
        row_ind, col_ind = linear_sum_assignment(weights)
     
        for i in range(len(row_ind)):
            drones[i].setTarget(location[row_ind[i]][col_ind[i]])
        
        return drones
            
        

    def isvalid(self,cell):
        if cell[0] >= 0 and cell[0] < len(self.grid):
            if cell[1] >= 0 and cell[1] < len(self.grid[0]):
                return True
        return False
    
    def unblocked(self,cell):
        if self.grid[cell[0]][cell[1]] == 1:
            return False
        return True

    def isDestination(self, cell, end):
        if cell[0] == end[0] and cell[1] == end[1]:
            return True
        return False
    
    def calculateHValue(self,cell, end):
        return abs(cell[0] - end[0]) + abs(cell[1] - end[1])
    
    def tracePath(self,cellDetails, end, dist ):

        row = end[0]
        col = end[1]

        Path = []
        while not (cellDetails[row][col]["parent_i"] == row and cellDetails[row][col]["parent_j"] == col):
            Path.append([row, col])
            temp_row = cellDetails[row][col]["parent_i"]
            temp_col = cellDetails[row][col]["parent_j"]
            row = temp_row
            col = temp_col

        Path.append([row, col])
        Path.reverse()
        if dist ==1:
            return len(Path)
        return Path[1]
    
    def aStarSearch(self,start , end, dist = 0):
        start = (start[0], start[1])
        end = (end[0], end[1])
                
        if not self.isvalid(start):
         
            if dist == 1:
                return 1000
            return start
        
        if not self.isvalid(end):
        
            if dist == 1:
                return 1000
            return start
        
        if not self.unblocked(end ):
            
            if dist == 1:
                return 1000
            return start
        
        if start == end:
         
            if dist == 1:
                return 0
            
            return start
        
        # Initialize the closed list
        closedList = [[False for i in range(len(self.grid[0]))] for j in range(len(self.grid))]

        cellDetails = [[{} for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                cellDetails[i][j]["f"] = float('inf')
                cellDetails[i][j]["g"] = float('inf')
                cellDetails[i][j]["h"] = float('inf')
                cellDetails[i][j]["parent_i"] = -1
                cellDetails[i][j]["parent_j"] = -1

        i = int(start[0])
        j = int(start[1])
        cellDetails[i][j]["f"] = 0.0
        cellDetails[i][j]["g"] = 0.0
        cellDetails[i][j]["h"] = 0.0
        cellDetails[i][j]["parent_i"] = i
        cellDetails[i][j]["parent_j"] = j

        openList = [[0.0, i, j]]

        foundDest = False

        while len(openList) > 0:
            p = openList.pop(0)
            i = p[1]
            j = p[2]
            closedList[i][j] = True

            sNew = [[-1, 0], [0, -1], [1, 0], [0, 1]]
            for k in range(len(sNew)):
                iNew = i + sNew[k][0]
                jNew = j + sNew[k][1]
                if self.isvalid([iNew, jNew]):
                    
                    if self.isDestination([iNew, jNew], end):
                        cellDetails[iNew][jNew]["parent_i"] = i
                        cellDetails[iNew][jNew]["parent_j"] = j
                   
                        foundDest = True
                        
                        return self.tracePath(cellDetails, end, dist)
                    
                    elif closedList[iNew][jNew] == False and self.unblocked([iNew, jNew]):
                        
                        gNew = cellDetails[i][j]["g"] + 1.0
                        hNew = self.calculateHValue([iNew, jNew], end)
                        fNew = gNew + hNew
                        if cellDetails[iNew][jNew]["f"] == float('inf') or cellDetails[iNew][jNew]["f"] > fNew:
                            openList.append([fNew, iNew, jNew])
                            cellDetails[iNew][jNew]["f"] = fNew
                            cellDetails[iNew][jNew]["g"] = gNew
                            cellDetails[iNew][jNew]["h"] = hNew
                            cellDetails[iNew][jNew]["parent_i"] = i
                            cellDetails[iNew][jNew]["parent_j"] = j

        if foundDest == False:
            print("Failed to find the destination cell")
        return start
    

if __name__ == '__main__':
    astar = Astar()
    drones = [Drone("red"), Drone("green"), Drone("blue")]
    drones[0].setPosition((50,50))
    drones[1].setPosition((25,21))
    drones[2].setPosition((75,75))
    targets = [(28,12), (56,23), (87,32)]
    drones = astar.calc_targets(drones, targets)
    for drone in drones:
        print(drone.target)