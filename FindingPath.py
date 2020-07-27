import time
import pygame
from tkinter import *
from tkinter import messagebox
from collections import deque, namedtuple
from queue import PriorityQueue
import queue
from sys import argv
import math

fileInput = argv[1]
window = Tk()
window.title("Select algorithm")
def getType():
    global type
    type= int(typeBox.get())
    window.quit()
    window.destroy()
label = Label(window, text="""Select algorithm:
    1. Uniform cost search
    2. Breath first search
    3. A star search
    Enter your choice:
""",width = 19)
typeBox = Entry(window)
var = IntVar()
typeBox.grid(row=0, column=5, pady=3)
label.grid(row=0, pady=1)
submit = Button(window, text='Submit', command=getType)
submit.grid(columnspan=2, row=31)
window.update()
mainloop()

with open(fileInput,"r", encoding="utf8") as file:
    read = list(file)
    col = int(read[0].split(',')[0])+1
    row = int(read[0].split(',')[1])+1
    start =[]
    start.append(int(read[1].split(',')[0]))
    start.append(int(read[1].split(',')[1]))
    start = tuple(start)
    end = []
    end.append(int(read[1].split(',')[2]))
    end.append(int(read[1].split(',')[3]))
    end = tuple(end)
    list_pickup_point = []
    if (len(read[1].split(','))>4):
        list_pickup_point = read[1].split(',')[4:]
    n = len((list_pickup_point))/2
    n = int(n)
    for i in range(len(list_pickup_point)):
        list_pickup_point[i]=int(list_pickup_point[i])
    list_temp= []
    for i in range(n):
        list_temp.append(tuple([list_pickup_point[i*2],list_pickup_point[i*2+1]]))
    list_pickup_point= list_temp

    num_of_polygon = int(read[2])
    list_poly =[]
    list_poly = [0 for i in range(num_of_polygon)]
    for i in range(num_of_polygon):
        list_poly[i] = read[3+i].split(',')
        for j in range(len(list_poly[i])):
            list_poly[i][j] = int(list_poly[i][j])


t = 20 #edge of square pixel
pygame.init()
pygame.display.set_caption('Finding Path')
screen = pygame.display.set_mode((800,800))



class Point:
    def __init__(self,x,y):
        #obstacle's value = 1
        self.x=x
        self.y=y
        self.value =0
    def drawPoint(self,color):
        if (color == pygame.Color("red") or color == pygame.Color("gray")):
            self.value=1
        pygame.draw.rect(screen,color, ((self.x*t, self.y*t),(t-1,t-1)), 0)
        pygame.display.update()

#create grid
grid =[]
grid = [0 for i in range(col)]
for i in range(col):
    grid[i] = [0 for j in range(row)]
#draw edge and background
for i in range(col):
    for j in range(row):
        grid[i][j]=Point(i,j)
        grid[i][j].drawPoint(pygame.Color('white'))
for i in range(row):
    grid[0][i].drawPoint(pygame.Color('gray'))
    grid[col-1][i].drawPoint(pygame.Color('gray'))
for i in range(col):
    grid[i][0].drawPoint(pygame.Color('gray'))
    grid[i][row-1].drawPoint(pygame.Color('gray'))
#draw start_point and end_point:
    grid[start[0]][row -1 -start[1]].drawPoint(pygame.Color("green"))
    grid[end[0]][row -1 - end[1]].drawPoint(pygame.Color("green"))
    for i in range(len(list_pickup_point)):
        grid[list_pickup_point[i][0]][row -1 -list_pickup_point[i][1]].drawPoint(pygame.Color("yellow"))
#function drawline
def plotLineLow(x0,y0, x1,y1,grid):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy

    D = 2*dy - dx
    y = y0

    for x in range(x0,x1+1):
        grid[x][row-1-y].drawPoint(pygame.Color("red"))
        if D > 0:
            y = y + yi
            D = D - 2*dx
        D = D + 2*dy
def plotLineHigh(x0,y0, x1,y1,grid):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx

    D = 2*dx - dy
    x = x0

    for y in range(y0,y1+1):
        grid[x][row-1-y].drawPoint(pygame.Color("red"))
        if D > 0:
            x = x + xi
            D = D - 2*dy
        D = D + 2*dx
def plotLine(x0,y0, x1,y1,grid):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(x1, y1, x0, y0,grid)
        else:
            plotLineLow(x0, y0, x1, y1,grid)
    else:
        if y0 > y1:
            plotLineHigh(x1, y1, x0, y0,grid)
        else:
            plotLineHigh(x0, y0, x1, y1,grid)
#function draw polygon
def drawPolygon(listXY, grid):
    for i in range(0, len(listXY), 2):
        try:
            plotLine(listXY[i], listXY[i + 1], listXY[i + 2], listXY[i + 3], grid)
        except:
            #Draw final line
            plotLine(listXY[i], listXY[i + 1], listXY[0], listXY[1], grid)

for i in range(num_of_polygon):
    drawPolygon(list_poly[i],grid)
#creat list obstacle
listObs =[]
for i in range(col):
    for j in range(row):
        if (grid[i][j].value == 1):
            listObs.append((i,row -1 -j))
#function draw path
def drawPath(path,grid):
    for point in path[-2:0:-1]:
        grid[point[0]][row -1 - point[1]].drawPoint(pygame.Color("blue"))
        time.sleep(0.1)
    return len(path[-2:0:-1])




def drawPathWithPickupPoint(graph,start,end,listPickupPoint,grid):
    cost = 0
    cost += len(listPickupPoint)
    if (len(listPickupPoint)!=0):
        cost += drawPath(graph(start, listPickupPoint[0]), grid)
        if (len(listPickupPoint) > 1):
            for i in range(len(listPickupPoint) - 1):
                cost += drawPath(graph(listPickupPoint[i], listPickupPoint[i + 1]), grid)
        cost += drawPath(graph(listPickupPoint[-1], end), grid)
    else:
        cost += drawPath(graph(start, end), grid)

    return cost

class Graph:
    def __init__(self, barriers, width, height):
        self.barriers = []
        self.barriers = barriers.copy()
        self.height = height
        self.width = width
        self.cost_map = height*width

    #Tìm tọa độ xung quanh tọa độ đang xét
    def get_vertex_neighbours(self, pos):
        n = []
        #Moves allow link a chess king
        #[(1,0),(-1,0),(0,1),(0,-1)]
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 <= 0 or x2 >= self.width or y2 <= 0 or y2 >= self.height:
                continue
            n.append((x2, y2))
        return n
    
    #xét điểm hiện tại có phải là vật cản hay không
    def move_cost(self, b):
        for barrier in self.barriers:
            if b == barrier:
                return math.inf #Extremely high cost to enter barrier squares
        return 1 #Normal movement cost


    def uniform_cost_search(self, start, goal):

        frontier = MyPriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        #kiểm tra data start và goal
        if goal in self.barriers or goal[0] < 0 or goal[0] > self.width or goal[1] < 0 or goal[1] > self.height:
            print("Wrong value goal!")
            return
        elif start in self.barriers or start[0] < 0 or start[0] > self.width or start[1] < 0 or start[1] > self.height:
            print("wrong value start!")
            return

        while not frontier.empty():

            current = frontier.get()

            if current == goal or cost_so_far[current] > self.cost_map:
                break

            for next in self.get_vertex_neighbours(current):
                new_cost = cost_so_far[current] + self.move_cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put(next, priority)
                    came_from[next] = current
                    
        path =[]
        
        if(current != goal):
            return 0
            
        End = goal
        Begind = start
        while Begind != End:
            path.append(End)
            End = came_from.get(End)

        path.append(Begind)
        return path

from queue import PriorityQueue

class MyPriorityQueue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

class AStarGraph(object):
    #Define a class board like grid with two barriers
 
    def __init__(self, barriers, width, height):
        self.barriers = []
        self.barriers = barriers.copy()
        self.height = height
        self.width = width
        self.cost_map = height*width
    
    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
 
    def get_vertex_neighbours(self, pos):
        n = []
        #Moves allow link a chess king
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 <= 0 or x2 >= self.width or y2 <= 0 or y2 >= self.height:
                continue
            n.append((x2, y2))
        return n
 
    def move_cost(self, b):
        for barrier in self.barriers:
            if b == barrier:
                return math.inf #Extremely high cost to enter barrier squares
        return 1 #Normal movement cost
    
        
    def AStarSearch(self, start, goal):
 
        frontier = MyPriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        if goal in self.barriers or goal[0] < 0 or goal[0] > self.width or goal[1] < 0 or goal[1] > self.height:
            print("Wrong value goal!")
            return
        elif start in self.barriers or start[0] < 0 or start[0] > self.width or start[1] < 0 or start[1] > self.height:
            print("wrong value start!")
            return
        
        while not frontier.empty():

            current = frontier.get()

            if current == goal or cost_so_far[current] > self.cost_map:
                break

            for next in self.get_vertex_neighbours(current):
                new_cost = cost_so_far[current] + self.move_cost(next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
        
        path =[]
        
        if(current != goal):
            return 0
            
        End = goal
        Begind = start
        while Begind != End:
            path.append(End)
            End = came_from.get(End)

        path.append(Begind)
        return path


class BreathFirstGraph:
    def __init__(self, barriers, width, height):
        self.barriers = []
        self.barriers = barriers.copy()
        self.height = height
        self.width = width
        self.cost_map = height*width

    def move_cost(self, b):
        if b in self.barriers:
            return 1
        return 0

    def vertices_neighbours(self, pos):
        n = []
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            if x2 <= 0 or x2 >= self.width or y2 <= 0 or y2 >= self.height:
                continue
            n.append((x2, y2))
        return n

    def BreathFirstSearch(self, start, goal):
        frontier = queue.Queue(maxsize = self.width ** self.height)
        frontier.put(start)
        came_from = {}
        came_from[start] = None

        if goal in self.barriers or goal[0] < 0 or goal[0] > self.width or goal[1] < 0 or goal[1] > self.height:
            print("Wrong value goal!")
            return
        elif start in self.barriers or start[0] < 0 or start[0] > self.width or start[1] < 0 or start[1] > self.height:
            print("wrong value start!")
            return

        while not frontier.empty():
            current = frontier.get()
            
            if current == goal:
                break

            for next in self.vertices_neighbours(current):
                if next not in came_from and self.move_cost(next) != 1:
                    frontier.put(next)
                    came_from[next] = current

        path =[]
        
        if(current != goal):
            return 0
            
        End = goal
        Begind = start
        while Begind != End:
            path.append(End)
            End = came_from.get(End)

        path.append(Begind)
        return path

cost = 0
typeName = 0
if (type == 1):
    typeName = "Uniform Cost Search"
    graph = Graph((listObs), col, row)
    cost = drawPathWithPickupPoint(graph.uniform_cost_search, start, end, list_pickup_point, grid)
elif (type == 2):
    typeName = "Breath First Search"
    graph = BreathFirstGraph((listObs), col, row)
    cost = drawPathWithPickupPoint(graph.BreathFirstSearch, start, end, list_pickup_point, grid)
elif (type == 3):
    typeName = "A Star search"
    graph = AStarGraph((listObs), col, row)
    cost = drawPathWithPickupPoint(graph.AStarSearch, start, end, list_pickup_point, grid)
else:
    print("Your input's wrong!")

Tk().wm_withdraw()
messagebox.askokcancel('Algorithm '+typeName, ('The program finished, the shortest distance \n to the path is ' + str(cost) + ' blocks away.'))



