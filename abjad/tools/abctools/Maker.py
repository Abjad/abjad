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

    # TODO: uncomment this after __makenew__ integration
#    @abc.abstractmethod
#    def __makenew__(self):
#        raise NotImplemented
