# baldwinization

This code exists to simulate neural-network controlled robots in Pybullet to study the effects of lifetime learning on genetic algorithms.

##How To Run This Code

All metavariables relevant to the evolutionary algorithms and robot parameters are stored in experiment_parameters.py. The main loop is run from search.py, which sources instances of individuals from controller.py. Error logs are written to a local file named <run seed>.txt

Before any code is run, check experiment_parameters to ensure proper setup, and run generate.py to ensure morphology reference files have been properly created. Search should create all necessary folders for data storage but as the repository is initially created for individual research it is not fully tested.
  
  ##File Hierarchy
  
  Search is the main file, and the only script that needs to be run by the user. It will create instances
