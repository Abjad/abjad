# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextManager(AbjadObject):
    r'''An abstract context manager class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplemented

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __enter__(self):
        r'''Enters context manager.
        '''
        raise NotImplemented

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exits context manager.
        '''
        raise NotImplemented
