# Pseudo train mapping logic

from mapping import MappingControl
from random import randrange

if __name__ == "__main__":
    control = MappingControl()

    control.init()

    for i in range(20000):
        index = randrange(0,8)
        sensor0 = randrange(0,5)
        sensor1 = randrange(0,5)
        sensor2 = randrange(0,5)

        if f'{sensor0}_{sensor1}_{sensor2}' not in control.data:
            control.data[f'{sensor0}_{sensor1}_{sensor2}'] = [-1, -1, -1, -1, -1, -1, -1, -1]
    
        direction = control.map[index]
        result = control.simulate_mapping(sensor0, sensor1, sensor2, direction)
        control.data[f'{sensor0}_{sensor1}_{sensor2}'][index] = result

    sorted_data = sorted(control.data)
    final_data = {}
    for key in sorted_data:
        for i in range(7):
            if control.data[key][i] == 1:
                final_data[key]= control.map[i]
        
        if key not in final_data:
            final_data[key]= "C"

    control.update_mapping(final_data)