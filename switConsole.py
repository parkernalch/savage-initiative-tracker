# SWINIT - Initiative Module
# Parker Nalchajian

from swchar import *
from swdeck import *
import os
import math

def dealTactician(character, deck, tact):
    if character.tactician:
        print(character.name + ': Roll Knowledge(Battle)')
        while True:
            try:
                roll = int(input())
                break
            except:
                continue
        success = math.floor(roll/4)
        #tacticianHand = deal(success, deck, discard)
        deal(success, deck, tact)
    return

def useTCard(card, tact, discard):
    if card in tact:
        discard.append(card)
        tact.remove(card)
    else:
        print('ERR: Bad Card Name')

def dealSW(Character, deck, discard):
    Character.hand.clear()

    num = 1
    if Character.lvlHead2:
        num = 3
    elif Character.lvlHead:
        num = 2
    else:
        num = 1
    hand = deal(num, deck, discard)

    if Character.quick:
        for i in range(len(hand)):
            while True:
                if cardToValue(hand[i]) < 6:
                    hand[i] = deal(1, deck, discard)[0]
                else:
                    break

    if Character.slowed and not Character.quickness:
        for i in range(len(hand)):
            while True:
                if cardToValue(hand[i]) >= 54:
                    break
                elif cardToValue(hand[i]) >= 11:
                    hand[i] = deal(1, deck, discard)[0]
                else:
                    break

    if Character.quickness and not Character.slowed:
        for i in range(len(hand)):
            while True:
                if cardToValue(hand[i]) < 8:
                    hand[i] = deal(1, deck, discard)[0]
                else:
                    break

    if Character.quickness and Character.slowed:
        for i in range(len(hand)):
            while True:
                if cardToValue(hand[i]) >= 54:
                    break
                elif cardToValue(hand[i]) >= 11 or cardToValue(hand[i]) < 8:
                    hand[i] = deal(1, deck, discard)[0]
                else:
                    break
    return hand

def initiative(combatDict, deck, discard):
    for char in combatDict.values():
        char.hand = dealSW(char, deck, discard)
        if char.quickness:
            if char.name in quickenTracker.keys():
                quickenTracker[char.name] = quickenTracker[char.name] + 1
            else:
                quickenTracker[char.name] = 1
        else:
            if char.name in quickenTracker.keys():
                quickenTracker.pop(char.name)

        if char.slowed:
            if char.name in slowTracker.keys():
                slowTracker[char.name] = slowTracker[char.name] + 1
            else:
                slowTracker[char.name] = 1
        else:
            if char.name in slowTracker.keys():
                slowTracker.pop(char.name)
                
    print(combatOrder(combatDict) + '\n')
    return combatOrder(combatDict)
        
        
def showHands(combatDict):
    for char in combatDict.values():
        char.hand = orderHand(char.hand)
        print(char.name + ': ', end='')
        print(char.hand)
    return

def combatOrder(combatDict):
    temp = {}
    store = []
    co = ''
    for char in combatDict.values():
        temp[char] = bestCard(char.hand)
        store.append(cardToValue(bestCard(char.hand)))
    store.sort(reverse=True)
    for cardVal in store:
        ch = list(temp.keys())[list(temp.values()).index(valueToCard(cardVal))]
        suffix = ''
        if ch.quickness:
            suffix += '(q' + str(int(quickenTracker[ch.name])) + ')'
        if ch.slowed:
            suffix += '(s' + str(int(slowTracker[ch.name])) + ')'
        co += ('\n' + valueToCard(cardVal) + ' | ' + ch.name + suffix)
    return co

def start():
    isWindows = True
    pcDict = initPC()
    combat = initPC()
    deck = buildDeck(True)
    discard = []
    tacticianCards = []
    Round = 1
    lastRound = []
    while True:
        if Round <= 1:
            print('Press ENTER to start combat')
            Round = 1
        elif Round > 1:
            print('Press ENTER to deal next round')

        ui = input()
        comm = ui.split(' ')[0]

        #END COMBAT: "end"
        if ui == 'end':
            reset(deck, discard, tacticianCards)
            print('type start() to begin new round')
            break

        #DEAL NEXT ROUND: ""
        elif ui == '':
            if isWindows:
                os.system('cls')
                
            if 'RJoker' in lastRound or 'BJoker' in lastRound:
                shuffle(deck, discard)

            lastRound.clear()

            hasTactician = False
            for ch in combat.values():
                if ch.tactician:
                    hasTactician = True
                    tact = ch
            if hasTactician and tact and Round == 1:
                dealTactician(tact, deck, tacticianCards)

            if isWindows:
                os.system('cls')

            if len(tacticianCards) > 0:
                print('Tactician Cards: ', end='')
                for card in tacticianCards:
                    print(card + ' ', end='')
                print('\n')

            print('======================')
            print('======= ROUND ' + str(Round) + ' =======')
            initiative(combat, deck, discard)
            print('======================')
            print('======================\n')

            Round += 1

        #USE TACTICIAN CARD: "u card"
        elif comm == 'u':
            tCard = ui.split(' ')[1].replace('h','♥').replace('H','♥').replace('c','♣').replace('C','♣').replace('d','♦').replace('D','♦').replace('s','♠').replace('S','♠')
            useTCard(tCard,tacticianCards, discard)

        #VIEW CHARACTER: "v fname"
        elif comm == 'v':
            fname = ui.split(' ')[1].lower()
            if fname == 'all' or fname == 'a':
                viewAll(combat)
            else:
                for ch in combat.values():
                    if ch.name.split(' ')[0].lower() == fname:
                        view(ch)

        #SLOW CHARACTER: "s fname"
        elif comm == 's':
            fname = ui.split(' ')[1].lower()
            for ch in combat.values():
                if ch.name.split(' ')[0].lower() == fname:
                    slow(ch)

        #QUICKEN CHARACTER: "q fname"
        elif comm == 'q':
            fname = ui.split(' ')[1].lower()
            for ch in combat.values():
                if ch.name.split(' ')[0].lower() == fname:
                    quicken(ch)

        #EDIT CHARACTER: "e fname"
        elif comm == 'e':
            fname = ui.split(' ')[1].lower()
            for ch in combat.values():
                if ch.name.split(' ')[0].lower() == fname:
                    edit(ch)
                    
        #ADD CHARACTER: "a [d/m] fname"
        elif comm == 'a':
            mod = ui.split(' ')[1].lower()
            if mod == 'd':
                #fname = ui.split(' ')[2].lower()
                fname = ui[4:len(ui)]
                addDefault(fname, combat)
            elif mod == 'm':
                newChars = []
                print('Add multiple characters:')
                while True:
                    name = input()
                    if name == '':
                        print('Press ENTER to submit')
                        temp = input()
                        if temp == '':
                            break
                        else:
                            newChars.append(temp)
                    else:
                        newChars.append(name)
                mAdd(newChars, combat)
            else:
                isPC = False
                fname = ui[2:len(ui)]
                for ch in pcDict.values():
                    if ch.name.split(' ')[0].lower() == fname.split(' ')[0].lower():
                        combat[fname] = ch
                        isPC = True
                if not isPC:        
                    add(fname, combat)

        #KILL CHARACTER: "k fname"
        elif comm == 'k':
            fname = ui.split(' ')[1].lower()
            for ch in combat.values():
                if ch.name.split(' ')[0].lower() == fname:
                    temp = ch
            if temp:
                combat.pop(fname)

        #PRINT ALL COMBATANTS: "p"
        elif comm == 'p':
            print('')
            for ch in combat.values():
                print(ch.name)
            print('')

        #VIEW HAND: "hd fname"
        elif comm == 'h':
            fname = ui.split(' ')[1].lower()
            print(hand(fname, combat))

        #PRINT QUICKENTRACKER
        elif comm == 'qt':
            for key in quickenTracker.keys():
                print(key + str(quickenTracker[key]))
                
        #PRINT SLOWTRACKER
        elif comm == 'st':
            for key in slowTracker.keys():
                print(key + str(slowTracker[key]))
                
        #PRINT HELP DIALOG: "h", "help", "HELP", "Help"
        elif comm == '?' or comm == 'help' or comm == 'HELP' or comm == 'Help':
            if isWindows:
                os.system('cls')
            print('==========================')
            print('ENTER ------------- Deal Next Round')
            print('"p" --------------- Print All Combatants')
            print('"end" ------------- End Combat')
            print('"v fname" --------- View Character')
            print('"a [d/m] fname" --- Add Character(s)')
            print('"e fname" --------- Edit Character')
            print('"k fname" --------- Kill Character')
            print('"s fname" --------- Slow Character')
            print('"q fname" --------- Quicken Character')
            print('"u card" ---------- Use Tactician Card')
            print('==========================')

        elif comm == 'reset':
            discard.clear()
            deck.clear()
            tacticianCards.clear()
            deck = buildDeck(True)
            print('Do you want to re-instantiate the combat list?\n')
            print('Current Roster:')
            for ch in combat.values():
                print(ch.name)
            print('')
            inp = yntf(input())
            if inp:
                combat.clear()
                combat = initPC()
            Round = 0
        else:
            continue

#################
##BUILD OBJECTS##
#################
PC = initPC()
combat = initPC()
deck = buildDeck(True)
discard = []
tacticianCards = []
#################
##END BUILD OBJ##
#################

## POWER TRACKERS ##
quickenTracker = {}
slowTracker = {}
####################
  
start()        
        
