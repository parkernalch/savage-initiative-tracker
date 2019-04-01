#SAVAGE WORLDS INITIATIVE TRACKER
#PARKER NALCHAJIAN

from tkinter import *
from swinit import *

global Round
Round = 0

class MainWindow(Frame):

    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        Grid.rowconfigure(self, 0, weight=0)
        Grid.rowconfigure(self, 1, weight=1)
        Grid.rowconfigure(self, 2, weight=0)
        Grid.rowconfigure(self, 3, weight=0)
        Grid.columnconfigure(self,0,weight=1)

        ############
        #TOP | ROW=0
        TOP = Frame(self,bg='red')
        self.TOP = TOP
        TOP.grid(row=0,column=0,sticky=NSEW)
        Grid.rowconfigure(TOP,0,weight=0)
        Grid.columnconfigure(TOP,0,weight=1)
        Grid.columnconfigure(TOP,1,weight=0)

        rdLbl = Label(TOP,text="ROUND #",bg='black',fg='gray')
        rdLbl.grid(row=0,column=0,sticky=NSEW)

        addBtn = Button(TOP,text="+",bg='black',fg='white',command=self.addOne)
        addBtn.grid(row=0,column=1,sticky=NSEW)

        ############
        #MID | ROW=1
        MID = Frame(self)
        self.MID = MID
        MID.grid(row=1,sticky=NSEW)
        Grid.columnconfigure(MID,0,weight=0)
        Grid.columnconfigure(MID,1,weight=1)
        Grid.columnconfigure(MID,2,weight=0)

        startFrame = combatPicker(MID)
        startFrame.grid(row=0,column=0,columnspan=3,sticky=NSEW)

        ############
        #SPC | ROW=2
        SPC = Frame(self,bg='black',height=2)
        self.SPC = SPC
        SPC.grid(row=2,sticky=NSEW)

        ############
        #BTM | ROW=3
        BTM = Frame(self,bg='green')
        self.BTM = BTM
        BTM.grid(row=3,sticky=NSEW)  
        Grid.rowconfigure(BTM,0,weight=1)
        Grid.columnconfigure(BTM,0,weight=1)
        Grid.columnconfigure(BTM,1,weight=0)

        def dealCmd():
            self.DEAL(combat,deck,discard,Round)
        def dealEvent(event):
            self.DEAL(combat,deck,discard,Round)

        dealBtn = Button(BTM,text="DEAL",bg='red',fg='white',command=dealCmd)
        dealBtn.grid(row=0,column=1,sticky=NSEW)

        self.master.bind('<Return>',dealEvent)

        #TAC | BTM R0 C0
        TAC = Frame(BTM,bg='black')
        self.TAC = TAC
        TAC.grid(row=0,column=0,sticky=NSEW)

    def DEAL(self, pcDict, deckobj, discobj, rd):
        ##Deal cards to turn order items
        if rd == 0:
            ##roundZero includes logic for Tacticians if present
            self.roundZero(pcDict,deckobj,discobj)
        else:    
            r=0
            ## The below checks whether Jokers were dealt last hand
            if 'BJoker' in discobj or 'RJoker' in discobj:
                shuffle(deckobj,discobj)

            ## Builds each character's hand with the dealSW function
            for ch in pcDict.values():
                ch.hand = dealSW(ch,deckobj,discobj)

                ##Here, we visually track which round quickness is on
                if ch.quickness:
                    if ch.name in quickenTracker.keys():
                        quickenTracker[ch.name] = quickenTracker[ch.name] + 1
                    else:
                        quickenTracker[ch.name] = 1
                else:
                    if ch.name in quickenTracker.keys():
                        quickenTracker.pop(ch.name)
                        
                ##Here, we visually track which round slow is on        
                if ch.slowed:
                    if ch.name in slowTracker.keys():
                        slowTracker[ch.name] = slowTracker[ch.name] + 1
                    else:
                        slowTracker[ch.name] = 1
                else:
                    if ch.name in slowTracker.keys():
                        slowTracker.pop(ch.name)
                        
            temp = {}
            store = []

            ##for each character, add their best card to temp dict
            ##and add the value to store arraylist
            for ch in pcDict.values():
                temp[ch] = bestCard(ch.hand)
                store.append(cardToValue(bestCard(ch.hand)))

            ##sort the arraylist from largest to smallest value
            store.sort(reverse=True)

            ##Clear the self.MID frame to avoid duplication of killed characters
            for widget in self.MID.winfo_children():
                widget.destroy()
                
            ##in the newly sorted store arraylist, read back the
            ##combat order by looking up each value in the temp dict
            for cardVal in store:
                ch = list(temp.keys())[list(temp.values()).index(valueToCard(cardVal))]
                self.addCombatObj(ch,ch.hand,r)
                r += 1

            ##advance the initiative round and update the round label
            self.advance()

    def tacDeal(self, deckobj,tacthand,entryobj):
        ##If the entry object has a number in it, store the int value
        try:
            s = int(entryobj.get())
        ##If not, store a zero
        except:
            s = 0

        ##Calculate Successes based on the knowledge(battle) roll
        success = math.floor(s/4)

        ##Deal cards into tacthand in accordance with num of successes
        deal(success,deckobj,tacthand)

        ##Add the new tactician cards to the TAC frame
        self.tacAdd(tacthand)

        ##Get rid of the entry object and labels/buttons
        self.clearMidframe()
        

    def tacUse(self,card, hand):        
        ##Remove the used tactician card
        ##and re-add the new hand to TAC
        
        hand.remove(card)
        self.tacAdd(hand)

    def tacAdd(self,handobj):
        ##Clear widgets from TAC window
        for widget in self.TAC.winfo_children():
            widget.destroy()
            
        ##For each card still in hand, add it to TAC
        for i in range(len(handobj)):
            card = Button(self.TAC,text=handobj[i],command= lambda i=i: self.tacUse(handobj[i],handobj))
            card.pack(side=LEFT,fill=BOTH,expand=1)

    def roundZero(self,pcDict,deckobj,discobj):
        ##begin tactician checker
        tact = False
        character = None

        ##if a character in pcDict has tactician, send character and tact=True
        for ch in pcDict.values():
            if ch.tactician:
                tact=True
                character = ch
                break

        ##If character is non-NoneType (i.e. there was a tactician)
        ## proceed with the tactician deal
        if character:
            name = Label(self.MID,text=character.name,fg='gray')
            name.grid(row=0,column=0,columnspan=3,sticky=NSEW)
            
            label = 'Roll Knowledge(Battle)'
            prompt = Label(self.MID,text=label,fg='gray')
            prompt.grid(row=1,column=0,columnspan=3,sticky=NSEW)

            entry = Entry(self.MID)
            entry.grid(row=2,column=0,columnspan=3,sticky=NSEW)
            entry.focus_set()
            
            def go_enter(event):
                self.tacDeal(deck,tacticianCards,entry)
                self.DEAL(combat,deck,discard,1)

            def goclick():
                self.tacDeal(deck,tacticianCards,entry)
                self.DEAL(combat,deck,discard,1)
            
            entry.bind('<Return>',go_enter)
            
            submit = Button(self.MID,text='-- GO --',command=goclick)
            submit.grid(row=3,column=0,columnspan=3,sticky=NS)
        ##If no tactician, advance the round and deal round 1 as usual
        else:
            self.advance()
            self.DEAL(pcDict,deckobj,discobj,1)
            
    def advance(self):
        ##Update the round counter at the top
        ##and increment the global Round variable
        global Round
        
        #txt = 'ROUND ' + str(Round)
        txt = 'ROUND {}'.format(Round)
        #print(txt)
        rdLbl = Label(self.TOP,text=txt,fg='gray',bg='black')
        #rdLbl = Label(self.TOP,text='ROUND X')
        rdLbl.grid(row=0,column=0,sticky=NSEW)

        Round+=1

    def clearMidframe(self):
        ##Destroy each widget present in the MID frame
        for widget in self.MID.winfo_children():
            widget.destroy()

    def displayHand(self, hand,btn):
        ##Create menu object that we'll fill with cards
        #menu = Menu(root, tearoff=0)
        menu = Menu(self, tearoff=0)

        ##Fill menu with buttons corresponding to each card in hand
        for card in hand:
            menu.add_command(label=card)
            
        ##Show the menu at the pointer position when button is clicked 
        menu.post(root.winfo_pointerx(), root.winfo_pointery())

    def addCombatObj(self, Char, hand, rw):
        ##Adds Ternary object to MID frame at row rw
        ##declares local lbl string with the best card in the Char's hand
        lbl = bestCard(hand)

        ##Color handler. If red card, red label. If black card, black label.
        ##If joker, use special formatting
        if lbl[-1:] == '♥' or lbl[-1:]=='♦':
            coBtn = Button(self.MID,text=lbl,fg='red',relief=FLAT,command=lambda: self.displayHand(Char.hand,coBtn))
        elif lbl[-1:]=='♣' or lbl[-1:]=='♠':
            coBtn = Button(self.MID,text=lbl,fg='black',relief=FLAT,command=lambda: self.displayHand(Char.hand,coBtn))
        elif lbl == 'RJoker':
            coBtn = Button(self.MID,text=lbl,fg='white',bg='red',relief=FLAT,command=lambda: self.displayHand(Char.hand,coBtn))
        else:
            coBtn = Button(self.MID,text=lbl,fg='white',bg='black',relief=FLAT,command=lambda: self.displayHand(Char.hand,coBtn))
        coBtn.grid(row=rw,column=0,sticky=NSEW)

        ##NameLabel stores the Character's name in full.
        nmLbl = Label(self.MID,text=Char.name,fg='black')

        ##Effect Handler. Slowed (s), Quickened (q), and both (qs)
        if Char.slowed and not Char.quickness:
            nmLbl = Label(self.MID,text='*'+Char.name+' (s' + str(slowTracker[Char.name]) +')')
        if Char.quickness and not Char.slowed:
            nmLbl = Label(self.MID,text='*'+Char.name+' (q' + str(quickenTracker[Char.name]) + ')')
        if Char.quickness and Char.slowed:
            nmLbl = Label(self.MID,text='**'+Char.name+' (q' + str(quickenTracker[Char.name]) + 's' + str(slowTracker[Char.name]) + ')')
        nmLbl.grid(row=rw,column=1,sticky=NSEW)

        def qs(event):
            fname = Char.name.split(' ')[0].lower()
            ##Create menu object that we'll fill with character options
            qskM = Menu(self, tearoff=0)

            ##Fill menu with buttons corresponding to each option
            qskM.add_command(label='Slow',command=lambda:slow(Char))
            qskM.add_command(label='Quicken',command=lambda:quicken(Char))
            ##qskM.add_command(label='Kill',command=lambda:combat.pop(fname))
                    
            ##Show the menu at the pointer position when button is clicked 
            qskM.post(root.winfo_pointerx(), root.winfo_pointery())
            
        nmLbl.bind('<Button-3>',qs)
        
        ##Settings Button
        ##Will Bring up character edit window
        ##################################################################
        ##################################################################
        stBtn = Button(self.MID,text='⋮',relief=FLAT,command=lambda : self.charWindow(Char))
        stBtn.grid(row=rw,column=2,sticky=NSEW)
        ##################################################################
        ##################################################################

    def pt(self, txt):
        print(txt)

    def charWindow(self,character):
        ##the restore dictionary will keep the original values of the
        ##character object for the life of the charWindow. If user cancels window,
        ##these values will be inserted back into the character so no change happens

        ##in the below, restore[] = restore[] is used to make sure the initial values
        ##remain intact instead of updating each time the character object is updated
        restore = {}
        restore['name'] = character.name
        restore['name'] = restore['name']
        restore['quick'] = character.quick
        restore['quick'] = restore['quick']
        restore['lvlHead'] = character.lvlHead
        restore['lvlHead'] = restore['lvlHead']
        restore['lvlHead2'] = character.lvlHead2
        restore['lvlHead2'] = restore['lvlHead2']
        restore['tactician'] = character.tactician
        restore['tactician'] = restore['tactician']

        ##instantiate the new window with a border of 5px
        win = Toplevel(bd=5)
        Grid.rowconfigure(win,0,weight=1)
        Grid.rowconfigure(win,1,weight=0)
        Grid.rowconfigure(win,2,weight=0)
        Grid.columnconfigure(win,0,weight=1)
        Grid.columnconfigure(win,1,weight=1)
        
        edit = EditCharacter(win,character).grid(row=0,column=0,columnspan=2,sticky=NSEW)
        spacer = Frame(win,height=10).grid(row=1,column=0,columnspan=2,sticky=NSEW)

        ##on cancel write back the restore[] values into the character object before destroying
        ##the edit window
        def cancel_click():
            character.name = restore['name']
            character.quick = restore['quick']
            character.lvlHead = restore['lvlHead']
            character.lvlHead2 = restore['lvlHead2']
            character.tactician = restore['tactician']
            win.destroy()

        def return_save(event):
            win.destroy()
            
        win.bind('<Return>',return_save)
            
        cancel = Button(win,text='CANCEL',command=cancel_click).grid(row=2,column=0,sticky=NSEW)
        save = Button(win,text='SAVE',command=win.destroy).grid(row=2,column=1,sticky=NSEW)

        def kill_click():
            fname = character.name.split(' ')[0].lower()
            combat.pop(fname)
            win.destroy()
        
        kill = Button(win,text='KILL',command=kill_click,bg='gray',fg='white').grid(row=3,column=0,columnspan=2,sticky=NSEW)

    def addOne(self):
        c = Character('New Combatant',False,False,False,False,False,False,[])
        addMaster = Toplevel(bd=5)
        Grid.rowconfigure(addMaster,0,weight=1)
        Grid.rowconfigure(addMaster,1,weight=0)
        Grid.rowconfigure(addMaster,2,weight=0)
        Grid.columnconfigure(addMaster,0,weight=1)
        Grid.columnconfigure(addMaster,1,weight=1)

        add = EditCharacter(addMaster,c).grid(row=0,column=0,columnspan=2,sticky=NSEW)
        spacer = Frame(addMaster,height=10).grid(row=1,column=0,columnspan=2,sticky=NSEW)

        def add_cancel():
            addMaster.destroy()

        def add_save():
            first = c.name.split(' ')[0].lower
            combat[first] = c
            addMaster.destroy()

        cancel = Button(addMaster,text='CANCEL',command=add_cancel).grid(row=2,column=0,sticky=NSEW)
        save = Button(addMaster,text='SAVE',command=add_save).grid(row=2,column=1,sticky=NSEW)

        def sav(event):
            add_save()

        addMaster.bind('<Return>',sav)

class EditCharacter(Frame):
    def __init__(self, master, character):
        
        Frame.__init__(self,master)
        Grid.rowconfigure(self, 0,weight=0)
        Grid.rowconfigure(self, 1,weight=1)
        Grid.rowconfigure(self, 2,weight=1)
        Grid.rowconfigure(self, 3,weight=1)
        Grid.rowconfigure(self, 4, weight=1)
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self,0,weight=1)
        Grid.columnconfigure(self,1,weight=0)
        Grid.columnconfigure(self,2,weight=0)

        def callback(*args):
            updateCharacter()
            ##printChar(character)

        ##Name tk.StringVar()
        self.nm = StringVar()
        self.nm.set(character.name)
        self.nm.trace('w',callback)

        ##Quick tk.BooleanVar()
        self.qk = BooleanVar()
        self.qk.set(character.quick)

        ##Lvl Headed tk.BooleanVar()
        self.lv1 = BooleanVar()
        self.lv1.set(character.lvlHead)

        ##lvl Headed 2 tk.BooleanVar()
        self.lv2 = BooleanVar()
        self.lv2.set(character.lvlHead2)

        ##Tactician tk.BooleanVar()
        self.tc = BooleanVar()
        self.tc.set(character.tactician)
        
        txt = 'EDIT ' + character.name
        lbl = Label(self,text=txt).grid(row=0,column=0,columnspan=3,sticky=NSEW)

        nmLbl = Label(self,text='NAME:').grid(row=1,column=0,sticky=W)
        qkLbl = Label(self,text='QUICK:').grid(row=2,column=0,sticky=W)
        lv1Lbl = Label(self,text='LEVEL HEADED:').grid(row=3,column=0,sticky=W)
        lv2Lbl = Label(self,text='IMP. LVL HEADED:').grid(row=4,column=0,sticky=W)
        tcLbl = Label(self,text='TACTICIAN:').grid(row=5,column=0,sticky=W)

        nmEnt = Entry(self,textvariable=self.nm)
        nmEnt.grid(row=1,column=1,columnspan=2,sticky=EW)
        nmEnt.focus_set()
        nmEnt.selection_range(0,END)
        
        ## Method for printing character attributes (used solely for testing)
        def printChar(character):
            print('Name: ' + character.name)
            print('\tQuick: ' + str(character.quick))
            print('\tLevel Headed: ' + str(character.lvlHead))
            print('\tImproved Level Headed: ' + str(character.lvlHead2))
            print('\tTactician: ' + str(character.tactician))

        ##Method for updating the character to the values present in the new window
        def updateCharacter():
            character.name = self.nm.get()
            character.quick = self.qk.get()
            character.lvlHead = self.lv1.get()
            character.lvlHead2 = self.lv2.get()
            character.tactician = self.tc.get()
            #printChar(character)
            
        ##QUICK RADIO BUTTON
        qkYes = Radiobutton(self,text='YES',variable=self.qk,value=True,indicatoron=0,command=updateCharacter).grid(row=2,column=1,sticky=EW)
        qkNo = Radiobutton(self,text='NO',variable=self.qk,value=False,indicatoron=0,command=updateCharacter).grid(row=2,column=2,sticky=EW)

        def lv1callback():
            if character.lvlHead:
                character.lvlHead = False
            else:
                character.lvlHead = True
            printChar(character)

        ##LEVEL HEADED RADIO BUTTON    
        lv1Yes = Radiobutton(self,text='YES',variable=self.lv1,value=True,indicatoron=0,command=updateCharacter).grid(row=3,column=1,sticky=EW)
        lv1No = Radiobutton(self,text='NO',variable=self.lv1,value=False,indicatoron=0,command=updateCharacter).grid(row=3,column=2,sticky=EW)

        def lv2callback():
            if character.lvlHead2:
                character.lvlHead2 = False
            else:
                character.lvlHead2 = True
            printChar(character)

        ##IMPROVED LEVEL HEADED RADIO BUTTON    
        lv2Yes = Radiobutton(self,text='YES',variable=self.lv2,value=True,indicatoron=0,command=updateCharacter).grid(row=4,column=1,sticky=EW)
        lv2No = Radiobutton(self,text='NO',variable=self.lv2,value=False,indicatoron=0,command=updateCharacter).grid(row=4,column=2,sticky=EW)

        def tccallback():
            if character.tactician:
                character.tactician = False
            else:
                character.tactician = True
            printChar(character)

        ##TACTICIAN RADIO BUTTON    
        tcYes = Radiobutton(self,text='YES',variable=self.tc,value=True,indicatoron=0,command=updateCharacter).grid(row=5,column=1,sticky=EW)
        tcNo = Radiobutton(self,text='NO',variable=self.tc,value=False,indicatoron=0,command=updateCharacter).grid(row=5,column=2,sticky=EW)
        
class combatPicker(Frame):
    def __init__(self,master,*args,**kwargs):
        Frame.__init__(self,master,*args,**kwargs)
        for i in range(len(PC.keys())):
            Grid.rowconfigure(self,i,weight=1)
        Grid.columnconfigure(self,0,weight=1)
        Grid.columnconfigure(self,1,weight=0)
        def populate():
            r = 0
            ##for ch in combat.values():
            for k in range(len(combat.keys())):
                fn = list(combat.keys())[k]
                ch = list(combat.values())[k]
                Nameplate = Label(self,text=ch.name).grid(row=r,column=0,sticky=NSEW)
                Remove = Button(self,text='Remove',command=lambda fn=fn:pop_remove(fn)).grid(row=r,column=1,sticky=NSEW)
                r += 1
                
        def clear():
            for widget in self.winfo_children():
                widget.destroy()
                
        def pop_remove(fname):
            ##print(fname)
            combat.pop(fname)
            clear()
            populate()

        populate()


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

####################
## POWER TRACKERS ##
quickenTracker = {}
slowTracker = {}
####################

root = Tk()
root.geometry('200x400')
root.iconbitmap('swit.ico')
root.title('')
main = MainWindow(root)
main.pack(side=TOP,fill=BOTH,expand=True)

mainloop()
