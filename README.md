# FollowingRobotNeuralNetwork

Test run robot logic
> python neuralnetwork.py

compass.txt format
> 1 2 3
> 1. Cardinal direction 
> 2. Number of moves to point north 
> 3. Direction: 1 - clockwise, 0 - counter clockwise

rules.txt format
> 1 2 3 4
> 1. Sensor 0 value 
> 2. Sensor 1 value
> 3. Sensor 2 value
> 4. Cardinal Direction

The training utilizes random number generation for the script to keep trying different combinations until it is able to complete the different tables that drive the fuzzy logic. Not alot of learning is being done because the model is not complex and dynamic enough to warrant a continuously changing neural network. However, adding more variables in determining the direction of the infrared light as well as generating the logic tables through "training" could motivate the need to have a dynamic neural network.