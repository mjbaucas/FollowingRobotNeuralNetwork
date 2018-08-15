#Simulates the behaviour of the robot and how it translates sensor values to directions

class MappingControl:
    def init(self):
        self.motor_pair = {}
    
    def train_mapping(self, data, environment):
        for key, value in data.items():
            environment.evaluate_sensors(value[0], value[1], value[2])
            control_key = f'{environment.digital[0]},{environment.digital[1]},{environment.digital[2]}'

            if control_key not in self.motor_pair:
                self.motor_pair[control_key] = [[0] * 19 for i in range(19)]
            
            delta_signal = [0, 0, 0]
            delta_signal[0] = value[5] - value[0]
            delta_signal[1] = value[6] - value[1]
            delta_signal[2] = value[7] - value[2]

            left_sensor = 0
            right_sensor = 0
            front_sensor = 0
            compare_unit = 25

            if delta_signal[2] > compare_unit:
                left_sensor = 1

            if delta_signal[1] > compare_unit:
                right_sensor = 1

            if delta_signal[0] > 0: 
                front_sensor = 1
            if delta_signal[0] > compare_unit:
                front_sensor = 2
                
            if right_sensor == 1:
                self.motor_pair[control_key][value[3]+9][value[4]+9] -= right_sensor
            if left_sensor == 1:
                self.motor_pair[control_key][value[3]+9][value[4]+9] -= left_sensor
            
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
                        pair_list = [f'{x-9},{y-9}']
                    elif value[x][y] == max_val and max_val > 0:
                        pair_list.append(f'{x-9},{y-9}')
            data_table[key] = pair_list

        # print(data_table) 
        self.generate_data_string(data_table)

    def generate_data_string(self, data_table):
        final_string = ""
        for key, value in data_table.items():
            if len(value) > 0:
                final_string = f'{final_string}{{{key},{value[0]}}},'
        
        print(final_string)

    def display_data(self):
        for key, value in self.motor_pair.items():
            for x in range(0, 19):
                print(f'{key}[{x-9}]: {value[x]}')