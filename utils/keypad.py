class Keypad:
    
    def __init__(self):
        import platform

        if platform.system() == 'Windows':
            self.reader = self.OnWindows()
        else:
            self.reader = self.OnOthers()

    def initialize(self):
        self.reader.initialize()
            
    def readkey(self):
        return self.reader.read()
 
    # with statement is available
    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reader.destroy()
        return True             # for suppressing exceptions

    class OSTemplate:
        def initialize(self):pass
        def read(self):pass
        def destroy(self):pass

        def __caller__(self): return self.read()
    

    class OnWindows(OSTemplate):
        def __init__(self):
            global msvcrt
            import msvcrt

        def read(self):
            return msvcrt.getch()

    class OnOthers(OSTemplate):
        def __init__(self):
            global sys
            global termios
            global tty

            import sys
            import tty
            import termios

        def initialize(self):
            self.term_fd = sys.stdin.fileno()
            self.old_attr = termios.tcgetattr(self.term_fd)
            tty.setraw(self.term_fd)

        def read(self):
            return sys.stdin.read(1)

        def destroy(self):
            termios.tcsetattr(self.term_fd, termios.TCSADRAIN, self.old_attr)



if __name__ == '__main__':
    import time
    with Keypad() as k:
        while True:
            key = k.readkey()
            print( "{0}\r".format(key) )
            if key == 'q':
                print( "bye" )
                break
            time.sleep(0.05)
            
