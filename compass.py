import random

class CompassControl:
    def init(self):
        self.map = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        self.network = self.set_direction_network()
    
    def set_direction_network(self):
        file = open("compass.txt", "r")
        
        temp_dict = {}
        for line in file:
            temp_list = line.split()
            temp_dict[temp_list[0]] = [int(temp_list[1]), int(temp_list[2])]
        
        return temp_dict

    def update_compass(self, data):
        file = open('compass.txt', 'w')
        file.close()
        file = open("compass.txt", "a")

        for key, value in data.items():
            file.write(f'{key} {value[0]} {value[1]} \n')

    def find(self, location):
        temp_map = self.map
        
        if location not in temp_map:
            return -1
        else: 
            position = temp_map.index(location)
         
        move_counter = 0
        
        if self.network and self.network[location][0] != -1:
            direction = 1 - self.network[location][1]
        else:
            direction = random.randrange(0,2)
        
        while position != 0:
            if direction == 0:
                position += 1
            else:
                position -= 1
            move_counter += 1

            if position > 7:
                position = 0

            if position < 0:
                position = 7
        
        if self.network and move_counter < self.network[location][0] or self.network[location][0] == -1 :
            self.network[location][1] = direction
            self.network[location][0] = move_counter
            self.update_compass(self.network)    

        return [move_counter, direction], 0

        