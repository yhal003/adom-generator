
import re

ESCAPE = 0x1b

PROTOCOL = [(r"\[c", "query device code"),
            (r"\[[1-9]0c", "report device code"),
            (r"\[5n", "query device status"),
            (r"\[0n", "report device ok"),
            (r"\[3n", "report device failure"),
            (r"\[6n","query cursor position"),
            (r"\[([0-9]+);([0-9]+)R", "report cursor position"),
            (r"c", "reset device"),
            (r"\[7h", "enable line wrap"),
            (r"\[7l", "disable line wrap"),
            (r"\(", "set default font"),
            (r"\)", "set alternate font"),
            (r"\[H", "cursor home"),
            (r"\[f", "cursor home (again)"),
            (r"\[([0-9]+);([0-9]+)H", "set cursor position"),
            (r"\[([0-9]+);([0-9]+)f", "set cursor position (again)"),
            (r"\[A", "move up one"),
            (r"\[B", "move down one"),
            (r"\[C", "move forward one"),
            (r"\[D", "move backward one"),
            (r"\[([0-9])+A", "count up"),
            (r"\[([0-9])+B", "count down"),
            (r"\[([0-9])+C", "count forward"),
            (r"\[([0-9])+D", "count backward"),
            (r"\[s", "save cursor"),
            (r"\[u", "unsave cursor"),
            (r"7", "save cursor and attrs"),
            (r"8", "restore cursor and attrs"),
            (r"\[r", "enable scrolling"),
            (r"\[([0-9]+);([0-9]+)r", "enable scrolling from row to row"),
            (r"D", "scroll down"),
            (r"M", "scroll up"),
            (r"H", "set tab at current position"),
            (r"\[g", "clear tab"),
            (r"\[3g", "clear all tabs"),
            (r"\[K","erase end of line"),
            (r"\[1K","erase start of line"),
            (r"\[2K","erase the entire line"),
            (r"\[J","erase down"),
            (r"\[1J","erase up"),
            (r"\[2J","erase screen"),
            (r"\[i","print screen"),
            (r"\[1i","print line"),
            (r"\[4i","disable print log"),
            (r"\[5i","start print log"),
            (r"\[4l","reset to replacement mode"),
            (r"\[(([0-9]+(;[0-9]+)*))*m","set dislay attributes"),
            (r'\[\?1h',"cursor keys mode"),
            (r'=',"special keypad mode"),
            (r'\[\?1049h',"alternative screen buffer"),
            (r'\[\?25n',"are user defined keys locked?"),
            (r'\[\?25l',"make cursor invisible"),
            (r'\[\?25h',"make cursor visible(?)"),
            (r'\[([0-9])@',"insert character"),
            (r"\[(([0-9]+(;[0-9]+)*))*h","set mode"),
]

from enum import Enum
class ScreenState(Enum):
    normal = 0
    escape = 1

class Screen:
    def __init__(self,cols,rows):
        self.display = []
        self.x = 0
        self.y = 0
        self.old_x= 0
        self.old_y = 0
        self.cols = cols
        self.rows = rows
        for i in range(0,rows):
            self.display.append([' '*cols])
        self.state = ScreenState.normal
        self.buffer =""

    
    def consume(self,b):
        if (self.state == ScreenState.normal):
            if (b == ESCAPE):
                self.state = ScreenState.escape
                return
            else:
                pass
                #print("printing %s" % bytes([b]).decode("ascii"))
        if (self.state == ScreenState.escape):
            if (b == ESCAPE):
                print("buffer is %s " % self.buffer)
                return
            self.buffer += bytes([b]).decode("ascii")
            for (command,desc) in PROTOCOL:
                if re.match(command,self.buffer):
                    print(desc)
                    self.buffer  = ""
                    self.state = ScreenState.normal
                    return


    def feed(self,bs):
        for b in bs:
            self.consume(b)
