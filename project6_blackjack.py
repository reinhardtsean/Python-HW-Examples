# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = None
player_score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        global in_play
        if in_play == True and pos == [200,100]:
            card_loc = CARD_BACK_CENTER
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        ster = ""
        for c in self.cards:
            ster = ster + c.__str__() + " " 
        return ster

    def add_card(self, card):
        # add a card object to a hand
        self.cards.append(card)        
        
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        tot =0
        ACE = False
        for c in self.cards:
            rank = c.get_rank()
            if rank == 'A':
                ACE = True
            tot += VALUES[rank]
        if ACE == True and tot < 12:
            tot +=10
            
        return tot
        
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for c in self.cards:
            c.draw(canvas, pos)
            pos[0] = pos[0] + CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                car = Card(suit,rank)
                self.deck.append(car)
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)
    
    def __str__(self):
        ster = ""
        for c in self.deck:
            ster = ster + c.__str__() + " " 
        return ster

p1_hand = Hand()
deal_hand = Hand()

#define event handlers for buttons
def deal():
    global outcome, in_play
    global deck, p1_hand, deal_hand, player_score
    if in_play == True:
        player_score -= 1
    deck = Deck()
    deck.shuffle()
    in_play = True
    p1_hand = Hand()
    deal_hand = Hand()
    p1_hand.add_card(deck.deal_card())
    p1_hand.add_card(deck.deal_card())
    deal_hand.add_card(deck.deal_card())
    deal_hand.add_card(deck.deal_card())
    outcome = "Hit or Stand?"
    


def hit():
    global deal_hand, p1_hand, in_play, outcome
    if in_play == True:
        if p1_hand.get_value() < 22:
            card = deck.deal_card()
            p1_hand.add_card(card)
        if p1_hand.get_value() >= 22:
            outcome = "You're busted!"


def stand():
    global deal_hand, p1_hand
    global in_play, outcome, player_score
    if in_play == True:
        in_play = False
        if p1_hand.get_value() > 21:
            outcome = "You're busted!"
            player_score -=1
        else:
            while deal_hand.get_value() < 17 and deal_hand.get_value() < p1_hand.get_value():
                card = deck.deal_card()
                deal_hand.add_card(card)
                
            if deal_hand.get_value() >= 22:
                outcome = "Dealer busted, Player Wins!"
                player_score +=1
                #check for win
            elif deal_hand.get_value() >= p1_hand.get_value():
                outcome = "Dealer Wins"   
                player_score -=1
            else:
                outcome = "Player Wins"
                player_score +=1
    

# draw handler    
def draw(canvas):
    global p1_hand, deal_hand
    p1_hand.draw(canvas, [200,300])
    deal_hand.draw(canvas, [200,100])
    
    canvas.draw_text("-- Player's Hand --", (200, 290), 24, 'White')
    canvas.draw_text("-- Dealer's Hand --", (200, 90), 24, 'White')
    canvas.draw_text("Player's Score: " + str(player_score), (420, 20), 24, 'White')
    canvas.draw_text(str(outcome), (100, 550), 24, 'White')
    canvas.draw_text("BLACKJACK", (200, 20), 24, 'White')
     

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
