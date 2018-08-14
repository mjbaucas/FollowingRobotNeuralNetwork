#Simulates the behaviour of the robot and how it translates sensor values to directions

class MappingControl:
    def init(self):
        self.motor_pair = {}
    
    def train_mapping(self, data, environment):
        for key, value in data.items():
            environment.evaluate_sensors(value[0], value[1], value[2])
            control_key = f'{environment.digital[0]}_{environment.digital[1]}_{environment.digital[2]}'

            if control_key not in self.motor_pair:
                self.motor_pair[control_key] = [[0] * 19 for i in range(19)]
            
            delta_signal = [0, 0, 0]
            delta_signal[0] = value[5] - value[0]
            delta_signal[1] = value[6] - value[1]
            delta_signal[2] = value[7] - value[2]

            left_sensor = 0
            right_sensor = 0
            front_sensor = 0
            if delta_signal[2] > 0 and delta_signal[2] > environment.baseline[2]:
                left_sensor = 1

            if delta_signal[1] > 0 and delta_signal[1] > environment.baseline[1]:
                right_sensor = 1

            if delta_signal[0] > 0: 
                front_sensor = 1
            if delta_signal[0] > environment.baseline[0]:
                front_sensor = 2
                
            if right_sensor == 1 or left_sensor == 1:
                self.motor_pair[control_key][value[3]+9][value[4]+9] -= 1
            
            if front_sensor > 0:
                self.motor_pair[control_key][value[3]+9][value[4]+9] += front_sensor
            else:
                self.motor_pair[control_key][value[3]+9][value[4]+9] -= 1
            
        # Post-data sort
        sorted_data = sorted(self.motor_pair)
        final_data = {}
        for key in sorted_data:
            final_data[key]= self.motor_pair[key]
        self.motor_pair = final_data
    
    def update_tables(self):
        data_table = {}
        for key, value in self.motor_pair.items():
            max_val = 0
            pair_list = []
            for x in range(0, 19):
                for y in range(0, 19):
                    if value[x][y] > max_val:
                        max_val = value[x][y]
                        pair_list = [f'{x}_{y}']
                    elif value[x][y] == max_val and max_val > 0:
                        pair_list.append(f'{x}_{y}')
            data_table[key] = pair_list
        
        print(data_table)

    def display_data(self):
        for key, value in self.motor_pair.items():
            for x in range(0, 19):
                print(f'{key}[{x-9}]: {value[x]}')