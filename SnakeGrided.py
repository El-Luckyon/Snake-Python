import tkinter as tk
import keyboard
from time import time

#Constants
FORWARD_KEY = "w"
BACKWARD_KEY = "s"
RIGHT_KEY = "d"
LEFT_KEY = "a"

SNAKE_HEAD_COLOR = "red"
SNAKE_BODY_COLOR = "gold"
FOOD_COLOR = "green"
BG_COLOR = "black"

DEFAULT_SNAKE_UPDATE_INTERVAL = 0.5

NUM_GRID_X = 50
NUM_GRID_Y = 28

#Runtime Variables
gridSizeX : int
gridSizeY : int
window : tk.Tk
lastKey = RIGHT_KEY
progress : float = 0
snakeUpdateInterval = DEFAULT_SNAKE_UPDATE_INTERVAL

#Classes
class GridCoordinate:
    x  : int= 0
    y : int = 0
    facingX : int
    facingY : int
    window : tk.Tk
    
    def __init__(self, window : tk.Tk, pos : tuple[int , int], facing : tuple[int, int]):
        self.window = window
        self.x = pos[0]
        self.y = pos[1]
        self.facingX = facing[0]
        self.facingY = facing[1]
        
    def setFacing(self, facing : tuple[int, int]):
        self.facingX = facing[0]
        self.facingY = facing[1]
        
    def getPos(self):
        return self.x, self.y
        
    def setPos(self, pos : tuple[int , int]):
        self.x = pos[0]
        self.y = pos[1]
    
    def getFacing(self):
        return self.facingX, self.facingY
    
    def convertToPx(self):
        window = self.window
        return self.x * gridSizeX, self.y * gridSizeY

    def destroy(self):
        del self

    
class GameObject:
    position : GridCoordinate
    frame : tk.Frame
    window : tk.Tk
    
    def __init__(self, window : tk.Tk):
        self.window = window
        frame = tk.Frame(window, width=10, height=10)
        frame.pack()
        self.frame = frame
        self.position = GridCoordinate(window, (-1, 0), (0, 0))
        
    def setColor(self, color : str):
        self.frame.config(bg=color)
    
    def draw(self):
        x, y = self.position.convertToPx()
        frame = self.frame
        frame.place(x=x, y=y, anchor="nw")
        frame.config(width=gridSizeX, height=gridSizeY)        
    
    def destroy(self):
        self.frame.destroy()
        self.position.destroy()
        del self

snakeParts : list[GameObject] = []

#Methods
def calculateGridSize():
    global gridSizeX, gridSizeY
    gridSizeX = window.winfo_width() / NUM_GRID_X
    gridSizeY = window.winfo_height() / NUM_GRID_Y
    
def createSnakePart(color : str):
    global window
    global snakeParts
    part = GameObject(window)
    part.setColor(color)
    snakeParts.append(part)
    return part
    
def updateSnake(deltaTime : float):
    global snakeParts
    global progress
    global window
    
    progress += deltaTime
    if progress > snakeUpdateInterval:
        head = snakeParts[0]
        positionToFill = GridCoordinate(window, head.position.getPos(), head.position.getFacing())
        head.position.x += head.position.facingX
        head.position.y += head.position.facingY
        head.draw()
        for i in range(1, len(snakeParts)):
            part = snakeParts[i]
            temp = GridCoordinate(window, part.position.getPos(), part.position.getFacing())
            part.position.setPos(positionToFill.getPos())
            part.position.setFacing(positionToFill.getFacing())
            positionToFill.setPos(temp.getPos())
            positionToFill.setFacing(temp.getFacing())
            temp.destroy()
            part.draw()
        positionToFill.destroy()
        progress = 0

def growSnake():
    global snakeParts
    newPart = createSnakePart(SNAKE_BODY_COLOR)
    lastPart = snakeParts[-1]
    facingX = lastPart.position.facingX
    facingY = lastPart.position.facingY
    if facingX != 0:
        newPart.position.x = lastPart.position.x - facingX
    else:
        newPart.position.y = lastPart.position.y - facingY
    newPart.draw()
    
def processInput(head : GameObject):
    global lastKey
    if keyboard.is_pressed(FORWARD_KEY) and lastKey != FORWARD_KEY:
        head.position.setFacing((0, -1))
        lastKey = FORWARD_KEY
    elif keyboard.is_pressed(BACKWARD_KEY) and lastKey != BACKWARD_KEY:
        head.position.setFacing((0, 1))
        lastKey = BACKWARD_KEY
    elif keyboard.is_pressed(RIGHT_KEY) and lastKey != RIGHT_KEY:
        head.position.setFacing((1, 0))
        lastKey = RIGHT_KEY
    elif keyboard.is_pressed(LEFT_KEY) and lastKey != LEFT_KEY:
        head.position.setFacing((-1, 0))
        lastKey = LEFT_KEY
    elif keyboard.is_pressed('g') and lastKey != 'g':
        lastKey = 'g'
        growSnake()
        
#Init
window = tk.Tk()
window.config(bg=BG_COLOR)

head = createSnakePart(SNAKE_HEAD_COLOR)
head.position.facingX = 1
head.position.facingY = 0

deltaTime = 0

#Main-Loop
while True:
    # t0 = time()
    # processInput(head)
    # calculateGridSize()
    # updateSnake(deltaTime)
    # window.update_idletasks()
    # window.update()
    # t1 = time()
    # deltaTime = t1 - t0
    try:
        t0 = time()
        processInput(head)
        calculateGridSize()
        updateSnake(deltaTime)
        window.update_idletasks()
        window.update()
        t1 = time()
        deltaTime = t1 - t0
    except Exception as e:
        print(e)
        break
    
#Cleanup
print("Program exited successfully")