class Keypad:
    def __init__(self):
        import platform
        self.os_type = platform.system()

    def initialize(self):
        if self.os_type == 'Windows':
            import msvcrt
        else:
            import sys
            import tty
            import termios

            self.term_fd = sys.stdin.fileno()
            self.old_attr = termios.tcgetattr(self.term_fd)
            tty.setraw(self.term_fd)

    def destroy(self):
        if self.os_type != 'Windows':
            import termios
            termios.tcsetattr(self.term_fd, termios.TCSADRAIN, self.old_attr)
            
    def readkey(self):
        if self.os_type == 'Windows':
            return msvcrt.getch()
        else:
            return sys.stdin.read(1)
    
    # with statement is available
    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.destroy()
        return True             # for suppressing exceptions


if __name__ == '__main__':
    import time
    with Keypad() as k:
        while True:
            key = k.readkey()
            print "%c" % key
            if key == 'q':
                print "bye"
                break
            time.sleep(0.5)
            
