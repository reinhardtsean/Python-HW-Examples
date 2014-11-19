"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
Prepared by: Sean R
link: http://www.codeskulptor.org/#user35_sb6ZKif9AjwpHmO_8.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(60)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    summy = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
    maxy = 0
    for ind in hand:
        summy[ind] = ind + summy[ind]
    for key in summy:
        if summy[key] > maxy:
            maxy = summy[key]
    return maxy

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold: tuple(n1,n2,..nm)
    num_die_sides: number of sides on each die: int
    num_free_dice: number of dice to be rolled: int

    Returns a floating point expected value
    """
    seq = [ind+1 for ind in range(num_die_sides)]
    listy = list(gen_all_sequences(seq, num_free_dice))
    trials = len(listy)
    u_prob = 1.0/trials
    final_score = 0.0
    for index in range(trials):
        test_hand = list(held_dice)
        for inx in range(num_free_dice):
            test_hand.append(listy[index][inx])
        final_score += score(test_hand)*u_prob
    return final_score
        
def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    answer_set = set([()])
    mask = gen_all_sequences([0,1], len(hand))
    for inx in mask:
        temp = []
        for iny in range(len(hand)):
            test = inx[iny]*hand[iny]
            if test != 0:
                temp.append(test)
        answer_set.add(tuple(temp))
    return answer_set

    
        
def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    trial_holds = list(gen_all_holds(hand))
    best_score = 0.0
    best_hand = ()
    for hold in trial_holds:
        test_score = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if test_score > best_score:
            best_score = test_score
            best_hand = hold
    
    return (best_score, best_hand)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score

    
#run_example()


#mport poc_holds_testsuite
#oc_holds_testsuite.run_suite(gen_all_holds)
                                       
    



