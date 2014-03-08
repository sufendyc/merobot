#!/usr/bin/python
import sys, random

shot_grid = []

def main():
    global shot_grid
    shot_grid = sys.argv[1].split(',')
    next_target = None
    
    for key, status in enumerate(shot_grid):
        if is_hit(key):
            next_target = find_next_target(key)
            if next_target:
                break
    
    while(not next_target):
        rnd_target = random.randint(0, len(shot_grid) - 1)
        if(is_unknown(rnd_target)):
            next_target = rnd_target
            break

    hit(next_target)
            
def find_next_target(x, dir = None):
    surr = get_surr(x)
    next_target = None
    # return the unknown point of this direction
    if dir:
        if dir in surr:
            if is_unknown(surr[dir]):
                next_target = surr[dir]
            elif is_hit(surr[dir]):
                next_target = find_next_hit(surr[dir], dir)
    else:
        for dir, nex in surr.items():
            if is_unknown(nex):
                next_target = nex
            elif is_hit(nex): 
                next_target = find_next_target(nex, dir)
                break
    
    return next_target
    

def hit(x):
    sys.stdout.write(str(x))

def get_surr(x):
    surr = {'n' : north(x), 'e' : east(x), 's' : south(x), 'w': west(x)}
    for key, val in surr.items():
        if surr[key] == None: del surr[key]
    
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
    return shot_grid[x] == '1'

def is_unknown(x):
    return shot_grid[x] == '0'

def is_missed(x):
    return shot_grid[x] == '-1'

if __name__ == "__main__":
    main()