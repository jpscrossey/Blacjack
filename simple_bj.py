# simple_bj

'''
SIMPLE BLACKJACK GAME
'''

import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":11}

playing = True

# CARD CLASS
class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return self.rank + " of " + self.suit

# DECK CLASS
class Deck():
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
            
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has:" + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
# HAND CLASS
class Hand():
    
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1
        
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value = self.value - 10
            self.aces = self.aces - 1
            
# CHIPS CLASS
class Chips():
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
    def lose_bet(self):
        self.total -= self.bet

'''
FUNCTION DEFINITIONS
'''

# TAKE A BET
def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("\nHow much do you want to bet? "))
        except ValueError:
            print("\nSorry, your bet must be an integer!")
        else:
            if chips.bet > chips.total:
                print("\nSorry, your bet cannot exceed",chips.total)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck,hand):
    global playing
    
    while True:
        x = input("\nWould you like to hit or stand? Enter 'h' or 's': ")
        
        if x[0].lower() == "h":
            hit(deck,hand)
        elif x[0].lower() == "s":
            print("\nPlayer stands, Dealer is playing")
            playing = False
        else:
            print("\nSorry, please try again.")
            continue
        break
        
def show_some(player,dealer):
    print("\nDealer's Hand")
    print(" <card hidden>")
    print("",dealer.cards[1])
    print("\nPlayer's Hand", *player.cards, sep="\n ")
    
def show_all(player,dealer):
    print("\nDealer's Hand:", *dealer.cards, sep="\n ")
    print("Dealer's Hand = ",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep="\n ")
    print("Player's Hand = ",player.value)
    
def player_busts(player,dealer,chips):
    print("\nPlayer Busts!")
    chips.lose_bet()
    
def player_wins(player,dealer,chips):
    print("\nPlayer Wins!")
    chips.win_bet()
    
def dealer_busts(player,dealer,chips):
    print("\nDealer Busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("\nDealer Wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("\nIt's a Push.")
    
'''
GAMEPLAY
'''

while True:
    print("\nWelcome to Blackjack!  Get as close to 21 as possible. \n\nDealer sticks on 17.  Aces count as either 1 or 11.")
    
    # CREATE AND SHUFFLE DECK - DEALING TWO CARDS TO PLAYER AND DEALER
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    # SETUP THE PLAYERS CHIPS
    player_chips = Chips()
    
    # PROMPT FOR BET
    take_bet(player_chips)
    
    # SHOW THE CARDS
    show_some(player_hand,dealer_hand)
    
    # RECALL FROM HIT OR STAND
    while playing:
        
        # PROMT PLAYER TO HIT OR STAND
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
        
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break
            
    # IF PLAYER NOT BUST, PLAY DEALER HAND
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
                hit(deck,dealer_hand)
                
        # SHOW ALL CARDS
        show_all(player_hand,dealer_hand)
        
        #DIFFERENT WINNING SCENARIOS
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
            
    # PLAYERS TOTAL CHIPS
    print("\nPlayer chip count stands at:",player_chips.total)
    
    # ASK TO PLAY AGAIN
    new_game = str(input("\nWould you like to play another hand?  Enter 'y' or 'n'. "))
    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("\nThanks for playing.")
        break
