# FollowingRobotNeuralNetwork

Test run robot logic
> python neuralnetwork.py

compass.txt format
{Cardinal direction} {Number of moves to point north} {Direction: 1 - clockwise, 0 - counter clockwise}

rules.txt format
{Sensor 0 value} {Sensor 1 value} {Sensor 2 value} {Cardinal Direction}

The training utilizes random number generation for the script to keep trying different combinations until it is able to complete the different tables that drive the fuzzy logic. Not alot of learning is being done because the model is not too complex and dynamic to warrant a continuously changing neural network. However, adding more variables in determining the direction of the infrared light as well as generating the logic tables through "training" could motivate the need to have a dynamic neural network.