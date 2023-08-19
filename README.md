# baldwinization

This code exists to simulate neural-network controlled robots in Pybullet to study the effects of lifetime learning on genetic algorithms.

## Dependencies

This code makes use of the following libraries:

matplotlib

numpy

pickle

pybullet

scikits

## How To Run This Code

All metavariables relevant to the evolutionary algorithms and robot parameters are stored in experiment_parameters.py. The main loop is run from search.py, which sources instances of individuals from controller.py. Error logs are written to a local file named <run seed>.txt. To run search.py, two console-level arguments must be given, the morphology of the robots being simulated and the random seed to use for the run. Currently supported morphologies are Snake, Quad, and Hex. For more on this, see subheader "creating new morphologies".

Before any code is run, check experiment_parameters to ensure proper setup, and run generate.py to ensure morphology reference files have been properly created. Search should create all necessary folders for data storage but as the repository is initially created for individual research this is not fully tested and some file IO errors may arise in preliminary runs.
  
## File Hierarchy
  
Search is the main file, and the only script that needs to be run by the user. It will create instances of Controller objects and simulate them using Controller's class functions. Those functions create individual instances of simulation, which in turn calls simulate, which runs robot.py. Robot.py draws parameters from the files created by Controller's methods, and the files it creates are read back into its parent Controller after simulation completes.
  
Robot parameters are all handled by the pyrosim library of files, forked from https://github.com/jbongard/pyrosim. Alterations to streamline neural network processing, create hidden neuron layers, and allow for synaptic development and tracking have been made to the neuralnetwork, synapse, and neuron files.
  
## Creating New Morphologies

Each morphology has its own class file, which is a subclass of the builder class template. These are responsible for creating a body file and brain file for simulation. To add a new type of robot, the following files need to be altered or created:
  
  - A new .py file containing the new morph's class and builder functions
  - Lines to build the body file need to be appended to generate.py
  - Cases for this new robot type need to be added to the constructor of controller.py
  - The name for this new robot type should be added to the robot_types list in experiment_parameters.py

## Altering Learning Rules

Learning rule parameters are stored in Controller objects and passed as arguments when the robot is simulated. The code dictating how they operate on individual synapses is located in synapse.py within the pyrosim folder. Changing how robots learn will require altering the main loop, which updates learning parameters, controller.py, which stores them, and synapse.py, which uses them.
