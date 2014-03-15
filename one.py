import rg, random

class Robot:

    def act(self, game):
        # TODO:
        # Swarm around the sub-leader bot
        # attack in group, increase radius of search to 2-3 tiles away
        
        #print " robot {} has moves ".format(self.robot_id), self.move_randomly(game)
        #print " robot {} has {} enemy around".format(self.robot_id, len(self.enemy_around(game)))
        if self.move_randomly(game):
            return self.move_randomly(game)
        else:
            enemies_1 = self.enemy_around(game, 1)
            enemies_2 = self.enemy_around(game)
            if len(enemies_1) > 0:
                if self.hp <= 15: 
                    return ['suicide']
                #attack the weakest enemy
                weakest_enemy = self.find_weakest(enemies_1)
                return ['attack', weakest_enemy.location]
            elif len(enemies_2) > 0:
                #no enemy around, extend to 2nd radius
                weakest_enemy = self.find_weakest(enemies_2)
                return ['move', rg.toward(self.location, weakest_enemy.location)]
                
            return ['guard']
        #else:
        #next_move = rg.toward(self.location, rg.CENTER_POINT)
        #if next_move in game.robots
        #else:
        #    return ['move', next_move]

        return ['guard']
    
    def find_weakest(self, enemies):
        if len(enemies) > 0:
            weakest_enemy = enemies[0]
            if len(enemies) > 1:
                for enemy in enemies[1:]:
                    if enemy.hp < weakest_enemy.hp:
                        weakest_enemy = enemy
        
            return weakest_enemy
    
    def enemy_around(self, game, radius=3, location = None):
        locs = self.locs(location)
        enemies = []
        for possible_loc in locs:
            if possible_loc in game.robots and game.robots[possible_loc].player_id != self.player_id:
                enemies.append(game.robots[possible_loc])
                
        if len(enemies) == 0 and radius > 1:
            for possible_loc in locs:
                enemies = self.enemy_around(game, radius - 1, possible_loc)
        
        return enemies
        
    def locs(self, location=None):
        if not location: location = self.location
        return rg.locs_around(location, filter_out=('invalid', 'obstacle'))
    
    def move_randomly(self, game):
        locs = self.locs()
        # move around randomly if there is no enemy around or life is low
        if (self.low_hp()) or len(self.enemy_around(game)) == 0:
            empty = []
            # find empty 
            for possible_loc in locs:
                if possible_loc not in game.robots and 'spawn' not in rg.loc_types(possible_loc):
                    if not (self.low_hp() and len(self.enemy_around(game, 1, possible_loc)) > 0):
                        empty.append(possible_loc)
            
            #avoid getting stuck at the corner
            if 'spawn' in rg.loc_types(possible_loc) and len(empty) == 0:
                empty.append(possible_loc)
            
            if len(empty) > 0:
                rnd = random.randint(0, len(empty) - 1)
                return ['move', empty[rnd]]

        return False
    
    def low_hp(self):
        min = 5
        max = 15
        return True if self.hp > min and self.hp < max else False
    
    # TODO:
    # find the nearest sub-leader bot
    def leader_bot(self, game):
        for loc, robot in game.robots.iteritems():
            if robot.player_id == self.player_id:
                return robot.location