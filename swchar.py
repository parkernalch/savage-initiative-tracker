# SWCHAR
# Parker Nalchajian

class Character:
    def __init__(self, name, isQuick, isLevelHeaded, isImpLevelHeaded, isTactician, isSlowed, isQuicknessed, hand):
        self.name = name
        self.quick = isQuick
        self.lvlHead = isLevelHeaded
        self.lvlHead2 = isImpLevelHeaded
        self.tactician = isTactician
        self.slowed = isSlowed
        self.quickness = isQuicknessed
        self.hand = hand

#BUILD PLAYER CHARACTERS
Sukorb = Character(
    'Sukorb Tsif',      #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    True,               #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Soombala = Character(
    'Soombala',         #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Vik = Character(
    'Vik Naraiya',      #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Garen = Character(
    'Garen Aldor',      #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Lydia = Character(
    'Lydia Na Valea',   #name
    True,               #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Klethic = Character(
    'Klethic Parnastalos',#name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Ardyn = Character(
    'Ardyn Durron',     #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

Cypher = Character(
    'Cypher Tosen',     #name
    False,              #quick
    False,              #lvlHead
    False,              #lvlHead2
    False,              #tactician
    False,              #slowed
    False,              #quickness
    [])                 #hand

# DICTIONARY STORAGE OF PLAYERS
def initPC():
    pcDict = {'sukorb':Sukorb,
          'soombala':Soombala,
          'vik':Vik,
          'garen':Garen,
          'lydia':Lydia,
          'klethic':Klethic,
          'ardyn':Ardyn,
          'cypher':Cypher}
    return pcDict

def combatFile():
    output = {}
    with open(r'C:/Python36/Personal/SW Initiative Tracker/loader.txt', 'r') as f:
        for line in f:
            #print(line)
            addFromString(line,output)
    return output

def tf_string(st):
    if st == 'True' or st == 'true' or st == 't' or st == 1:
        return True
    elif st == 'False' or st == 'false' or st == 'f' or st == 0:
        return False
    else:
        raise ValueError("cannot convert \"{}\" to a bool".format(st))
        
def addFromString(s,output):
    arr = s.split(',')
    if arr[0] == '' or arr[0] == '//' or arr[0] == '#':
        c = None
    elif len(arr) <= 1:
        c = Character(arr[0].rstrip("\n"),False,False,False,False,False,False,[])
        output[c.name] = c
    else:
        name = arr[0].rstrip("\n")
        quick = tf_string(arr[1].replace(' ','').replace('\n',''))
        lvlHead = tf_string(arr[2].replace(' ','').replace('\n',''))
        lvlHead2 = tf_string(arr[3].replace(' ','').replace('\n',''))
        tactician = tf_string(arr[4].replace(' ','').replace('\n',''))
        slowed=False
        quickness=False
        hand=[]
        c = Character(name,quick,lvlHead,lvlHead2,tactician,slowed,quickness,hand)
        output[c.name] = c

def slow(character):
    if character.slowed:
        character.slowed = False
        print(character.name + ' returns to NORMAL')
    else:
        character.slowed = True
        print(character.name + ' SLOWS down')

def quicken(character):
    if character.quickness:
        character.quickness = False
        print(character.name + ' returns to NORMAL')
    else:
        character.quickness = True
        print(character.name + ' SPEEDS UP')


def yntf(st):
    if st == 'y' or st == 'Y' or st == 'Yes' or st == 'yes' or st == 'YES' or st == 'true' or st == 'TRUE' or st == 'True':
        return True
    elif st == 'n' or st == 'N' or st == 'No' or st == 'no' or st == 'NO' or st == 'false' or st == 'FALSE' or st == 'False':
        return False
    else:
        return False
    
def add(name, dest):
    #print('add single character')
    print('is ' + name + ' quick?[Y/N]')
    quick = yntf(input())
    print('is ' + name + ' Level Headed?[Y/N]')
    lvlHead = yntf(input())
    if lvlHead:
        print('is ' + name + ' Improved Level Headed?[Y/N]')
        lvlHead2 = yntf(input())
    else:
        lvlHead2 = False
    print('is ' + name + ' a Tactician?[Y/N]')
    tactician = yntf(input())
    dest[name] = Character(name, quick, lvlHead, lvlHead2, tactician, False, False, [])
    return dest

def mAdd(li, dest):
    #print('add multiple character')
    for name in li:
        addDefault(name, dest)
    return dest
    
def addDefault(name, dest):
    #print('add character with all False flags')
    dest[name.split(' ')[0].lower()] = Character(name, False, False, False, False, False, False, [])
    return dest

def edit(character):
    view(character)
    print('Which would you like to change?')
    print('\t1 - Quick')
    print('\t2 - Level Headed')
    print('\t3 - Improved Level Headed')
    print('\t4 - Tactician')
    while True:
        choice = input()
        if choice == '1':
            if character.quick:
                character.quick = False
            else:
                character.quick = True
            break
        elif choice == '2':
            if character.lvlHead:
                character.lvlHead = False
            else:
                character.lvlHead = True
            break
        elif choice == '3':
            if character.lvlHead2:
                character.lvlHead2 = False
            else:
                character.lvlHead2 = True
            break
        elif choice == '4':
            if character.tactician:
                character.tactician = False
            else:
                character.tactician = True
            break
        else:
            print('ERR: Bad input. Try again')
            continue

def hand(name, dest):
    for ch in dest.values():
        if ch.name.split(' ')[0].lower() == name:
            temp = ch
        else:
            continue
    return temp.hand

def view(Character):
    print(Character.name)
    print('\tQuick: ' + str(Character.quick))
    print('\tLevel Headed: ' + str(Character.lvlHead))
    print('\tImp. Level Headed: ' + str(Character.lvlHead2))
    print('\tTactician: ' + str(Character.tactician))
    print('\tSlowed: ' + str(Character.slowed))
    print('\tQuickness: ' + str(Character.quickness))
    print('\tHand: ',end='')
    print(Character.hand)

def viewAll(pcDict):
    for ch in pcDict.values():
        view(ch)
        print('')
