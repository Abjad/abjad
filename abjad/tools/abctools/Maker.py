# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Maker(AbjadObject):
    r'''Abstract base class for all maker classers.
    '''

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self):
        raise NotImplemented

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def new(self):
        raise NotImplemented
