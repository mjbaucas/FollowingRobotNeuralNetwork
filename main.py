# Testing space for logic

from mapping import MappingControl
from fuzzylogic import Environment

if __name__ == "__main__":
    environment = Environment()
    mapping_control = MappingControl()
    
    file = open('data.csv', 'r')
    
    temp_dict = {}
    sensor0_list = []
    sensor1_list = []
    sensor2_list = []
    counter = 0
    for line in file:
        temp_list = line.split(',')
        temp_dict[counter] = [int(temp_list[0]), int(temp_list[1]), int(temp_list[2]), int(temp_list[3]), int(temp_list[4]), int(temp_list[5][:-1])]
        
        if counter < 7:
            sensor0_list.append(int(temp_list[0]))
            sensor1_list.append(int(temp_list[1]))
            sensor2_list.append(int(temp_list[2]))
            
        counter += 1         
   
    environment.init(sensor0_list, sensor1_list, sensor2_list)
    mapping_control.init()
    mapping_control.train_mapping(temp_dict, environment)
    print(mapping_control.motor_left)