import abc
from abjad.tools.abctools.AbjadObject.AbjadObject import AbjadObject


class Maker(AbjadObject):
    '''Abstract base class for all maker classers.'''

    ### SPECIAL METHODS ###

    def __call__(self):
        raise NotImplemented

    ### PUBLIC METHODS ###

    def new(self):
        raise NotImplemented
