import select
import subprocess
from abjad.tools import abctools


class Pipe(abctools.AbjadObject, subprocess.Popen):
    '''A two-way, non-blocking pipe for interprocess communication:

    ::

        abjad> from abjad.tools.documentationtools import Pipe
        abjad> pipe = Pipe('python', ['-i'])
        abjad> pipe.write('my_list = [1, 2, 3]\n')
        abjad> pipe.write('print my_list')

    Return `Pipe` instance.
    '''

    def __init__(self, exe='python', args=['-i'], timeout=0):
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
