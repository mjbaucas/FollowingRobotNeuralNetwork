# Testing space for logic

from mapping import MappingControl
from fuzzylogic import Environment

if __name__ == "__main__":
    environment = Environment()
    mapping_control = MappingControl()
    
    datafile = open('data.csv', 'r', encoding="utf-8-sig")
    
    temp_dict = {}
    sensor0_list = []
    sensor1_list = []
    sensor2_list = []
    counter = 0
    for line in datafile:
        temp_list = line.split(',')
        if len(temp_list) == 8:
            temp_dict[counter] = [int(temp_list[0]), int(temp_list[1]), int(temp_list[2]), int(temp_list[3]), int(temp_list[4]), int(temp_list[5]), int(temp_list[6]), int(temp_list[7][:-1])]
            
            if counter < 7:
                sensor0_list.append(int(temp_list[0]))
                sensor1_list.append(int(temp_list[1]))
                sensor2_list.append(int(temp_list[2]))
                
            counter += 1         
    
    environment.init(sensor0_list, sensor1_list, sensor2_list)
    mapping_control.init()
    mapping_control.train_mapping(temp_dict, environment)
    mapping_control.update_tables()