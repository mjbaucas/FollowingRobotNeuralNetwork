#Uses both mapping and compass values to create an environment that can translate sensor values to robot motion
from common import find_indexes_in_list

class Environment:
    def init(self, sensor0, sensor1, sensor2):
        self.digital = [0, 0, 0]
        self.baseline = [0, 0, 0]
        self.sensors = [0, 0, 0]
        self.calibrate(sensor0, sensor1, sensor2)

    def calibrate(self, sensor0_data, sensor1_data, sensor2_data):
        self.baseline[0] = min(sensor0_data)
        self.baseline[1] = min(sensor1_data)
        self.baseline[2] = min(sensor2_data)
        
    def evaluate_sensors(self, sensor0, sensor1, sensor2):
        self.sensors[0] = sensor0 - self.baseline[0]
        self.sensors[1] = sensor1 - self.baseline[1]
        self.sensors[2] = sensor2 - self.baseline[2]
        
        for x in range(0,3):
            if self.sensors[x] < 0:
                self.sensors[x] = 0

        high = self.sensors.index(max(self.sensors))
        low = self.sensors.index(min(self.sensors))
        if high == low:
            high = 0
            mid = 1
            low = 2
        else:
            mid = 3 - (high + low)
        
        compare_unit = 50
        high_low_diff = self.sensors[high] - self.sensors[low]  

        # Establish relation between high and low values
        if high_low_diff >= 9*compare_unit:
            self.digital[high] = 4
            self.digital[low] = 0
        elif high_low_diff >= 7*compare_unit:
            self.digital[high] = 3
            self.digital[low] = 0
        elif high_low_diff >= 5*compare_unit:
            self.digital[high] = 2
            self.digital[low] = 0
        elif high_low_diff >= 2*compare_unit:
            self.digital[high] = 1
            self.digital[low] = 0
        else:
            self.digital[high] = 0
            self.digital[low] = 0
        
        # First quartile
        if self.sensors[mid] >= (high_low_diff)/4:
            self.digital[mid] = round((self.digital[high] - self.digital[low])/4)
        
        # Second quartile
        if self.sensors[mid] >= (high_low_diff)/2:
            self.digital[mid] = round((self.digital[high] - self.digital[low])/2)

        # Third quartile
        if self.sensors[mid] >= 3*((high_low_diff)/4):
            self.digital[mid] = round(3*(self.digital[high] - self.digital[low])/4)
        
        # If high and mid ratios are the same
        if self.sensors[mid] == self.sensors[high]:
            self.digital[mid] = self.digital[high]

        # If mid and low ratios are the same
        if self.sensors[mid] == self.sensors[low]:
            self.digital[mid] = self.digital[low]
        