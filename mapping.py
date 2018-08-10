#Simulates the behaviour of the robot and how it translates sensor values to directions

class MappingControl:
    def init(self):
        self.map = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.data = {}
    
    def simulate_mapping(self, sensor0, sensor1, sensor2, direction):
        if sensor0 < 3 and sensor1 < 3 and sensor2 < 3:
            return 0
        
        if sensor0 >= 3 and sensor1 < 3 and sensor2 < 3:
            if direction == 'N':
                return 1
            return 0
        
        if sensor1 >= 3 and sensor0 < 3 and sensor2 < 3:
            if direction == 'E':
                return 1
            return 0
        
        if sensor2 >= 3 and sensor0 < 3 and sensor1 < 3:
            if direction == 'W':
                return 1
            return 0
        
        if sensor0 >= 3 and sensor1 >= 3 and sensor2 < 3:
            if sensor0 > sensor1:
                if direction == 'N':
                    return 1
                return 0
            
            if sensor0 == sensor1:
                if direction == 'NE':
                    return 1
                return 0
            
            if sensor0 < sensor1:
                if direction == 'E':
                    return 1
                return 0
            
        if sensor0 >= 3 and sensor2 >= 3 and sensor1 < 3:
            if sensor0 > sensor2:
                if direction == 'N':
                    return 1
                return 0
            
            if sensor0 == sensor2:
                if direction == 'NW':
                    return 1
                return 0
            
            if sensor0 < sensor2:
                if direction == 'W':
                    return 1
                return 0
        
        if sensor1 >= 3 and sensor2 >= 3 and sensor0 < 3:
            if sensor1 > sensor2:
                if direction == 'SE':
                    return 1
                return 0
            
            if sensor1 == sensor2:
                if direction == 'S':
                    return 1
                return 0
            
            if sensor1 < sensor2:
                if direction == 'SW':
                    return 1
                return 0

        if sensor0 >= 3 and sensor1 >= 3 and sensor2 >= 3:
            return 0
    
    def update_mapping(self, data):
        file = open('rules.txt', 'w')
        file.close()
        file = open("rules.txt", "a")

        for key, value in data.items():
            sensor_values = key.split("_")
            file.write(f'{sensor_values[0]} {sensor_values[1]} {sensor_values[2]} {value}\n')