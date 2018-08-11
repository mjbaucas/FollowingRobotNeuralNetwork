# FollowingRobotNeuralNetwork

Test run robot logic
> python main.py

The training utilizes data from the actual robot for the script to interpret. This data is used by the srcipt to complete a decision table. The decision table contains all of the discovered sensor states based on the provided sensor data that has been transalted by the designed fuzzy logic. This fuzzy logic takes in the analog values from the sensors compares it with the sensor values. The sensors are then ranked based on each comparison. This creates the sensor states. Each state will contain a list of all the possible voltage outputs that the robot can do to maximize the main infrared sensor. The list is updated to show which of the combinations are most successful for the robot to lookup. 