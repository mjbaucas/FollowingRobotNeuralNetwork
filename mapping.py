#Simulates the behaviour of the robot and how it translates sensor values to directions

class MappingControl:
    def init(self):
        self.motor_left = {}
        self.motor_right = {}
    
    def train_mapping(self, data, environment):
        for key, value in data.items():
            environment.evaluate_sensors(value[0], value[1], value[2])
            control_key = f'{environment.digital[0]}_{environment.digital[1]}_{environment.digital[2]}'

            if control_key not in self.motor_left:
                self.motor_left[control_key] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            if control_key not in self.motor_right:
                self.motor_right[control_key] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

            if value[5] < 1000 and value[5] > 0:
                self.motor_left[control_key][value[3]+9] += 1
                self.motor_right[control_key][value[3]+9] += 1
            elif value[5] == 0:
                self.motor_left[control_key][value[3]+9] += 2
                self.motor_right[control_key][value[3]+9] += 2
            else:
                self.motor_left[control_key][value[3]+9] -= 2
                self.motor_right[control_key][value[3]+9] -= 2