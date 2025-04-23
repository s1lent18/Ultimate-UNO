import random
from typing import List    

cards = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RRev", "RSkip", "RSkip", "R+2", "R+2",
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GRev", "GSkip", "GSkip", "G+2", "G+2",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BRev", "BSkip", "BSkip", "B+2", "B+2",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YRev", "YSkip", "YSkip", "Y+2", "Y+2",
    "W+4", "W+4", "WC", "WC"
]

deck = cards.copy()

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
    "C": 10,
    "+4": 15,
    "+2": 18,
    "Rev": 20,
    "Skip": 20,
}

revDeck = []

def cardVal(card):
    return card[1:len(card)]

def pick():
    card = random.randint(0, len(deck) - 1)
    return deck[card]

class AI:
    def __init__(self):
        self.hand = self.assignCards()
        self.memory = self.hand.copy()
        self.numTurns = 0
        self.shuffled = False
        self.playerCards = []
        self.other1Cards = []
        self.other2Cards = []
        self.rememberOtherCards = [False, False, False]
        
    def add(self, p, a1, a2):
        self.playerCards = p
        self.other1Cards = a1
        self.other2Cards = a2
        
    def assignCards(self) -> List[int]:
        arr = []
        for i in range(3):
            card = random.randint(0, len(deck) - 1)
            arr.append(deck[card])
            deck.remove(deck[card])
        return arr
    
    def calculateHeuristic(self):
        idx = max(range(len(self.hand)), key=lambda i: weights[self.hand[i][1:]])
        return idx     
            
class Player:
    def __init__(self):
        self.hand = self.assignCards()
        
    def assignCards(self) -> List[int]:
        arr = []
        for i in range(3):
            card = random.randint(0, len(deck) - 1)
            arr.append(deck[card])
            deck.remove(deck[card])
        return arr
    
    def calculateHeuristic(self):
        idx = max(range(len(self.hand)), key=lambda i: weights[self.hand[i][1:]])
        return idx 
    
    def seven(self, bot: AI):
        
        myCard = int(input("Enter your card index you want to exchange"))
        
        theirCard = int(input("Enter the card of AI you want"))
        
        self.hand[myCard], bot.hand[theirCard] = bot.hand[theirCard], self.hand[myCard]
        
        return player, bot    
    
    def draw4(self, p2, p3, p4):
        temp = p1
        p1 = p2
        p2 = p3
        p3 = p4
        p4 = temp
        return p1, p2, p3, p4

    def nine(self, player):
        print(player)
        flag = 1
        while flag:
            flag = int(input("Enter 0 to skip or 1 to continue: "))
            if flag == 0:
                break
            else:
                num1 = int(input("Enter the card number you want to change: "))
                num2 = int(input("Enter the card number you want to change with: "))
                player[num1], player[num2] = player[num2], player[num1]
                
            print(player)
            
        return player
    
    def wild(self):
        print(self.hand)
    
    def playHuman(self, cardDrawn, bot1: AI, bot2: AI, bot3: AI):
        
        print(f"Card Drawn: {cardDrawn}")
        
        choice = int(input("Enter the card Number [1, 2, 3] to exchange with the card drawn or enter 0 to skip\n"))
        
        if choice != 0:
            
            card = self.hand[choice - 1]
            
            self.hand.remove(card)
            self.hand.append(cardDrawn)
            
            cardDrawn = card
            
            if str(cardVal(cardDrawn)) == "7":
                
                botChoice = int(input("Enter the AI Bot Number [1, 2, 3] to want to exchange with"))
                
                if botChoice == 1:
                    self.seven(bot=bot1)
                elif botChoice == 2:
                    self.seven(bot=bot2)
                elif botChoice == 3:
                    self.seven(bot=bot3)
                    
            elif str(cardVal(cardDrawn)) == "9":
                botChoice = int(input("Enter the AI Bot Number [1, 2, 3] to want to see & shuffle their cards"))
                
                if botChoice == 1:
                    bot1.shuffled = True
                    self.nine(player=bot1)
                elif botChoice == 2:
                    bot2.shuffled = True
                    self.nine(player=bot2)
                elif botChoice == 3:
                    bot3.shuffled = True
                    self.nine(player=bot3)

            elif str(cardVal(cardDrawn)) == "C":
                self.wild()

            elif str(cardVal(cardDrawn)) == "+4":
                self.hand, ai1.hand, ai2.hand, ai3.hand = self.draw4(p2 = ai1.hand, p3 = ai2.hand, p4 = ai3.hand)

def cost(card):
        temp = cardVal(card)
        retCost = weights[temp]
        return retCost      
    
def playBot(me: AI, player: Player, bot1: AI, bot2: AI, cardDrawn):
    
    if me.shuffled:
        remembers = random.random() < 0.5
    else:
        print(f"Number of Turns played by Now: {me.numTurns}")
        remembers = random.random() < (0.98 - (me.numTurns * 0.05))
        
    idx = me.calculateHeuristic()
    
    if cost(me.hand[idx]) > cost(cardDrawn):
    
        print(f"Hueristic Index: {idx}")
            
        memory = me.memory.copy() if remembers else random.sample(me.hand, len(me.hand))
        
        print(f"Memory: {memory}")
        
        card = me.hand[idx]
        
        print(f"Card: {card}")
    
        me.hand.remove(card)
        me.hand.append(cardDrawn)
        cardDrawn = card
        
    if str(cardVal(cardDrawn)) == "7":
        choice = random.randint(1, 3)
        
        if choice == 1:
            cIdx = player.calculateHeuristic()
        elif choice == 2:
            cIdx = bot1.calculateHeuristic()
        elif choice == 3:
            cIdx = bot2.calculateHeuristic()
        
        sevenBot(bot=me, player=choice, changeIdx=cIdx)
        
    elif str(cardVal(cardDrawn)) == "9":
        choice = random.randint(1, 3)
        nineBot(bot = me, player = choice)
        
    elif str(cardVal(cardDrawn)) == "C":
        wildBot(bot = me)
    
    me.numTurns += 1
    
def sevenBot(bot: AI, player, changeIdx):  
    
    print("Bot Called 7")
    
    remember = random.random() < 0.6
    
    idx = bot.calculateHeuristic()
    
    memory = []
    
    if player == 1:
            if bot.rememberOtherCards[0]:
                memory = bot.playerCards.copy() if remember else random.sample(bot.playerCards, len(bot.playerCards))
                
            else:
                memory = bot.playerCards.copy()
                changeIdx = random.randint(0, 3)
                
    elif player == 2:
        if bot.rememberOtherCards[1]:
            memory = bot.other1Cards.copy() if remember else random.sample(bot.other1Cards, len(bot.other1Cards))
            
        else:
            memory = bot.other1Cards.copy()
            changeIdx = random.randint(0, 3)
            
    elif player == 3:
        if bot.rememberOtherCards[2]:
            memory = bot.other2Cards.copy() if remember else random.sample(bot.other2Cards, len(bot.other2Cards))
            
        else:
            memory = bot.other2Cards.copy()
            changeIdx = random.randint(0, 3)       
        
    myCard = bot.hand[idx]
    theirCard = memory[changeIdx]
    
    bot.hand.remove(myCard)
    bot.hand.append(theirCard)
    
    memory.remove(theirCard)
    memory.append(myCard)
    
    if player == 1:
        bot.playerCards = memory
    elif player == 2:
        bot.other1Cards = memory
    elif player == 3:
        bot.other2Cards = memory
    
    return memory            
        
def nineBot(bot: AI, player):
    
    print("Bot Called 9")
    
    memory = []
    
    if player == 1:
        bot.rememberOtherCards[0] = True
        memory = bot.playerCards.copy()
    elif player == 2:
        bot.rememberOtherCards[1] = True
        memory = bot.other1Cards.copy()
    elif player == 3:
        bot.rememberOtherCards[2] = True
        memory = bot.other2Cards.copy()
    
    random.shuffle(memory)
    
    if player == 1:
        bot.playerCards = memory
    elif player == 2:
        bot.other1Cards = memory
    elif player == 3:
        bot.other2Cards = memory
            
    return memory 

def wildBot(bot: AI):
    bot.numTurns = 0
    bot.memory = bot.hand.copy()

player = Player()
ai1 = AI()
ai2 = AI()
ai3 = AI()

ai1.add(p = player.hand, a1 = ai2.hand, a2 = ai3.hand)
ai2.add(p = player.hand, a1 = ai1.hand, a2 = ai3.hand)
ai3.add(p = player.hand, a1 = ai1.hand, a2 = ai2.hand)

lastTurn = 1

print(f"Player - 1 Cards: {player.hand}")
print(f"Player - 2 Cards: {ai1.hand}")
print(f"Player - 3 Cards: {ai2.hand}")
print(f"Player - 4 Cards: {ai3.hand}")

while len(deck) > 0:
    
    last = pick()
    
    deck.remove(last)
    
    print(f"Card Drawn: {last}")
    
    if str(cardVal(last)) == "Skip":
        
        lastTurn = (lastTurn + 1) % 4
        
    print(f"Turn Off: {lastTurn}")
        
    if lastTurn == 1:
        print("Player - 1 Turn:")
        
        player.playHuman(bot1 = ai1, bot2 = ai2, bot3 = ai3, cardDrawn = last)
        
    if lastTurn == 2:
        playBot(me = ai1, player = player, bot1 = ai2, bot2 = ai3, cardDrawn = last)    
        
    if lastTurn == 3:
        playBot(me = ai2, player = player, bot1 = ai1, bot2 = ai3, cardDrawn = last) 
    
    if lastTurn == 4:
        playBot(me = ai3, player = player, bot1 = ai1, bot2 = ai2, cardDrawn = last)
        
    lastTurn += 1
    if lastTurn > 4:
        lastTurn = 1
        
    print(f"Player - 1 Cards: {player.hand}")
    print(f"Player - 2 Cards: {ai1.hand}")
    print(f"Player - 3 Cards: {ai2.hand}")
    print(f"Player - 4 Cards: {ai3.hand}")