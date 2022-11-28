from pyrosim import pyrosim
import os

from snake import SNAKE
from quad import QUAD
from hex import HEX
import experiment_parameters as ep

def create_world():
    pyrosim.Start_SDF("bodyfiles/world.sdf")
    pyrosim.End()

def create_bodies():
    snake = SNAKE()
    snake.make_body()
    quad = QUAD()
    quad.make_body()
    hex = HEX()
    hex.make_body()

if not os.path.exists("./bodyfiles"):
    os.mkdir("bodyfiles")
if not os.path.exists("./nnfiles"):
    os.mkdir("nnfiles")
create_world()
create_bodies()
