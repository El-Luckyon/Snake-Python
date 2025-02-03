from tkinter import *
import keyboard

# Constants
WINDOW_NAME = "Snake" 
WINOW_BACKGROUND_COLOR = "black"

SNAKE_COLOR = "green"
SNAKE_SIZE = 25
SNAKE_STARTING_SPEED = 0.01

KEYBIND_FORWARD = 'w'
KEYBIND_BACKWARD = 's'
KEYBIND_RIGHT = 'd'
KEYBIND_LEFT = 'a'

DEBUG = True

# Methods
def dLog(msg : any):
    if DEBUG:
        msg = str(msg)
        print(msg)
        
def cleanup():
    print("Program safely exited")
    
def createSnakeLabel(window):
    snakeFrame = Frame(window, background=SNAKE_COLOR)
    snakeFrame.config(width=SNAKE_SIZE, height=SNAKE_SIZE)
    snakeFrame.pack()    
    return snakeFrame    

# Classes
class GameObject:
    position = [SNAKE_SIZE / 2, SNAKE_SIZE / 2]
    facing = [1, 0]
    velocity = 0
    label : Label
    tracing = False
    traceAxis = 0
    traceGoal = 0
    traceProgress = 0
    target = None
    
    def __init__(self, label : Label):
        self.label = label
    
    def applyVelocity(self):
        facing = self.facing
        facingX = facing[0]
        if facingX != 0:
            self.position[0] += (self.velocity * facingX)
        else:
            self.position[1] += (self.velocity * facing[1])
        if self.tracing:
            self.traceProgress += self.velocity
    
    def draw(self):
        self.label.place(x=self.position[0], y=self.position[1], anchor=CENTER)
        
    def setVelocity(self, value : float):
        self.velocity = value
    
    def getVelocity(self):
        return self.velocity
    
    def setFacing(self, value : str):
        if value == "F":
            self.facing[0] = 0
            self.facing[1] = -1
        elif value == "B":
            self.facing[0] = 0
            self.facing[1] = 1
        elif value == "L":
            self.facing[0] = -1
            self.facing[1] = 0
        elif value == "R":
            self.facing[0] = 1
            self.facing[1] = 0
            
    def getFacing(self):
        facing = self.facing
        facingX = self.facing[0]
        facingY = self.facing[1]
        
        if facingY == -1:
            return "F"
        elif facingY == 1:
            return "B"
        elif facingX == 1:
            return "R"
        elif facingX == -1:
            return "L"

# Init
window = Tk()
window.configure(background=WINOW_BACKGROUND_COLOR)
window.title(WINDOW_NAME)

head = GameObject(createSnakeLabel(window))
head.label.config(bg="red")
head.setFacing("R")
head.setVelocity(SNAKE_STARTING_SPEED)
snakeParts = []
snakeParts.append(head)

# Polling Methods
def getPositon(facing, prevPos):
    pos = [0, 0]
    if facing == "F":
        pos = [prevPos[0], prevPos[1] + SNAKE_SIZE]
    elif facing == "B":
        pos = [prevPos[0], prevPos[1] - SNAKE_SIZE]
    elif facing == "R":
        pos = [prevPos[0] - SNAKE_SIZE, prevPos[1]]
    elif facing == "L":
        pos = [prevPos[0] + SNAKE_SIZE, prevPos[1]]
    return pos
    
def growSnake():
    newPart = GameObject(createSnakeLabel(window))
    lastPart = snakeParts[-1]
    facing = lastPart.getFacing()  
    newPart.position = getPositon(facing, lastPart.position)
    newPart.setFacing(facing)
    newPart.setVelocity(head.getVelocity())
    newPart.draw()
    snakeParts.append(newPart)

def startTraceChain(facing):
    size = len(snakeParts)
    if size == 1: return
    size -= 1
    part = snakeParts[size]
    part.traceGoal = SNAKE_SIZE
    if facing == "F" or facing == "B":
        part.traceAxis = 0
    elif facing == "R" or facing == "L":
        part.traceAxis = 1
    part.tracing = True
    
def processInput():        
    global wasGpressed
    
    if keyboard.is_pressed(KEYBIND_FORWARD) and head.getFacing() != "F":
        startTraceChain(head.facing)
        head.setFacing("F")
        dLog("FORWARD")
    elif keyboard.is_pressed(KEYBIND_BACKWARD) and head.getFacing() != "B":
        startTraceChain(head.facing)
        head.setFacing("B")
        dLog("BACKWARD")
    elif keyboard.is_pressed(KEYBIND_LEFT) and head.getFacing() != "L":
        startTraceChain(head.facing)
        head.setFacing("L")
        dLog("LEFT")
    elif keyboard.is_pressed(KEYBIND_RIGHT) and head.getFacing() != "R":
        startTraceChain(head.facing)
        head.setFacing("R")
        dLog("RIGHT")
        
    if keyboard.is_pressed('g') and not wasGpressed and DEBUG:
        growSnake()
        wasGpressed = True
        dLog("Snake Grown")
        
    if not keyboard.is_pressed('g'):
        wasGpressed = False
        
def updateSnake():
    for part in snakeParts:
        part.applyVelocity()
        part.draw()

        
while window.winfo_exists:
    try:
       processInput()
       updateSnake()
       window.update_idletasks()
       window.update()
    except:
       cleanup()
       break
    