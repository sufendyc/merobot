#!/usr/bin/python
import sys, random

shot_grid = []

def main():
    global shot_grid
    shot_grid = sys.argv[1].split(',')
    next_target = None

    if "1" in shot_grid:
        #there is a ship that is half sunk. Hunt the ship down
        next_target = get_next_guess_by_hit()
    else:
        next_target = get_parity_guess()

    while next_target is None:
        # TESTING: should already found a target by now.
        rnd_target = random.randint(0, len(shot_grid) - 1)
        if(is_unknown(rnd_target)):
            next_target = rnd_target
            break


    hit(next_target)

def get_parity_guess():
    # hit a random parity point when there is no half sunk ship found
    next_target = None
    parity = filter(lambda num: sum(map(int, str(num))) % 2 == 0 and is_unknown(num), list(xrange(len(shot_grid))))
    
    weights = {0: 100, 2: 5,4: 90,6: 5, 8: 5}
    weighted_parity = []

    for idx in parity:
        dist = abs(4 - idx/10) + abs(4 - idx%10)
        #diff = abs((idx / 10) - (idx % 10))
        weight = 101 - (dist*dist)
        weighted_parity.extend([idx] * weight)
        #weighted_parity.extend([idx] * weights[diff])

    next_target = random.choice(weighted_parity)
    
    #next_target = random.choice(parity)

    return next_target

def get_next_guess_by_hit():
    # hit the surrounding area of a known hit point, to try to sink a ship
    last_hit = shot_grid.index("1") #find the first occurance of the hit cell
    surr = get_surr(last_hit)
    next_target = None

    opposite = {'n' : 's', 'w': 'e', 'e' : 'w', 's' : 'n'}

    for dr, grid_id in surr.items():
        if is_unknown(grid_id):
            next_target = grid_id

        headed_back = False
        while is_hit(grid_id):
            new_grid_surr = get_surr(grid_id)
            if dr in new_grid_surr:
                grid_id  = new_grid_surr[dr]
            elif headed_back:
                break
            else:
                headed_back = True
                dr = opposite[dr]

            if is_unknown(grid_id):
                next_target = grid_id
                return next_target

    return next_target


def hit(x):
    sys.stdout.write(str(x))

def get_surr(x):
    surr = {'n' : north(x), 'w': west(x), 'e' : east(x), 's' : south(x)}
    for key, val in surr.items():
        target = surr[key]
        if target == None or is_missed(target): del surr[key]
    
    return surr

def north(x):
    nex = x - 10
    if nex >= 0: return nex

def east(x):
    nex = x + 1
    if nex < 100 and nex / 10 == x / 10: return nex

def south(x):
    nex = x + 10
    if nex < 100: return nex
    
def west(x):
    nex = x - 1
    if nex >= 0 and nex/10 == x/10: return nex
    
def is_hit(x):
    return shot_grid[x] in ['1' , '2']

def is_unknown(x):
    return shot_grid[x] == '0'

def is_missed(x):
    return shot_grid[x] == '-1'

def is_sunk(x):
    return shot_grid[x] == '2'

if __name__ == "__main__":
    main()