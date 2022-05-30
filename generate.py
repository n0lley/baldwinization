import pyrosim
from snake import SNAKE
from quad import QUAD
from hex import HEX

def create_world():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.End()

def create_bodies():
    snake = SNAKE()
    snake.make_body()
    quad = QUAD()
    quad.make_body()
    hex = HEX()
    hex.make_body()

create_world()
