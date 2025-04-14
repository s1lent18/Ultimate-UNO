import random
from typing import List

cards = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RRev", "RSkip", "RSkip", "R+2", "R+2"
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GRev", "GSkip", "GSkip", "G+2", "G+2",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BRev", "BSkip", "BSkip", "B+2", "B+2",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YRev", "YSkip", "YSkip", "Y+2", "Y+2",
    "W+4", "W+4", "WJ", "WJ"
]

deck = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RRev", "RSkip", "RSkip", "R+2", "R+2"
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GRev", "GSkip", "GSkip", "G+2", "G+2",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BRev", "BSkip", "BSkip", "B+2", "B+2",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YRev", "YSkip", "YSkip", "Y+2", "Y+2",
    "W+4", "W+4", "WJ", "WJ"
]

weights = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "+2": 18,
    "Rev": 20,
    "Skip": 20,
    "+4": 15,
    "J": 10
}

# Draw 4 acts as a turnable
# Skip Lets you skip your turn
# Wild Card Lets you see your own cards
# Reverse Lets you Reverse any power-up applied on you
# 9 of any color Lets you See the and Shuffle any opponent's cards
# 7 of any color Lets you swap your one card with any card of any opponent

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

def exchange(num, player, card):
    old = player[num]
    revDeck.append(player[num])
    player[num] = card
    return player, old

P1 = assignCards()
P2 = assignCards()
P3 = assignCards()
P4 = assignCards()

def printall(P1, P2, P3, P4):
    print(P1)
    print(P2)
    print(P3)
    print(P4)

def draw4(p1, p2, p3, p4):
    temp = p1
    p1 = p2
    p2 = p3
    p3 = p4
    p4 = temp
    return p1, p2, p3, p4

def reverse():
    return True

def wild(player):
    print(player)

def nine(player):
    print(player)
    flag = int(input("Enter 0 to skip or 1 to continue: "))
    print(player)
    while flag:
        print(player)
        if flag == 0:
            break
        else:
            num1 = int(input("Enter the card number you want to change: "))
            num2 = int(input("Enter the card number you want to change with: "))
            player[num1], player[num2] = player[num2], player[num1]
            
    return player

def seven(player, exchange, myCard, theirCard):
    player[myCard], exchange[theirCard] = exchange[theirCard], player[myCard]
    print(player)
    print(exchange)
    
    return player, exchange    

def turn(Player, card):
    print(card)
    choice = int(input("Enter either 1, 2, or 3 to exchange the card or 0 to skip: "))
    if choice == 0:
        revDeck.append(card)
    else:
        Player, card = exchange(choice - 1, Player, card)
        print(Player)
    return card
        
def cost():
    pass

def lastcard(card):
    return card[1:len(card)]


last = ""

flag1 = False
flag2 = False

while len(deck) > 0:
    printall(P1, P2, P3, P4)
    if str(lastcard(last)) == "Skip" or flag2:
        
        print("Turn of Player 2")      
        
        last = turn(Player = P2, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P2, P1 = seven(P2, P1, int(me), int(card))
            elif change == "3":
                P2, P3 = seven(P2, P3, int(me), int(card))
            elif change == "4":
                P2, P4 = seven(P2, P4, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "3":
                P3 = nine(P3)
            elif changePlayer == "4":
                P4 = nine(P4)       
                
        flag1 = True
        flag2 = False
    else:
        print("Turn of Player 1")
        
        last = turn(Player = P1, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "2":
                P1, P2 = seven(P1, P2, int(me), int(card))
            elif change == "3":
                P1, P3 = seven(P1, P3, int(me), int(card))
            elif change == "4":
                P1, P4 = seven(P1, P4, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "2":
                P2 = nine(P2)
            elif changePlayer == "3":
                P3 = nine(P3)
            elif changePlayer == "4":
                P4 = nine(P4)
                
    if str(lastcard(last)) == "Skip" or flag1:
        
        print("Turn of Player 3")
        
        last = turn(Player = P3, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P3, P1 = seven(P3, P1, int(me), int(card))
            elif change == "2":
                P3, P2 = seven(P3, P2, int(me), int(card))
            elif change == "4":
                P3, P4 = seven(P3, P4, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "2":
                P2 = nine(P2)
            elif changePlayer == "4":
                P4 = nine(P4)       
        
        flag2 = True
        flag1 = False
    else:
        print("Turn of Player 2")
        
        last = turn(Player = P2, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P2, P1 = seven(P2, P1, int(me), int(card))
            elif change == "3":
                P2, P3 = seven(P2, P3, int(me), int(card))
            elif change == "4":
                P2, P4 = seven(P2, P4, int(me), int(card))
        
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "3":
                P3 = nine(P3)
            elif changePlayer == "4":
                P4 = nine(P4)
                
    if str(lastcard(last)) == "Skip" or flag2:
        
        print("Turn of Player 4")
        
        last = turn(Player = P4, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P4, P1 = seven(P4, P1, int(me), int(card))
            elif change == "2":
                P4, P2 = seven(P4, P2, int(me), int(card))
            elif change == "3":
                P4, P3 = seven(P4, P3, int(me), int(card))
        
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "2":
                P2 = nine(P2)
            elif changePlayer == "3":
                P3 = nine(P3)
        
        flag2 = False
        flag1 = True
    else:
        print("Turn of Player 3")
        
        last = turn(Player = P3, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P3, P1 = seven(P3, P1, int(me), int(card))
            elif change == "2":
                P3, P2 = seven(P3, P2, int(me), int(card))
            elif change == "4":
                P3, P4 = seven(P3, P4, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "2":
                P2 = nine(P2)
            elif changePlayer == "4":
                P4 = nine(P4)
                
    if str(lastcard(last)) == "Skip" or flag1:
        
        print("Turn of Player 1")
        
        last = turn(Player = P1, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "2":
                P1, P2 = seven(P1, P2, int(me), int(card))
            elif change == "3":
                P1, P3 = seven(P1, P3, int(me), int(card))
            elif change == "4":
                P1, P4 = seven(P1, P4, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "2":
                P2 = nine(P2)
            elif changePlayer == "3":
                P3 = nine(P3)
            elif changePlayer == "4":
                P4 = nine(P4)
        
        flag1 = False
        flag2 = True      
    else:
        
        print("Turn of Player 4")
        
        last = turn(Player = P4, card = pick())
        
        print(lastcard(last))
        
        if str(lastcard(last)) == "7":
            change = input("Enter the Player number whom you want to change with: ")
            me = input("Enter the card Index you want to change: ")
            card = input("Enter the card Index you want to change with: ")
            
            if change == "1":
                P4, P1 = seven(P4, P1, int(me), int(card))
            elif change == "2":
                P4, P2 = seven(P4, P2, int(me), int(card))
            elif change == "3":
                P4, P3 = seven(P4, P3, int(me), int(card))
                
        elif str(lastcard(last)) == "9":
            changePlayer = str(input("Enter the number of the player you want to see and shuffle the card of: "))
            if changePlayer == "1":
                P1 = nine(P1)
            elif changePlayer == "2":
                P2= nine(P2)
            elif changePlayer == "3":
                P3 = nine(P3)        
    
    printall(P1, P2, P3, P4)
        
    break