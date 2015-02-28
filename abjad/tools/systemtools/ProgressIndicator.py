# -*- encoding: utf-8 -*-
from __future__ import print_function
import sys
from abjad.tools.abctools import ContextManager


class ProgressIndicator(ContextManager):
    r'''A context manager for printing progress indications.
    '''

    ### INITIALIZER ###

    def __init__(self, message='', total=None):
        self._message = message
        self._progress = 0
        self._total = total

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters progress indicator.
        '''
        self._print()

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits progress indicator.
        '''
        print()

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

    ### PRIVATE METHODS ###

    def _print(self):
        message = self.message or 'Progress'
        if self.total is not None:
            message = '{}: {} / {}'.format(
                message,
                self.progress,
                self.total,
                )
            print(message, end='')
        else:
            message = '{}: {}'.format(
                message,
                self.progress,
                )
            print(message, end='')
        return self

    ### PUBLIC METHODS ###

    def advance(self):
        r'''Advances the progress indicator's progress count.  Overwrites
        the current terminal line with the progress indicators message and new
        count.
        '''
        self._progress += 1
        sys.stdout.flush()
        print('\r', end='')
        self._print()

    ### PUBLIC PROPERTIES ###

    @property
    def message(self):
        r'''Gets message of progress indicator.

        Returns string.
        '''
        return self._message

    @property
    def progress(self):
        r'''Gets progress.

        Returns integer.
        '''
        return self._progress

    @property
    def total(self):
        r'''Gets total count.

        Returns integer or none.
        '''
        return self._total