import select
import subprocess
from abjad.tools import abctools


class Pipe(abctools.AbjadObject, subprocess.Popen):
    '''A two-way, non-blocking pipe for interprocess communication:
    
    ::
    
        abjad> from abjad.tools.documentationtools import Pipe
    
    ::
    
        abjad> pipe = Pipe('python', ['-i'])
        abjad> pipe.writeline('my_list = [1, 2, 3]')
        abjad> pipe.writeline('print my_list')
    
    Return `Pipe` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_arguments', '_executable', '_timeout')

    ### INITIALIZER ###

    def __init__(self, executable='python', arguments=['-i'], timeout=0):
        self._arguments = arguments
        self._executable = executable
        self._timeout = timeout
        argv = [executable]
        if arguments != None:
            argv = argv + arguments
        subprocess.Popen.__init__(self, argv, 
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

    ### PUBLIC ATTRIBUTES ###

    @property
    def arguments(self):
        return self._arguments

    @property
    def executable(self):
        return self._executable

    @property
    def timeout(self):
        return self._timeout

    ### PRIVATE METHODS ###

    def _readbyte(self, n = 1):
        poll = select.poll()
        poll.register(self.stdout.fileno(), select.POLLIN or select.POLLPRI)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                return self.stdout.read(n)

    ### PUBLIC METHODS ###

    def close(self):
        '''Close the pipe.'''
        self.terminate()
        self.wait()

    def read(self, n = 1):
        '''Read from the pipe.'''
        c = self._readbyte()
        string = ""
        while c != None:
            string = string + str(c)
            c = self._readbyte()
        return string

    def write(self, data):
        '''Write `data` into the pipe.'''
        poll = select.poll()
        poll.register(self.stdin.fileno(), select.POLLOUT)
        fd = poll.poll(self.timeout)
        if len(fd):
            f = fd[0]
            if f[1] > 0:
                self.stdin.write(data)

    def writeline(self, data):
        '''Write `data` into the pipe, terminated by a newline.'''
        self.write('%s\n' % data)
