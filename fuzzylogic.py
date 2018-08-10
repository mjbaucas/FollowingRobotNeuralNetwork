#Uses both mapping and compass values to create an environment that can translate sensor values to robot motion

class Environment:
    def init(self, sensor0, sensor1, sensor2):
        self.calibrate(sensor0, sensor1, sensor2)
        self.rules = self.set_rules()
        self.compass = self.set_compass()

    def set_rules(self):
        file = open("rules.txt", "r")
        
        temp_dict = {}
        for line in file:
            temp_list = line.split()
            temp_dict[f'{temp_list[0]}-{temp_list[1]}-{temp_list[2]}'] = temp_list[3]
        
        return temp_dict
    
    def set_compass(self):
        file = open("compass.txt", "r")
        
        temp_dict = {}
        for line in file:
            temp_list = line.split()
            temp_dict[temp_list[0]] = [int(temp_list[1]), int(temp_list[2])]
    
        return temp_dict

    def calibrate(self, sensor0, sensor1, sensor2):
        value_high = max(sensor0, sensor1, sensor2)
        value_low = min(sensor0, sensor1, sensor2)
        
        temp_list = [sensor0, sensor1, sensor2]
        temp_list = sorted(temp_list)
        value_mid = temp_list[1]

        if not hasattr(self, 'high') or self.high < value_high:
            self.high = value_high
            
        if not hasattr(self, 'mid') or self.mid < value_mid:
            self.mid = value_mid
        
        if not hasattr(self, 'low') or self.low > value_low:
            self.low = value_low
        
        if self.high > value_high or self.mid > value_high or self.low > value_high:
            self.high = value_high
            self.mid = value_mid
            self.low = value_low

    def evaluate_sensor(self, sensor):
        sensor_value = 0

        if sensor >= self.low: 
            sensor_value += 1

        if sensor >= self.mid: 
            if sensor == self.mid:
                sensor_value += 1
            else:
                sensor_value += 2

        if sensor >= self.high: 
            sensor_value += 1

        return sensor_value

    def evaluate(self, sensor0, sensor1, sensor2):
        direction = self.evaluate_direction(sensor0, sensor1, sensor2)
        self.evaluate_output(direction)

    def evaluate_direction(self, sensor0, sensor1, sensor2):
        value0 = self.evaluate_sensor(sensor0)
        value1 = self.evaluate_sensor(sensor1)
        value2 = self.evaluate_sensor(sensor2)
        
        heat_map = [value0, value1, value1, value1, value1, value2, value2]

        direction = 'C'
        if hasattr(self, 'rules'):
            temp_list = self.rules[f'{value0}-{value1}-{value2}']
            direction = temp_list

            if direction == 'C':
                self.calibrate(sensor0, sensor1, sensor2)
                try:
                    direction = self.evaluate_direction(sensor0, sensor1, sensor2)
                except RuntimeError as re:
                    direction = 'T'

        return direction

    def evaluate_output(self, direction):
        compass = self.compass            

        if direction in compass:
            if compass[direction][1] == 0:
                print(f'{direction}: Turn {compass[direction][0]} notch(es) clockwise')
            elif compass[direction][1] == 1:
                print(f'{direction}: Turn {compass[direction][0]} notch(es) counter-clockwise')
            else:
                print(f'{direction}: Unknown direction and moves')
        else:
            if direction == 'T':
                print(f'T: Robot timed out, stuck in calibrate loop')
            else:
                print(f'U: Unknown direction and moves')
