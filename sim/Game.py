from __future__ import division, print_function
import random

# Primary engine for the game simulation. You shouldn't need to edit
# any of this if you're just testing strategies.

def payout(s1,s2):
    if s1 == 'h':
        if s2 == 'h':
            return 0
        else:
            return -3
    else:
        if s2 == 'h':
            return 1
        else:
            return -2
            
            
class GamePlayer(object):
    '''
    Wrapper class for players to keep track of food etc
    Parent is the main game instance, so we can just ask
    how many hunts have happened.
    '''
    def __init__(self, parent, player, food, hunts=0):
        self.parent = parent
        self.player = player
        self.food = food
        self.hunts = hunts
        
    @property
    def rep(self):
        return self.hunts/self.parent.hunt_opportunities if self.parent.hunt_opportunities else 0
        
    def __repr__(self):
        return '{} {} {:.3f}'.format(self.player, self.food, self.rep)

    def __str__(self):
        return "Player {} now has {} food and a reputation of {:.3f}".format(self.player, self.food, self.rep)
        
            
    
class Game(object):
    '''
    Game(players, verbose=True, min_rounds=300, average_rounds=1000)
    
    Primary game engine for the sim. players should be a list of players
    as defined in Player.py or bots.py. verbose determines whether the game
    will print the result of individual rounds to the console or not.
    
    Per the rules, the game has a small but constant probability of ending
    each round after min_rounds. The current defaults are completely arbitrary;
    feel free to play with them.
        
    Call game.play_game() to run the entire game at once, or game.play_round()
    to run one round at a time.
    
    See app.py for a bare-minimum test game.
    '''   
    def __init__(self, players, verbose=True, min_rounds=300, average_rounds=1000):
        self.verbose = verbose
        self.max_rounds = min_rounds + int(random.expovariate(1/(average_rounds-min_rounds)))
        self.round = 0
        self.hunt_opportunities = 0
        
        self.players = players # to set self.P
        start_food = 300*(self.P-1)
        
        self.players = [GamePlayer(self,p,start_food) for p in players]

        # Bais: Here be my prodigy
        self.ranking = []
        
        
    @property
    def m_bonus(self):
        return 2*(self.P-1)
    
    @property
    def P(self):
        return len(self.players)
        
    def calculate_m(self):
        return random.randrange(1, self.P*(self.P-1))
            
        
    def play_round(self):
        # Get beginning of round stats        
        self.round += 1
        if(self.verbose):
            print ("\nBegin Round " + str(self.round) + ":")
        m = self.calculate_m()
        
        # Beginning of round setup
        random.shuffle(self.players)
        reputations = list(player.rep for player in self.players)
        
        # Get player strategies
        strategies = []
        for i,p in enumerate(self.players):
            opp_reputations = reputations[:i]+reputations[i+1:]
            strategy = p.player.hunt_choices(self.round, p.food, p.rep, m, opp_reputations)

            strategy.insert(i,'s')
            strategies.append(strategy)

        # Perform the hunts
        self.hunt_opportunities += self.P-1

        results = [[] for j in range(self.P)]
        for i in range(self.P):
            for j in range(self.P):
                if i!=j:
                    results[i].append(payout(strategies[i][j], strategies[j][i]))
                
        total_hunts = sum(s.count('h') for s in strategies)
        
        if (self.verbose):
            print ("There were {} hunts of {} needed for bonus".format(total_hunts, m))

        if total_hunts >= m:
            bonus = self.m_bonus
            if (self.verbose):
                print("Cooperation Threshold Acheived. Bonus of {} awarded to each player".format(self.m_bonus))
        else:
            bonus = 0
        
        # Award food and let players run cleanup tasks
        for strat, result, player in zip(strategies, results, self.players):
            food = sum(result)
            hunts = strat.count('h')
            
            player.food += food+bonus
            player.hunts += hunts
            player.player.hunt_outcomes(result)
            player.player.round_end(bonus, m, total_hunts)
            
    
        if self.verbose:
            newlist = sorted(self.players, key=lambda x: x.food, reverse=True)
            for p in newlist:
                print (p)
                   
        
        if self.game_over():            
            print ("Game Completed after {} rounds".format(self.round))
            raise StopIteration
            
        
    def game_over(self):        
        starved = [p for p in self.players if p.food <= 0]
        num_starved = len(starved)
        for p in starved:
            print ("{} has starved and been eliminated in round {}".format(p.player, self.round))
            self.ranking.insert(0, (self.P - num_starved + 1, self.round, p))
        
        self.players = [p for p in self.players if p.food > 0]

        if (self.P < 2) or (self.round > self.max_rounds):
            for p in self.players:
                self.ranking.insert(0, (1, self.round, p))
        
        return (self.P < 2) or (self.round > self.max_rounds)
        
        
    def play_game(self):
        '''
        Preferred way to run the game to completion
        Written this way so that I can step through rounds one at a time
        '''
        print ("Playing the game to the end:")
        
        while True:
            try:
                self.play_round()
            except StopIteration:
                if len(self.players) <= 0:
                    print ("Everyone starved")
                elif (len(self.players) == 1):
                    print ("The winner is: ", self.players[0].player)
                else:
                    survivors = sorted(self.players, key=lambda player: player.food, reverse=True)
                    print ("The winner is: ", survivors[0].player)
                    print ("Multiple survivors:")
                    print (survivors)
                break

        mantitles = {
            'exit':   'Exits simulation.',
            'ls':     'List of player rankings.',
            'man':    'Explanation of command.',
            'help':   'Lists all the commands.',
            'plot':   'Plots ranks.',
            'stats':  'Stats of a player.',
            }
        manuals = {
            'man':    'Inputs: command name.',
            'stats':  'Inputs: player rank.',
            }
        usages = {
            'man':    'Usage: man <cmd>',
            'stats':  'Usage: stats <rank_player>'
            }
        
        print()
        print('Welcome to the query console.')
        print('To get started, type \'help\'.')
        while True:
            cmd = raw_input('>> ').split(' ')
            for i in range(cmd.count('')):
                cmd.remove('')

            if len(cmd) == 0:
                print('Command not found.')
            elif cmd[0] == 'exit':
                break;
            elif cmd[0] == 'man':
                if len(cmd) > 1 and mantitles.has_key(cmd[1]):
                    print(mantitles[cmd[1]])
                    if usages.has_key(cmd[1]):
                      print(usages[cmd[1]])
                    if manuals.has_key(cmd[1]):
                      print()
                      print(manuals[cmd[1]])
                else:
                    print(usages['man'])
            elif cmd[0] == 'help':
                for k, v in mantitles.iteritems():
                    print(k, '\t', v)
            elif cmd[0] == 'ls':
                print('Rank\tPlayer\t\t\tRound\tFood')
                print('-----------------------------------------')
                for rank, n_round, p in self.ranking:
                  print('{0}\t{1}\t\t{2}\t{3}'
                      .format(rank,
                              p.player.name.ljust(10),
                              n_round,
                              p.food if p.food > 0 else '--- '))
            elif cmd[0] == 'plot':
                print('NYI')
            elif cmd[0] == 'stats':
                print('NYI')
            else:
                print('Command not found.')

