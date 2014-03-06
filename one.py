import rg, random

class Robot:

    def act(self, game):
        #print " robot {} has moves ".format(self.robot_id), self.move_randomly(game)
        #print " robot {} has {} enemy around".format(self.robot_id, len(self.enemy_around(game)))
        if self.move_randomly(game):
            return self.move_randomly(game)
        else:
            enemies = self.enemy_around(game)
            if len(enemies) > 0:
                #if self.hp <= 5: 
                #    return ['suicide']
                #attack the weakest enemy
                weakest_enemy = enemies[0]
                if len(enemies) > 1:
                    for enemy in enemies[1:]:
                        if enemy.hp < weakest_enemy.hp:
                            weakest_enemy = enemy
                return ['attack', weakest_enemy.location]
            return ['guard']
        #else:
        #next_move = rg.toward(self.location, rg.CENTER_POINT)
        #if next_move in game.robots
        #else:
        #    return ['move', next_move]

        return ['guard']
        
    def enemy_around(self, game):
        locs = self.locs()
        enemies = []
        for possible_loc in locs:
            if possible_loc in game.robots and game.robots[possible_loc].player_id != self.player_id:
                enemies.append(game.robots[possible_loc])
        
        return enemies
        
    def locs(self):
        return rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
    
    def move_randomly(self, game):
        locs = self.locs()
        empty = []
        for possible_loc in locs:
            if possible_loc not in game.robots and 'spawn' not in rg.loc_types(possible_loc):
                empty.append(possible_loc)
                
        if len(empty) == 0 and possible_loc:
            empty.append(possible_loc)
        
        rnd = random.randint(0, len(empty) - 1)
        
        if (self.hp < 15) or len(self.enemy_around(game)) == 0:
            if len(empty) > 0:        
                return ['move', empty[rnd]]
            else:
                return False
        else:
            return False
    
    def leader_bot(self, game):
        for loc, robot in game.robots.iteritems():
            if robot.player_id == self.player_id:
                return robot.location