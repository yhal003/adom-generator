import subprocess
import termios
import fcntl
import pty
import tty
import struct
import os
import signal
import select
import pyte
import vt102
#import queue
import threading
from multiprocessing import Process,Queue
import array


class ADOM_Process:

    def __init__(self, path, rows, cols):
        self.master, self.slave = pty.openpty()
        winsize = struct.pack("HHHH",rows,cols,0,0)
        fcntl.ioctl(self.master, termios.TIOCSWINSZ, winsize)
        tty.setraw(self.master)
        tty.setraw(self.slave)

        attr = termios.tcgetattr(self.master)
        (attr[4],attr[5]) = (4098,4098)
        termios.tcsetattr(self.master,termios.TCSANOW, attr)

        my_env = os.environ
        my_env["LD_PRELOAD"] = "./libnosleep.so"
        self.process = subprocess.Popen([path], 
                                        stdout = self.slave, 
                                        stdin = self.slave, 
                                        shell=False, 
                                        env = my_env,
                                        preexec_fn=os.setsid)
        

        self.poll = select.epoll()
        self.poll.register(self.master,select.POLLIN)
        #self.screen = pyte.Screen(cols, rows)
        #self.stream = pyte.ByteStream()
        #self.stream.attach(self.screen)
        #self.stream = vt102.stream()
        #self.screen = vt102.screen((rows,cols))
        #self.screen.attach(self.stream)
        import terminal
        self.screen = terminal.Terminal(rows,cols, enabled_filetypes = None)

        self.queue = Queue()
        
        #self.polling_thread = threading.Thread(target = self._poll)
        #self.polling_thread.daemon = True
        #self.polling_thread.start()


    def _poll(self):
        while (True):
            ls = self.poll.poll(0)
            for (fd,event) in ls:
                data = os.read(self.master,1024000)
                self.stream.feed(data)
                self.queue.put(1)



    def release_on_change(self):
        ls = self.poll.poll(0)
        if (len(ls) == 0):
            return
        while (True):
            data = os.read(self.master,204800)
            #self.stream.process(bytes(data).decode("utf-8"))
            self.screen.write(bytes(data).decode("ascii"),special_checks = False)
            #self.new_screen.feed(data)
            if (len(data) < 204800):
                break

        #self.queue.get()

    def send(self, str):
        os.write(self.master, bytes(str,"ASCII"))
        # termios.tcdrain(self.master)

        

    def kill(self):
        os.killpg(self.process.pid, signal.SIGTERM)
