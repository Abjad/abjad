# -*- encoding: utf-8 -*-
import sys
from abjad.tools.abctools import ContextManager


class ProgressIndicator(ContextManager):
    r'''A context manager for printing progress indications.
    '''

    ### INITIALIZER ###

    def __init__(self, message=''):
        self._message = message
        self._progress = 0

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters progress indicator.
        '''
        print '{}: {}'.format(self._message, self._progress),
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits progress indicator.
        '''
        print

    def __repr__(self):
        r'''Gets interpreter representation of context manager.

        ..  container:: example

            ::

                >>> context_manager = systemtools.ProgressIndicator()
                >>> context_manager
                <ProgressIndicator()>

        Returns string.
        '''
        return '<{}()>'.format(type(self).__name__)

    ### PUBLIC PROPERTIES ###

    @property
    def message(self):
        r'''Gets message of progress indicator.

        Returns string.
        '''
        return self._message

    ### PUBLIC METHODS ###

    def advance(self):
        r'''Advances the progress indicator's progress count.  Overwrites
        the current terminal line with the progress indicators message and new
        count.
        '''
        self._progress += 1
        sys.stdout.flush()
        print '\r',
        print '{}: {}'.format(self._message, self._progress),
