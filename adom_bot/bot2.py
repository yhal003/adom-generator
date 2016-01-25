import pty
import pyte
import subprocess
import os
import termios
import struct
import fcntl
import threading
import time
import signal
import re
import select
import queue

from adom_constants import *
from config import *

class Character:
    def __init__(self):
        self.corruptions = set()
        self.talents = set()

def feed_data(console,stream):
    while (True):
        time.sleep(0.01)
        data = os.read(console,10240)
        stream.feed(data)

def find_match(screen,pattern):
    for line in screen.display:
        m = re.search(pattern, line)
        if (m != None):
            return m
    return None

def expect(screen,regex_list):
    global screen_queues 
#    print("expecting %s" % str(regex_list))
    q = screen_queues[screen]

    for i in range(0,len(regex_list)):
        r = regex_list[i]
        m = find_match(screen,r)
        if (m != None):
            return (i,m)


    while (True):
        try:
            #q.get(True,0.001)
            q.get()
        except queue.Empty:
            pass
        for i in range(0,len(regex_list)):
            r = regex_list[i]
            m = find_match(screen,r)
            if (m != None):
                return (i,m)


def expect_line_different(screen,ln, s):
#    print("expecting different line from %s" % s)
    global screen_queues 
    q = screen_queues[screen]
    while (True):
        try:
            q.get(True,0.001)
        except queue.Empty:
            pass
        if (screen.display[ln] != s):
            return screen.display[ln]

    

def send(console,s):
    os.write(console,bytes(s,"ASCII"))

def check_inventory(screen,console,item_re,item_type):
    send(console,item_type)
    item_type_re = re.compile(re.escape("('%s')" % item_type))
    expect(screen, [item_type_re,r"nothing"])
    for l in screen.display:
        if (re.search(item_re,l) != None):
            print("item matches!")
            return True
    return False
    

def pick_talent(screen,console,talent,attempt):
    #print("picking %s" % talent)
    pick = "a"
    expect(screen,[r'\[\?\] Help'])
    talent_re = re.compile("([A-Z])[ ]*\-[ ]*%s" % talent)
    (i,m) = expect(screen, [talent_re,r"Choose"]);
    if (i == 0):
        pick = m.group(1)
        send(console,pick)
        return True
    else:
        if (not ((screen.display[-6].startswith("(more")) or (screen.display[-5].startswith("(more")) or screen.display[-4].startswith("(more"))):
            if (attempt < 1):
                return pick_talent(screen,console,talent,attempt+1)
            else:
                for l in screen.display:
                    print(l)
                send(console,"a")
                return False
        first_talent = screen.display[3]
        mid_talent = screen.display[10]
        last_talent = screen.display[16]
        send(console,"+")
        time.sleep(0.05)
        expect_line_different(screen,3,first_talent)
        expect_line_different(screen,10,mid_talent)
        expect_line_different(screen,16,last_talent)
        return pick_talent(screen,console,talent,attempt)




global screen_queues
screen_queues = {}
global poll 
poll  = select.poll()
global master_to_stream_console
master_to_stream_console = {}
global total
total = 0
global maximum

global found
found = False


def char_selector(config,seed):

    global total
    global maximum
    global found
    global poll
    global master_to_stream_console


    master, slave = pty.openpty()

    winsize = struct.pack("HHHH",ROWS,COLS,0,0)
    fcntl.ioctl(master, termios.TIOCSWINSZ, winsize)


    s = subprocess.Popen([ADOM_PATH], stdout = slave, stdin = slave, shell=True, preexec_fn=os.setsid)
    
    screen = pyte.Screen(COLS,ROWS)
    stream = pyte.ByteStream()
    stream.attach(screen)

    screen_queues[screen] = queue.Queue()

    master_to_stream_console[master] = (stream,screen)
    poll.register(master,select.POLLIN)

    #t = threading.Thread(target = lambda : feed_data(master,stream))
    #t.daemon = True
    #t.start()

    expect(screen,[r"--- Play the Game --- Credits ---"])
    send(master,"p")
    (i,m) = expect(screen,[r"Press '(.)' to continue"])
    key = m.group(1)
    send(master,key.lower())

    while (True):


        total += 1
        if (total > maximum or found):
            os.killpg(s.pid,signal.SIGTERM)
            return

        char = Character()

        expect(screen,[r"Your choice"])
        send(master,"g")
        (i,m) = expect(screen,[r"You are born in the month of the (.*) on"])
        month = m.group(1)
        #print("Generated month of the %s" % m.group(1))    
        send(master," ")
        #expect(screen,[r'\[s\]pecific character type'])
        send(master,"s")
        #expect(screen,[r'Choose a sex'])
        send(master,pick_sex(char_description.SEX))
        #expect(screen,[r'Choose a race'])
        send(master,pick_race(char_description.RACE))
        #expect(screen,[r'Choose a profession'])
        send(master,pick_class(char_description.CLASS))
        #expect(screen,[r'Press SPACE to continue'])
        send(master," ")
        #expect(screen,[r'Shall your attributes be modified'])
        send(master,"r")

        if (char_description.TALENTS):
            talent_list = char_description.TALENTS
        else:
            talent_list = []
        t = 1
        (i,m) = expect(screen,[r'Choose a talent \(1 of ([1-9])\)'])
        talents = int(m.group(1))
        picked_all_talents = True

#        print("total talents count is %d" % talents)
        while (True):
            succ = pick_talent(screen,master, talent_list[t-1],0)
            picked_all_talents = picked_all_talents  and succ
            t += 1
            if (t > talents):
                break
            (i,m) = expect(screen,[r'Choose a talent \(%d of %d\)' % (t,talents)])

        name = char_description.NAME + "_%d%d" % (total,seed)
        expect(screen,[r'What is your name'])
        send(master,"%s\n" % name)


#        time.sleep(0.2)
#        print(screen.display)
        (i,m) = expect(screen,[r'DV/PV: ([0-9]+)/([0-9]+)'])
        DV  = int(m.group(1))
        PV  = int(m.group(2))
        (i,m) = expect(screen,
                       [r'St:[ ]*([0-9]+)  Le:[ ]*([0-9]+)  Wi:[ ]*([0-9]+)  Dx:[ ]*([0-9]+)  To:[ ]*([0-9]+)  Ch:[ ]*([0-9]+)  Ap:[ ]*([0-9]+)  Ma:[ ]*([0-9]+)  Pe:[ ]*([0-9]+)'])
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


        # corruption list
        send(master,"\\")
        (i,m) = expect(screen,[r"C \- (.*)",r"You are not yet corrupted"])
#        for l in screen.display:
#            print(l)

        if (i == 0):
            expect(screen,[r"A \- (.*)"])
            expect(screen,[r"B \- (.*)"])
            corruptions = set()
            corruption_screen  = "".join(screen.display)
            r  = r'[A-Z] - ([^.!*]+[.!*])'
            for c in re.findall(r,corruption_screen):
                corruptions.add(c)
            send(master," ")
            expect(screen,[r'DV/PV: ([0-9]+)/([0-9]+)'])
        

        # now we check if char fits

        fits = True

        
        if (hasattr(char_description,"TALENT_COUNT")):
            if (talents < char_description.TALENT_COUNT):
                fits = False
        
        if (hasattr(char_description,"STARSIGN")):
            if (char_description.STARSIGN != month):
                fits = False

        if (hasattr(char_description,"GOOD_CORRUPTIONS")):
            fits = fits and set(corruptions).issuperset(set(char_description.GOOD_CORRUPTIONS))

        if (hasattr(char_description,"BAD_CORRUPTIONS")):
            fits = fits and set(corruptions).isdisjoint(set(char_description.BAD_CORRUPTIONS))

        # check stats
        if (hasattr(char_description,"ST")):
            fits = fits and (char.st >= char_description.ST)
        if (hasattr(char_description,"LE")):
            fits = fits and (char.le >= char_description.LE)
        if (hasattr(char_description,"WI")):
            fits = fits and (char.wi >= char_description.WI)
        if (hasattr(char_description,"DX")):
            fits = fits and (char.dx >= char_description.DX)
        if (hasattr(char_description,"TO")):
            fits = fits and (char.to >= char_description.TO)
        if (hasattr(char_description,"CH")):
            fits = fits and (char.ch >= char_description.CH)
        if (hasattr(char_description,"AP")):
            fits = fits and (char.ap >= char_description.AP)
        if (hasattr(char_description,"MA")):
            fits = fits and (char.ma >= char_description.MA)
        if (hasattr(char_description,"PE")):
            fits = fits and (char.pe >= char_description.PE)

        # check inventory
        if (hasattr(char_description,"ITEMS")):
            send(master,"i")
            send(master,"v")
            expect(screen,[r"Text filter"])

            item_types = set()
            items = set()
            for (item_type,item) in char_description.ITEMS:
                item_types.add(item_type)
                items.add(item)

            inventory = {}
            for item_type in item_types:
                inventory[item_type] = []
                send(master, item_type)
                time.sleep(0.05)
                item_type_re = re.compile(re.escape("('%s')" % item_type))
                (i,m) = expect(screen, [item_type_re,r"nothing"])
                #for l in screen.display:
                #    print(l)
                if (i == 0):
                    item_list_screen = "".join(screen.display)
                    item_re = r"[a-z][ ]*\-[ ]*([^\[]*)\[[0-9]+s\]"
                    for it in re.findall(item_re,item_list_screen):
                        inventory[item_type].append(it)
                        print(it)
                
            for (item_type,item) in char_description.ITEMS:
                found_item = False
                for it in inventory.get(item_type,[]):
                    if (re.search(item,it)):
                        found_item = True
                        break
                if (not found_item):
                    fits = False
                    break
                    
            
            send(master," ")
            send(master," ")
            expect(screen,[r'DV/PV: ([0-9]+)/([0-9]+)'])
            


        if (fits):
            print("This one FITS!!!")
            send(master,"S")
            send(master,"y\n")
            send(master," ")

            #send(master,"Q")
            #expect(screen,[r'Really quit?'])
            #send(master,"y\n")
            #expect(screen,[r'Game Summary'])
            #send(master," ")
            #expect(screen,[r'Press SPACE to continue'])
            #send(master," ")

        else:
            send(master,"Q")
            expect(screen,[r'Really quit?'])
            send(master,"y\n")
            expect(screen,[r'Game Summary'])
            send(master," ")
            expect(screen,[r'Press SPACE to continue'])
            send(master," ")

        print("generated char month=%s talents=%d DV:PV %d/%d  (st:%d,le:%d,wi:%d,dx:%d,to:%d,ch:%d,ap:%d,ma:%d,pe:%d) " % (month,talents,DV,PV,char.st,char.le,char.wi,char.dx,char.to,char.ch,char.ap,char.ma,char.pe))
        #print("corruptions: %s" % str(corruptions))
    print("COMPLETE")

    print(screen.display)

import sys

if (len(sys.argv) != 3):
    print("usage: roller num char_description_file.py",file=sys.stderr)
    print("where num is maximum number of characters to roll",file=sys.stderr)
    print("and char_description_file.py is your character definition",file=sys.stderr)
    exit(1)

maximum = int(sys.argv[1])

module_name = re.match((r"([^.]+)."),sys.argv[2]).group(1)
char_description = __import__(module_name)


# t = threading.Thread(target = lambda : feed_data(master,stream))

#char_description = {}
#char_description["class"] = "Wizard"
#char_description["race"] = "Gray Elf"
#char_description["sex"] =  "Male"
#char_description["talents"] =  ["Alert","Miser","Treasure Hunter","Boon to the Family","a","a","a","a"]

import random
import string
random.seed()
char_description.NAME = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))

# constrains

#char_description["talent_count"] = 1
#char_description["items"] = [("=", r"ring(.*) of djinni")]
#char_description["good_corruptions"] = ["astral","stilts","antennae"] 
#char_description["good_corruptions"] = ["antennae","astral","stilts"] 
#char_description["bad_corruptions"] = ["stiff","mana battery"] 
#char_description["starsign"] = "Candle"

#char_description["Le"] = 20
#char_description["St"] = 17
#char_description["To"] = 14


def poll_adoms():
    global poll
    global master_to_stream_console
    global screen_queues
    print("Started")
    while (True):
        #time.sleep(0.01)
        ls = poll.poll(0)
        for (master,event) in ls:
            (stream,console) = master_to_stream_console[master]
            data = os.read(master,1024000)
            stream.feed(data)
            screen_queues[console].put(1)


t = threading.Thread(target = poll_adoms)
t.daemon = True
t.start()            

import timeit
char_selector(char_description,1)

#for i in range(0,1):
#    time.sleep(1)
#    t = threading.Thread(target = lambda: char_selector(char_description))
#    t.start()

