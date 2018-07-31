class Environment:
    def init(self, sensor0, sensor1, sensor2):
        self.calibrate(sensor0, sensor1, sensor2)
        self.rules = self.set_rules()

    def set_rules(self):
        file = open("rules.txt", "r")
        
        temp_dict = {}
        for line in file:
            temp_list = line.split()
            temp_dict[f'{temp_list[0]}-{temp_list[1]}-{temp_list[2]}'] = [temp_list[3], temp_list[4]]
        
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
        direction, calibrate = self.evaluate_direction(sensor0, sensor1, sensor2)
        self.evaluate_output(direction)

    def evaluate_direction(self, sensor0, sensor1, sensor2):
        value0 = self.evaluate_sensor(sensor0)
        value1 = self.evaluate_sensor(sensor1)
        value2 = self.evaluate_sensor(sensor2)
        
        direction = 'X'
        calibrate = 'X'

        if hasattr(self, 'rules'):
            temp_list = self.rules[f'{value0}-{value1}-{value2}']
            direction = temp_list[0]
            calibrate = temp_list[1]

            if calibrate == 'C':
                self.calibrate(sensor0, sensor1, sensor2)
                if direction == 'X':
                    direction, calibrate = self.evaluate_direction(sensor0, sensor1, sensor2)
        
        return direction, calibrate

    def evaluate_output(self, direction):
        if direction == 'N':
            print('Forward')              
        elif direction == 'NE':
            print('45* Clockwise')              
        elif direction == 'E':
            print('90* Clockwise')
        elif direction == 'SE':
            print('135* Clockwise')          
        elif direction == 'S':
            print('180* Clockwise')              
        elif direction == 'SW':
            print('135* Counter Clockwise')              
        elif direction == 'W':
            print('90* Counter Clockwise')              
        elif direction == 'SW':
            print('45* Counter Clockwise')              
        else:
            print('Stop')              

    def print_values(self):
        print(f'HIGH: {self.high}, MID: {self.mid}, LOW: {self.low}')       

    