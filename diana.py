class Player:
  def __init__(self):
    # time-sequence of data which might be useful
    self.g_rep = list()
    self.n_players = list()
    self.n_coops = list()
    self.actions = list()

    self.u_to_a = dict()
    self.u_to_a[('h', 0)] = 'h'
    self.u_to_a[('s', -3)] = 'h'
    self.u_to_a[('h', 1)] = 's'
    self.u_to_a[('s', -2)] = 's'

  def hunt_choices(self,
                    round_number,
                    my_food,
                    my_reputation,
                    m,
                    reps):
    """ Called to get our agent's decision on a new round.

    round_number:       integer, the number round you are in.
    my_food:            integer, the amount of food you have.
    my_reputation:      float (python's representation of real numbers), your
                        current reputation.
    m:                  integer, the threshold cooperation value for this round.
    reps:               list of floats, the reputations of all the remaining
                        players in the game. The ordinal positions of players in
                        this list will be randomized each round.
    """

    # update with current data
    self.n_players.append(len(reps))
    self.g_rep.append(global_rep(reps))

    # NB. I just noticed that we are given all the player_reputations all at
    # once.. This allows us to plan for the whole round all together. This
    # allows us to equilibrate our own reputation with more freedom. For
    # example, let's assume that we go for a strategy which allows us to
    # pre-determine how many hunts/slacks to perform to maintain our
    # reputation. Then we can freely distribute the hunts/slacks so as to
    # maximize the expected gain.

    # initial strategy
    actions = [ 's' for r in reps ]

    self.actions.append(actions)
    return actions

  def global_rep(reps):
    """ Temporary: current global reputation as a mean of the reputations. """
    return sum(reps)/len(reps)

  def hunt_outcomes(self, food_earnings):
    """ Called after each round is complete.
    
    food_earnings:      list of integers, the amount of food earned from the
                        last hunt. The amount of food you have for the next hunt
                        will be current_food + sum(food_earnings). This list is
                        in the same order as the decision in the corresponding
                        hunt_choices.
    """

    their_actions = determine_opponent_decisions(food_earnings)
    # TODO determine how my reputation has influenced their actions

  def determine_opponent_decisions(utilities):
    return [ self.u_to_a[(x, y)] for x, y in zip(self.actions[-1], utilities) ]

  def round_end(self, award, m, n_cooperators):
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
    self.n_coops.append(n_cooperators)
    pass

