from Player import BasePlayer

class TitForTatter(BasePlayer):
    def __init__(self):
        self.name = "TitForTatter"
        self.actions_recv = []

    def hunt_choices(
                    self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations,
                    ):

        if self.actions_recv == []:
            return ['h']*len(player_reputations)
        else:
            return self.actions_recv[:len(player_reputations)]

    def hunt_outcomes(self, food_earnings):
        self.actions_recv = []

        for earning in food_earnings:
            self.actions_recv.append(self.infere_action(earning))

    def infere_action(self, food_earning):
        if food_earning == -2:
            # none hunted
            return 's'
        elif food_earning == 1:
            # you hunted but I didn't, lol
            return 'h'
        elif food_earning == -3:
            # I hunted but you bastard didn't
            return 's'
        elif food_earning == 0:
            # we both hunted, like machotes
            return 'h'
        else:
            assert(False)

if __name__ == '__main__':
    titForTatter = TitForTatter()
    print titForTatter.name
    print titForTatter.actions_recv
    titForTatter.actions_recv = ['h','s','h','h','h']


