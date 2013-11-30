# -*- encoding: utf-8 -*-
import select
import subprocess
import time
from abjad.tools import abctools


class Pipe(abctools.AbjadObject, subprocess.Popen):
    r'''A two-way, non-blocking pipe for interprocess communication:

    ::

        >>> pipe = documentationtools.Pipe('python', ['-i'])
        >>> pipe.writeline('my_list = [1, 2, 3]') # doctest: +SKIP
        >>> pipe.writeline('print my_list')       # doctest: +SKIP

    Return `Pipe` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_arguments', 
        '_executable', 
        '_timeout',
        )

    ### INITIALIZER ###

    def __init__(self, executable='python', arguments=('-i',), timeout=0):
        self._arguments = arguments
        self._executable = executable
        self._timeout = timeout
        argv = [executable]
        if arguments != None:
            argv = argv + list(arguments)
        subprocess.Popen.__init__(self, argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Arguments of pipe.
        '''
        return self._arguments

    @property
    def executable(self):
        r'''Executable of pipe.
        '''
        return self._executable

    @property
    def timeout(self):
        r'''Timeout of pipe.
        '''
        return self._timeout

    ### PRIVATE METHODS ###

    def _readbyte(self, n=1):
        poll = select.poll()
        poll.register(self.stdout.fileno(), select.POLLIN or select.POLLPRI)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                return self.stdout.read(n)

    ### PUBLIC METHODS ###

    def close(self):
        r'''Closes pipe.
        '''
        self.terminate()
        self.wait()

    def read(self):
        r'''Reads from pipe.
        '''
        c = self._readbyte()
        string = ""
        while c != None:
            string = string + str(c)
            c = self._readbyte()
        return string

    def read_wait(self, seconds=0.01):
        r'''Tries to read from pipe.  Wait `seconds` 
        if nothing comes out and the repeats.

        Should be used with caution, as this may loop forever.
        '''
        while True:
            read = self.read()
            if read:
                return read
            time.sleep(seconds)

    def write(self, data):
        r'''Writes `data` into pipe.
        '''
        poll = select.poll()
        poll.register(self.stdin.fileno(), select.POLLOUT)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                self.stdin.write(data)

    def write_line(self, data):
        r'''Write `data` into pipe. Then writes newline to pipe.
        '''
        self.write('%s\n' % data)
