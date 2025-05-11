# Wild Card Lets you see your own cards
# 9 of any color Lets you See the and Shuffle any opponent's cards
# 7 of any color Lets you swap your one card with any card of any opponent

import numpy
import random
import time
from typing import List  
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD  

cards = [
    "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "RRev", "RRev", "RSkip", "RSkip", "W+4",
    "G0", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "GRev", "GRev", "GSkip", "GSkip", "W+4",
    "B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "BRev", "BRev", "BSkip", "BSkip", "WC",
    "Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "YRev", "YRev", "YSkip", "YSkip", "WC"
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

def createDeck():
    random.shuffle(deck)
    return deck

revDeck = []

def cardVal(card):
    return card[1:len(card)]

def pick():
    card = random.randint(0, len(deck) - 1)
    return deck[card]

class BayesianAI:
    def __init__(self, allCards):
        self.allCards = allCards
        self.model = DiscreteBayesianNetwork()
        self.inference = None
        self.setupModel()
        
    def setupModel(self):
        slots = ['O1_C1', 'O1_C2', 'O1_C3']
        
        for slot in slots:
            self.model.add_node(slot)
        
        for slot in slots:
            cpd = TabularCPD(
                variable=slot,
                variable_card=len(self.allCards),
                values=[[1 / len(self.allCards)] for _ in self.allCards]
                # ⛔ DON'T pass state_names here!
            )
            self.model.add_cpds(cpd)
        
        self.inference = VariableElimination(self.model)
        
    def updateOnObservation(self, slot, card):
        values = []
        for c in self.allCards:
            values.append(0.99 if c == card else 0.01 / (len(self.allCards) - 1))

        cpd = TabularCPD(
            variable=slot,
            variable_card=len(self.allCards),
            values=[[v] for v in values]
        )
        self.model.remove_cpds(self.model.get_cpds(slot))
        self.model.add_cpds(cpd)
        self.inference = VariableElimination(self.model)

    def updateOnShuffle(self, slots):
        for slot in slots:
            cpd = TabularCPD(
                variable=slot,
                variable_card=len(self.allCards),
                values=[[1 / len(self.allCards)] for _ in self.allCards]
            )
            self.model.remove_cpds(self.model.get_cpds(slot))
            self.model.add_cpds(cpd)
        self.inference = VariableElimination(self.model)

    def getMostLikelyCards(self):
        mostLikely = {}
        for slot in ['O1_C1', 'O1_C2', 'O1_C3']:
            q = self.inference.map_query(variables=[slot])
            mostLikely[slot] = q[slot]
        return mostLikely

class AI:
    
    def __init__(self):
        self.hand = self.assignCards()
        self.memory = self.hand.copy()
        self.numTurns = 0
        self.shuffled = False
        self.playerCards = []
        self.other1Cards = []
        self.other2Cards = []
        self.rememberOtherCards = [0, 0, 0]
        self.cardDeck = createDeck()
        self.bayesAI = BayesianAI(self.cardDeck)
        
    def updateAIMemory(self, moveType, targetPlayer, seenCard = True):
        
        if moveType == 'swap':
            slot = '01_C1'
            self.bayesAI.updateOnObservation(slot, seenCard)
            
        elif moveType == 'shuffle':
            self.bayesAI.updateOnShuffle(['O1_C1', 'O1_C2', 'O1_C3'])
        
    def add(self, p, a1, a2):
        self.playerCards = p
        self.other1Cards = a1
        self.other2Cards = a2
        
    def assignCards(self):
        arr = []
        for i in range(3):
            card = random.randint(0, len(deck) - 1)
            arr.append(deck[card])
            deck.remove(deck[card])
        return arr
    
    def calculateHeuristic(self):
        idx = max(range(len(self.hand)), key=lambda i: weights[self.hand[i][1:]])
        return idx     
     
    def calculateWinning(self):
        summ = 0
        for card in self.hand:
            summ += weights[cardVal(card)]
            
        return summ
               
class Player:
    def __init__(self):
        self.hand = self.assignCards()
        
    def calculateWinning(self):
        summ = 0
        for card in self.hand:
            summ += weights[cardVal(card)]
            
        return summ    
    
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
        
        while True:
            try:
                myCard = int(input("Enter your card index to exchange (1-3): "))
                if 1 <= myCard <= 3:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid integer")

        while True:
            try:
                theirCard = int(input("Enter the AI's card index to take (1-3): "))
                if 1 <= theirCard <= 3:
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 3")
            except ValueError:
                print("Please enter a valid integer")
        
        self.hand[myCard - 1], bot.hand[theirCard - 1] = bot.hand[theirCard - 1], self.hand[myCard - 1]
        
        return self.hand, bot, (myCard - 1), (theirCard - 1)    
  
    def nine(self, player: AI):
        print(player)
        flag = 1
        while flag:
            flag = int(input("Enter 0 to skip or 1 to continue: "))
            if flag == 0:
                break
            else:
                num1 = int(input("Enter the card number you want to change: "))
                num2 = int(input("Enter the card number you want to change with: "))
                player.hand[num1 - 1], player.hand[num2 - 1] = player.hand[num2 - 1], player.hand[num1 - 1]
                
            print(player)
            
        return player
    
    def wild(self):
        print(self.hand)
    
    def playHuman(self, cardDrawn, bot1: AI, bot2: AI, bot3: AI):
        
        print(f"Card Drawn: {cardDrawn}")
        
        choice = int(input("Enter the card Number [1, 2, 3] to exchange with the card drawn or enter 0 to skip\n"))
        
        if choice != 0:
            
            card = self.hand[choice - 1]
            
            for i in range(len(self.hand)):
                if self.hand[i] == card:
                    self.hand[i] = cardDrawn
            
            cardDrawn = card
            
        print(f"Card Drawn for Check - {cardDrawn}")    
            
        if str(cardVal(cardDrawn)) == "7":
            
            botChoice = int(input("Enter the AI Bot Number [1, 2, 3] to want to exchange with"))
            
            if botChoice == 1:
                
                if bot2.rememberOtherCards[1] == 2:
                    
                    bot2.rememberOtherCards[1] = 1
                    
                if bot3.rememberOtherCards[1] == 2:
                    
                    bot3.rememberOtherCards[1] = 1
                
                self.hand, bot1, myCard, theirCard = self.seven(bot=bot1)
                
                bot2.playerCards[myCard], bot2.other1Cards[theirCard] = bot2.other1Cards[theirCard], bot2.playerCards[myCard]
                
                bot3.playerCards[myCard], bot3.other1Cards[theirCard] = bot3.other1Cards[theirCard], bot3.playerCards[myCard]

            elif botChoice == 2:
                
                if bot2.rememberOtherCards[1] == 2:
                    
                    bot2.rememberOtherCards[1] = 1
                    
                if bot3.rememberOtherCards[1] == 2:
                    
                    bot3.rememberOtherCards[1] = 1
                
                self.hand, bot2, myCard, theirCard = self.seven(bot=bot2)
                
                bot1.playerCards[myCard], bot1.other1Cards[theirCard] = bot1.other1Cards[theirCard], bot1.playerCards[myCard]
                
                bot3.playerCards[myCard], bot3.other2Cards[theirCard] = bot3.other2Cards[theirCard], bot3.playerCards[myCard]

            elif botChoice == 3:
                
                if bot1.rememberOtherCards[2] == 2:
                    
                    bot1.rememberOtherCards[2] = 1
                    
                if bot2.rememberOtherCards[2] == 2:
                    
                    bot2.rememberOtherCards[2] = 1
                
                self.hand, bot3, myCard, theirCard = self.seven(bot=bot3)
                
                bot1.playerCards[myCard], bot1.other2Cards[theirCard] = bot1.other2Cards[theirCard], bot1.playerCards[myCard]
                
                bot2.playerCards[myCard], bot3.other2Cards[theirCard] = bot3.other2Cards[theirCard], bot3.playerCards[myCard]
                
        elif str(cardVal(cardDrawn)) == "9":
            botChoice = int(input("Enter the AI Bot Number [1, 2, 3] to want to see & shuffle their cards"))
            
            if botChoice == 1:
                
                bot1.shuffled = True
                
                if bot2.rememberOtherCards[1] == 2:
                    
                    bot2.rememberOtherCards[1] = 1
                    
                if bot3.rememberOtherCards[1] == 2:
                    
                    bot3.rememberOtherCards[1] = 1
                    
                self.nine(player=bot1)
                
            elif botChoice == 2:
                
                bot2.shuffled = True
                
                if bot2.rememberOtherCards[1] == 2:
                    
                    bot2.rememberOtherCards[1] = 1
                    
                if bot3.rememberOtherCards[1] == 2:
                    
                    bot3.rememberOtherCards[1] = 1
                
                self.nine(player=bot2)
                
            elif botChoice == 3:
                
                bot3.shuffled = True
                
                if bot1.rememberOtherCards[2] == 2:
                    
                    bot1.rememberOtherCards[2] = 1
                    
                if bot2.rememberOtherCards[2] == 2:
                    
                    bot2.rememberOtherCards[2] = 1
                
                self.nine(player=bot3)

        elif str(cardVal(cardDrawn)) == "C":
            self.wild()

def cost(card):
    if isinstance(card, int):
        return card  # already a weight
    elif isinstance(card, str):
        return weights[cardVal(card)]
    else:
        raise ValueError(f"Unexpected card type: {type(card)}, value: {card}")
    
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
        
        for i in range(len(me.hand)):
            if me.hand[i] == card:
                me.hand[i] = cardDrawn
                
        for i in range(len(me.memory)):
            if me.memory[i] == card:
                me.memory[i] = cardDrawn
    
        cardDrawn = card
        
    if str(cardVal(cardDrawn)) == "7":
        print(f"me - {me.hand}")
        print(f"Player - {player.hand}")
        print(f"bot1 - {bot1.hand}")
        print(f"bot2 - {bot2.hand}")
        # choice = random.randint(1, 3)
        
        likely = me.bayesAI.getMostLikelyCards()
        
        targets = {
            1: [likely['O1_C1'], likely['O1_C2'], likely['O1_C3']],
            2: me.other1Cards, 
            3: me.other2Cards
        }
        
        choice = max(targets.items(), key=lambda item: max(cost(c) for c in item[1] if c is not None))[0]
        
        if choice == 1:
            cIdx = player.calculateHeuristic()
            me.hand, player.hand = sevenBot(bot=me, player=player, pIdx=choice - 1, changeIdx=cIdx)
            bot1.rememberOtherCards[0] = 1
            bot2.rememberOtherCards[0] = 1
        elif choice == 2:
            cIdx = bot1.calculateHeuristic()
            me.hand, bot1.hand = sevenBot(bot=me, player=bot1, pIdx=choice - 1, changeIdx=cIdx)
            bot2.rememberOtherCards[1] = 1
        elif choice == 3:
            cIdx = bot2.calculateHeuristic()
            me.hand, bot2.hand = sevenBot(bot=me, player=bot2, pIdx=choice - 1, changeIdx=cIdx)
            bot1.rememberOtherCards[2] = 1
            
        print(f"me - {me.hand}")
        print(f"Player - {player.hand}")
        print(f"bot1 - {bot1.hand}")
        print(f"bot2 - {bot2.hand}")
        
    elif str(cardVal(cardDrawn)) == "9":
        targets = {
            1: player.hand,
            2: bot1.hand,
            3: bot2.hand
        }

        choice = max(targets.items(), key=lambda item: max(cost(c) for c in item[1] if c is not None))[0]
        
        if choice == 1:
            player.hand = nineBot(me = me, player = player)
            me.playerCards = player.hand
            me.rememberOtherCards[0] = 2
            
        elif choice == 2:
            bot1.hand = nineBot(me = me, player = bot1)
            bot1.shuffled = True
            me.other1Cards = bot1.hand
            me.rememberOtherCards[1] = 2
            
        else:
            bot2.hand = nineBot(me = me, player = bot2)
            bot2.shuffled = True
            me.other2Cards = bot2.hand
            me.rememberOtherCards[2] = 2
        
    elif str(cardVal(cardDrawn)) == "C":
        wildBot(bot = me)
    
    me.numTurns += 1
    
def sevenBot(bot: AI, player, pIdx: int, changeIdx):  
    
    print(f"Bot Called 7 with - {pIdx}")
    
    remember1 = random.random() < 0.98
    remember2 = random.random() < 0.45
    
    idx = bot.calculateHeuristic()
    
    memory = []
    
    if bot.rememberOtherCards[pIdx] == 2:
        memory = player.hand.copy() if remember1 else random.sample(player.hand, len(player.hand))
            
    elif bot.rememberOtherCards[pIdx] == 1:
        memory = player.hand.copy() if remember2 else random.sample(player.hand, len(player.hand))
            
    else:
        memory = player.hand.copy()
        changeIdx = random.randint(0, 2)  
        
    myCard = bot.hand[idx]
    theirCard = memory[changeIdx]
    
    for i in range(len(bot.hand)):
        if bot.hand[i] == myCard:
            bot.hand[i] = theirCard
            break

    for i in range(len(player.hand)):
        if player.hand[i] == theirCard:
            player.hand[i] = myCard
            break
    
    return bot.hand, player.hand        
        
def nineBot(me: AI, player: AI):
    
    print("Bot Called 9")
    
    print(f"Before: {player.hand}")
    
    random.shuffle(player.hand)
    
    print(f"After: {player.hand}")

    me.memory = player.hand
            
    return player.hand

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

while True:
    
    last = pick()
    
    deck.remove(last)
    
    print(f"Card Drawn: {last} & Turn Off - {lastTurn}")    
    
    if len(deck) == 0:
        break
        
    if lastTurn == 1:
        print("Player - 1 Turn:")
        
        player.playHuman(bot1 = ai1, bot2 = ai2, bot3 = ai3, cardDrawn = last)
        
        print("\n")
        
        time.sleep(1.5)
        
    if len(deck) == 0:
        break
        
    if lastTurn == 2:
        playBot(me = ai1, player = player, bot1 = ai2, bot2 = ai3, cardDrawn = last)    
        
        print("\n")
        
        time.sleep(1.5)
        
    if len(deck) == 0:
        break
        
    if lastTurn == 3:
        playBot(me = ai2, player = player, bot1 = ai1, bot2 = ai3, cardDrawn = last) 
        
        print("\n")
        
        time.sleep(1.5)
        
    if len(deck) == 0:
        break
    
    if lastTurn == 4:
        playBot(me = ai3, player = player, bot1 = ai1, bot2 = ai2, cardDrawn = last)
        
        print("\n")
        
        time.sleep(1.5)
        
    lastTurn += 1
    if lastTurn > 4:
        lastTurn = 1
        
    print(f"Player - 1 Cards: {player.hand}")
    print(f"Player - 2 Cards: {ai1.hand}")
    print(f"Player - 3 Cards: {ai2.hand}")
    print(f"Player - 4 Cards: {ai3.hand}")
    
array = []

array.append(("Player", player.calculateWinning()))
array.append(("AI - 1", ai1.calculateWinning()))
array.append(("AI - 2", ai2.calculateWinning()))
array.append(("AI - 3", ai3.calculateWinning()))

array.sort(key=lambda x: x[1])

print(array)

print(f"{array[0][0]} Won the game with {array[0][1]} Weight Values")