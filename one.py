import rg, random

class Robot:

    def act(self, game):
        locs = self.locs()
        enemies = self.enemy_around(game)
        #suicide mode
        if self.hp <= 15 and len(enemies) > 1:
            return ['suicide']
        
        #attack mode
        if len(enemies) > 0:
            #attack the weakest enemy
            weakest_enemy = enemies[0]
            for enemy in enemies[:1]:
                if enemy.hp < weakest_enemy.hp:
                    weakest_enemy = enemy
            return ['attack', weakest_enemy.location]
        # move to center
        else:
            
            next_move = rg.toward(self.location, self.leader_bot(game))
            if next_move in game.robots:
                return ['guard']
            else:
                return ['move', next_move]

        return ['guard']
        
    def enemy_around(self, game):
        locs = self.locs()
        enemies = []
        for possible_loc in locs:
            if possible_loc in game.robots and game.robots[possible_loc].player_id != self.player_id:
                enemies.append(game.robots[possible_loc])
        
        return enemies
    
    def locs(self):
        return rg.locs_around(self.location, filter_out=('invalid', 'obstacle', 'spawn'))
        
    def leader_bot(self, game):
        for loc, robot in game.robots.iteritems():
            if robot.player_id == self.player_id:
                return robot.location