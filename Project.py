import random
from typing import List

cards = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RSkip",
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GSkip",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BSkip",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YSkip",
    "W+4", "W+4", "WJ", "WJ"
]

deck = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RSkip",
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GSkip",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BSkip",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YSkip",
    "W+4", "W+4", "WJ", "WJ"
]

P1 = []
P2 = []
P3 = []
P4 = []
revDeck = []

def assignCards() -> List[int]:
    arr = []
    for i in range(3):
        card = random.randint(0, len(deck) - 1)
        arr.append(deck[card])
        deck.remove(deck[card])
    return arr

def pick():
    card = random.randint(0, len(deck) - 1)
    return deck[card]

def exchange(num, player, card) -> List[int]:
    revDeck.append(player[num])
    player[num] = card
    return player

P1 = assignCards()
P2 = assignCards()
P3 = assignCards()
P4 = assignCards()

print(P1)
#print(P2)
#print(P3)
#print(P4)

def turn(Player, card):
    print(card)
    choice = int(input("Enter either 1, 2, or 3 to exchange the card or 0 to skip: "))
    if choice == 0:
        revDeck.append(card)
    else:
        Player = exchange(choice - 1, Player, card)
        print(Player)
        
def cost():
    pass

while len(deck) > 0:
    turn(Player = P1, card = pick())
    turn(Player = P2, card = pick())
    turn(Player = P3, card = pick())
    turn(Player = P4, card = pick())  
    break