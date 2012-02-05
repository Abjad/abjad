import select
import subprocess


class Pipe(subprocess.Popen):

    def __init__(self, exe, args=None, timeout=0):
        self.timeout = timeout
        argv = [exe]
        if args != None:
            argv = argv + args
        subprocess.Popen.__init__(self, argv, 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    def close(self):
        self.terminate()
        self.wait()

    def write(self, data):
        poll = select.poll()
        poll.register(self.stdin.fileno(), select.POLLOUT)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                self.stdin.write(data)

    def _readbyte(self, n = 1):
        poll = select.poll()
        poll.register(self.stdout.fileno(), select.POLLIN or select.POLLPRI)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                return self.stdout.read(n)

    def read(self, n = 1):
        c = self._readbyte()
        string = ""
        while c != None:
            string = string + str(c)
            c = self._readbyte()
        return string
