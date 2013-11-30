# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Maker(AbjadObject):
    r'''Abstract base class for all maker classers.
    '''

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        r'''Calls maker.
        '''
        raise NotImplemented

    @abc.abstractmethod
    def __makenew__(self):
        r'''Makes new maker.

        Returns new maker.
        '''
        raise NotImplemented
