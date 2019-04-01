# pydeck - The Playing Card Module
# Parker Nalchajian

from random import randint
#from swchar import *

suits = {'♣':0.2,'♦':0.4,'♥':0.6,'♠':0.8}
values = {'A':14, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
          '8':8, '9':9, 'T':10, 'J':11, 'Q':12, 'K':13}
jokers = {'BJoker':54, 'RJoker':54}

def buildDeck(includeJokers):
    deckListObj = []
    for obj in suits:
        for val in values:
            deckListObj.append(val + obj)
    if includeJokers:
        for j in jokers:
            deckListObj.append(j)
    return deckListObj

def deal(num, deckListObj, discardListObj):
    handList = []
    for i in range(num):
        if len(deckListObj) <= 1:
            shuffle(deckListObj, discardListObj)
            
        rand = randint(1,len(deckListObj) - 1)
        handList.append(deckListObj[rand])
        discardListObj.append(deckListObj[rand])
        del deckListObj[rand]    
        
    return handList
        
def shuffle(deckListObj, discardListObj):
    for card in discardListObj:
        deckListObj.append(card)
    discardListObj.clear()
    return deckListObj

def bestCard(handObj):
    temp = []
    for card in handObj:
        temp.append(cardToValue(card))
    best = max(temp)
    bcard = valueToCard(best)
    return bcard

def cardToValue(card):
    if card == 'BJoker':
        value = 55
    elif card == 'RJoker':
        value = 54
    else:
        value_1 = values[card[:1]]
        value_2 = suits[card[-1:]]
        value = value_1 + value_2
    return value

def valueToCard(value):
    if value == 54:
        card = 'RJoker'
    elif value == 55:
        card = 'BJoker'
    else:
        temp = str(value).split('.')
        num = list(values.keys())[list(values.values()).index(int(temp[0]))]
        suit = list(suits.keys())[list(suits.values()).index(float('0.' + temp[1]))]
        card = num + suit
    return card
        
def disCard(num, deckListObj, discardListObj):
    for i in range(num):
        if len(deckListObj) <= 1:
            shuffle(deckListObj, discardListObj)
            
        rand = randint(1,len(deckListObj) - 1)
        discardListObj.append(deckListObj[rand])
        del deckListObj[rand]
    return

def orderHand(hand):
    for i in range(len(hand)):
        hand[i] = cardToValue(hand[i])
    hand.sort(reverse=True)
    for j in range(len(hand)):
        hand[j] = valueToCard(hand[j])
    return hand

def reset(deck, discard, tacticianCards):
    discard.clear()
    deck.clear()
    tacticianCards.clear()
    deck = buildDeck(True)
    if len(discard) == 0 and len(tacticianCards) == 0 and len(deck) == 54:
        return True
    else:
        return False
    
####################################

