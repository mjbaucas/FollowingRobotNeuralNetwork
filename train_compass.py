# Pseudo train compass logic

from random import randrange

from compass import CompassControl

if __name__ == "__main__":
    control = CompassControl()

    control.init()
    for x in range(100):
        direction = control.map[randrange(0, 8)]
        moves, find = control.find(direction)
        if find == 0:
            print(f'{direction} FOUND, MOVES:{moves}')    
        else:
            print(f'{direction} NOT FOUND, MOVES:{moves}')