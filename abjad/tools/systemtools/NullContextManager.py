# -*- coding: utf-8 -*-
from abjad.tools.abctools import ContextManager


class NullContextManager(ContextManager):
    r'''A context manager that does nothing.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager and does nothing.
        '''
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager and does nothing.
        '''
        pass
