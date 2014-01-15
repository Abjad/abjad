# -*- encoding: utf-8 -*-
import sys
from abjad.tools.abctools import ContextManager


class RedirectedStreams(ContextManager):
    r'''A context manager for capturing stdout and stderr output.

    ::

        >>> import StringIO
        >>> string_io = StringIO.StringIO()
        >>> with systemtools.RedirectedStreams(stdout=string_io):
        ...     print "hello, world!"
        ...
        >>> result = string_io.getvalue()
        >>> string_io.close()
        >>> print result
        hello, world!

    Redirected streams context manager is immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters redirected streams context manager.

        Returns none.
        '''
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits redirected streams context manager.

        Returns none.
        '''
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        ..  container:: example

            ::

                >>> context_manager = systemtools.RedirectedStreams()
                >>> context_manager
                <RedirectedStreams()>

        Returns string.
        '''
        return '<{}()>'.format(type(self).__name__)
