from adom_constants import *
import re
from enum import Enum
import time
import sys
from profilehooks import profile

class GameState(Enum):
    begin = 1
    main_menu = 2
    talents = 3
    wilderness = 4
    inventory = 5
    corruptions = 6

START_GAME_MARKER = r"--- Play the Game --- Credits ---"
PRESS_KEY_MARKER = r"Press '(.)' to continue"
POSTCARD_MARKER = r'The Postcard Quest'
MAIN_MENU_MARKER = r"Your choice"
MONTH_SELECTION_MARKER = r"You are born in the month of the (.*) on"
TALENT_CHOICE_MARKER = r"Choose a talent \([1-9] of ([1-9])\)"

def TALENT_PICK_MARKER(talent):
    return re.compile("([A-Z])[ ]*\-[ ]*%s" % talent)

HELP_MARKER = r'\[\?\] Help'
NAME_MARKER = r'What is your name'
WILDERNESS_MARKER = 'DV/PV:[ ]+[0-9]+/[0-9]+[ ]+H:[ ]+[0-9]+\([0-9]+\)[ ]+P:[ ]+[0-9]+\([0-9]+\)[ ]+Exp:[ ]+[0-9]+/[0-9]+[ ]+DrCh'
STATS_MARKER = r'St:[ ]*([0-9]+)  Le:[ ]*([0-9]+)  Wi:[ ]*([0-9]+)  Dx:[ ]*([0-9]+)  To:[ ]*([0-9]+)  Ch:[ ]*([0-9]+)  Ap:[ ]*([0-9]+)  Ma:[ ]*([0-9]+)  Pe:[ ]*([0-9]+)'

REALLY_QUIT_MARKER = r'Really quit\?'
REALLY_SAVE_MARKER = r'Really save the game\?'
GAME_SUMMARY_MARKER = r'Game Summary'
PRESS_SPACE_MARKER = r'Press SPACE to continue'

MORE_MARKER = r'\(more'

INVENTORY_MARKER = r'Text filter'
ITEM_MARKER = r'[a-z][ ]*\-[ ]*([^\[]*)\[[0-9]+s\]'
GOLD_MARKER=r'You are carrying ([0-9]+) gold pieces\.'
NO_GOLD_MARKER=r'You don\'t own any gold pieces\.'

YOU_ARE_NOT_YET_CORRUPTED_MARKER = r'You are not yet corrupted'
CORRUPTION_MARKER = r'[A-Z] - (.*)'


class Character:
    def __init__(self):
        (self.st, self.le, self.wi, 
         self.dx, self.to, self.ch, 
         self.ap, self.ma, self.pe) = (0,0,0,0,0,0,0,0,0)

        self.month = None
        self.talent_count = 0
        self.item_list = { 
            ITEM_RING: [],
            ITEM_BOOK: [],
            ITEM_AMULET: [],
            ITEM_FOOD: [],
            ITEM_SCROLL: [],
            ITEM_WAND: [],
            ITEM_POTION: [],
            ITEM_WEAPON: []
            
        }

        self.gold = 0

        self.corruptions = []

class ADOM_Bot:

    def __init__(self,adom_process):
        self.process = adom_process
        self.expect([START_GAME_MARKER])
        self.state = GameState.begin


    def expect_non_blocking(self,regex_list, start = 0, finish = -1):
        self.process.release_on_change()
        if (finish == -1):
            finish = len(self.process.screen.dump())
        for i in range(0,len(regex_list)):
            r = regex_list[i]
            found = False
            pattern = None
            for l in self.process.screen.dump()[start:finish]:
                m = re.search(r,l)
                if (m != None):
                    found = True
                    pattern = m
                    break
            if (found):
                return (i,m)
        return (-1,None)

    def expect(self,regex_list, start = 0, finish = -1):
        print("expecting %s " % str(regex_list), file=sys.stderr)
        while (True):
            (i,m) = self.expect_non_blocking(regex_list, start, finish)
            if (i != -1):
                return (i,m)
            else:
                pass
                #self.process.release_on_change()

                

    def _check_state(self,expected):
        if (self.state != expected):
            raise ValueError("operation can only be performed in state %r: bot in state %r" % (expected, self.state))

    def send(self,str):
        self.process.send(str)
    
    def main_menu(self):
        self._check_state(GameState.begin)
        self.send("p")
        (i,m) = self.expect([PRESS_KEY_MARKER])
        key = m.group(1).lower()
        self.send(key)
        #time.sleep(0.1)
        #print("\n".join(self.process.screen.dump()))
        (i,m) = self.expect([POSTCARD_MARKER,MAIN_MENU_MARKER])
        if (i == 0):
            self.send(" ")
            self.expect([MAIN_MENU_MARKER])
        self.state = GameState.main_menu

    # returns partially filled character
    def roll_character(self,
                       name,
                       sex,
                       race,
                       profession,
                       talents):
        self._check_state(GameState.main_menu)
        char = Character()
        self.send("g")
        (i,m) = self.expect([MONTH_SELECTION_MARKER])
        char.month = m.group(1)
        self.send(" s%s%s%s r" % (pick_sex(sex), pick_race(race), pick_class(profession)))
        (i,m) = self.expect([TALENT_CHOICE_MARKER])
        self.state = GameState.talents

        char.talent_count = int(m.group(1))
        ts = talents[:]
        for i in range(0,char.talent_count):
            try:
                t = ts.pop(0)
            except IndexError:
                t = "Random Talent Selection"
            self.pick_talent(t)
        self.expect([NAME_MARKER])
        self.send("%s\n" % name)
        self.expect([WILDERNESS_MARKER])
        self.state = GameState.wilderness
        return char

    def fill_stats(self, char):
        self._check_state(GameState.wilderness)
        (i,m) = self.expect([STATS_MARKER])
        (char.st,char.le,char.wi,char.dx,
         char.to,char.ch,char.ap,
         char.ma,char.pe) = (int(m.group(1)),
                                        int(m.group(2)),
                                        int(m.group(3)),
                                        int(m.group(4)),
                                        int(m.group(5)),
                                        int(m.group(6)),
                                        int(m.group(7)),
                                        int(m.group(8)),
                                        int(m.group(9)))

    def fill_items(self,char,item_type):
        self._check_state(GameState.wilderness)
        self.send("i")
        self.send("v")
        self.expect([INVENTORY_MARKER])
        self.state = GameState.inventory
        self.send(item_type)
        time.sleep(0.01)
        
        item_type_re = re.escape("('%s')" % item_type)

        (i,m) = self.expect([item_type_re, r"nothing"],4,5)
        if (i == 0):
            item_list_screen = "".join(self.process.screen.dump())
            for it in re.findall(ITEM_MARKER, item_list_screen):
                char.item_list[item_type].append(it)

        self.send(" ")
        self.send(" ")
        self.expect([WILDERNESS_MARKER])
        self.state = GameState.wilderness

    def fill_gold(self,char):
        self._check_state(GameState.wilderness)
        self.send("$")
        (i,m) = self.expect([GOLD_MARKER,NO_GOLD_MARKER])
        if (i == 0):
            char.gold = int(m.group(1))
        else:
            char.gold = 0

    def fill_corruptions(self,char):
        self._check_state(GameState.wilderness)
        self.send("\\")
        #time.sleep(0.05)
        #for l in self.process.screen.dump():
        #    print(l)
        (i,m) = self.expect([CORRUPTION_MARKER,YOU_ARE_NOT_YET_CORRUPTED_MARKER])
        if (i == 0):
            self.state = GameState.corruptions
            time.sleep(0.05)
            corruption_screen = "".join(self.process.screen.dump())
            corruption_types = re.compile("(" + "|".join(CORRUPTIONS) + ")")
            for c in re.findall(corruption_types, corruption_screen):
                char.corruptions.append(c[0])
            self.send(" ")
            self.expect([WILDERNESS_MARKER])
            self.state = GameState.wilderness
        



    def save_game(self):
        self._check_state(GameState.wilderness)
        self.send("S")
        self.expect([REALLY_SAVE_MARKER])
        self.send("y\n")
        self.expect([PRESS_SPACE_MARKER])
        self.send(" ")
        self.expect([MAIN_MENU_MARKER])
        self.state = GameState.main_menu

    def quit_game(self):
        self._check_state(GameState.wilderness)
        self.send("Q")
        self.expect([REALLY_QUIT_MARKER])
        self.send("y\n")
        self.expect([GAME_SUMMARY_MARKER])
        self.send(" ")
        self.expect([PRESS_SPACE_MARKER])
        self.send(" ")
        self.expect([MAIN_MENU_MARKER])
        self.state = GameState.main_menu

    def pick_talent(self,talent):
        self._check_state(GameState.talents)
        #time.sleep(0.05)
        #print("\n".join(self.process.screen.dump()))
        self.expect([HELP_MARKER])
        (i,match) = self.expect_non_blocking([TALENT_PICK_MARKER(talent)])
        if (match):
            pick = match.group(1)
            self.send(pick)
            return True
        else:
            #print(TALENT_PICK_MARKER(talent))
            footer = "".join(self.process.screen.dump()[-6:-1])
            if (not re.search(MORE_MARKER,footer)):
                # random talent selection
                self.send("a")
                return False
            else:
                self.send("+")
                # this is ugly but I do not know how to reliably check page scroll
                time.sleep(0.05)
                return self.pick_talent(talent)
            
                
            
                


        
        
