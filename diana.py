class Player:
  def __init__(self):
    # time-sequence of data which might be useful
    self.global_reputation = list()
    self.num_players = list()
    self.num_cooperators = list()

  def hunt_choices(self,
                    round_number,
                    current_food,
                    current_reputation,
                    m,
                    player_reputations):
    """ Called to get our agent's decision on a new round.

    round_number:       integer, the number round you are in.
    current_food:       integer, the amount of food you have.
    current_reputation: float (python's representation of real numbers), your
                        current reputation.
    m:                  integer, the threshold cooperation value for this round.
    player_reputations: list of floats, the reputations of all the remaining
                        players in the game. The ordinal positions of players in
                        this list will be randomized each round.
    """

    # update with current data
    self.num_players.append(len(player_reputations))
    self.global_reputation.append(calc_global_reputation(player_reputations))

    # NB. I just noticed that we are given all the player_reputations all at
    # once.. This allows us to plan for the whole round all together. This
    # allows us to equilibrate our own reputation with more freedom. For
    # example, let's assume that we go for a strategy which allows us to
    # pre-determine how many hunts/slacks to perform to maintain our
    # reputation. Then we can freely distribute the hunts/slacks so as to
    # maximize the expected gain.

    # initial strategy
    hunt_decisions = [ 's' for r in player_reputations ]
    return hunt_decisions

  def calc_global_reputation(player_reputations):
    """ Temporary: current global reputation as a mean of the reputations. """
    return sum(player_reputations)/len(player_reputations)

  def hunt_outcomes(self, food_earnings):
    """ Called after each round is complete.
    
    food_earnings:      list of integers, the amount of food earned from the
                        last hunt. The amount of food you have for the next hunt
                        will be current_food + sum(food_earnings). This list is
                        in the same order as the decision in the corresponding
                        hunt_choices.
    """
    pass

  def round_end(self, award, m, number_cooperators):
    """ Called after each round is complete.

    award:              integer, total food bonus (can be zero) you received due
                        to players cooperating during the last round. The amount
                        of food you have for the next round will be current_food
                        (including food_earnings from hunt_outcomes this round)
                        + award.
    m:                  BAIS: NOT SPECIFIED.. I GUESS IT'S THE SAME AS IN THE
                        ABOVE FUNCTION. THERE NOTES ARE CRAP, I'VE HAD TO CLEAN
                        THEM QUITE A BIT. THEY SHOULD BE ASHAMED OF THEMSELVES..
                        I DON'T UNDERSTAND WHY THEY DIDN'T JUST MAKE ONE SINGLE
                        METHOD OUT OF THIS AND THE PREVIOUS. I HATE THEM.
    number_cooperators: integer, how many players chose to cooperate over the
                        last round.
    """
    self.num_cooperators.append(number_cooperators)
    pass

