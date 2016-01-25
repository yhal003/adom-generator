from config import *
from dark_magic import ADOM_Process
from adom_bot import ADOM_Bot

import re
import signal
import sys
import traceback

def signal_handler(signal, frame):
    p.kill()
    print("Killed",file=sys.stderr)
    sys.exit(0)

# generate ADOM character based on character definition 
# expects the game to be in main menu
def generate(bot,character_definition,seed):
    pass

signal.signal(signal.SIGINT, signal_handler)

def verify_char(bot,char,char_description):
    fits = True
    if (hasattr(char_description,"STARSIGN")):
        fits = fits and (char_description.STARSIGN == char.month)

    if (hasattr(char_description,"TALENT_COUNT")):
        fits = fits and (char_description.TALENT_COUNT <= char.talent_count)

    if (hasattr(char_description,"ITEMS")):
        for item_type in char_description.ITEMS.keys():
            bot.fill_items(char, item_type)
            for item_re in char_description.ITEMS[item_type]:
                has_item = False
                for item in char.item_list[item_type]:
                    print(item)
                    if re.search(item_re,item):
                        has_item = True
                if (not has_item):
                    fits = False

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

    if (hasattr(char_description,"GOLD")):
        bot.fill_gold(char)
        fits = fits and (char.gold >= char_description.GOLD)

    if (hasattr(char_description,"GOOD_CORRUPTIONS") or hasattr(char_description,"BAD_CORRUPTIONS")):
        bot.fill_corruptions(char)
        for c in char.corruptions:
            print(c)

    if (hasattr(char_description,"GOOD_CORRUPTIONS")):
        fits = fits and set(char_description.GOOD_CORRUPTIONS).issubset(set(char.corruptions))
    
    if (hasattr(char_description,"BAD_CORRUPTIONS")):
        fits = fits and set(char_description.BAD_CORRUPTIONS).isdisjoint(set(char.corruptions))

    return fits



p = ADOM_Process(ADOM_PATH, ROWS, COLS)

try:
    b = ADOM_Bot(p)

    if (len(sys.argv) != 3):
        print("usage: roller num char_description_file.py",file=sys.stderr)
        print("where num is maximum number of characters to roll",file=sys.stderr)
        print("and char_description_file.py is your character definition",file=sys.stderr)
        exit(1)

    maximum = int(sys.argv[1])

    module_name = re.match((r"([^.]+)."),sys.argv[2]).group(1)
    char_description = __import__(module_name)

    import random
    import string
    random.seed()
    char_description.NAME = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))



    from adom_constants import *
    b.main_menu()
    for i in range(0,maximum):
        char = b.roll_character(char_description.NAME, 
                                char_description.SEX,
                                char_description.RACE,
                                char_description.CLASS,
                                char_description.TALENTS)
        b.fill_stats(char)
        if (verify_char(b,char,char_description)):
            print("FITS!")
            b.save_game()
            p.kill()
            exit(0)
        print("%s talents=%d st:%d,le:%d,wi:%d,dx:%d,to:%d,ch:%d,ap:%d,ma:%d,pe:%d" %
              (char.month, char.talent_count, 
               char.st, char.le, char.wi, char.dx, char.to, char.ch, char.ap, char.ma, char.pe)
        )

        b.quit_game()

except Exception as err:
    print(traceback.format_exc(), file=sys.stderr)
finally:
    p.kill()
