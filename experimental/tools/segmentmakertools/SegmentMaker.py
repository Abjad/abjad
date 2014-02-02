# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker baseclass.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self, divisions=None):
        r'''Calls segment-maker.

        Returns LilyPond file.
        '''
        music = self._make_music(divisions=divisions)
        return music

    ### PRIVATE METHODS ##

    @abc.abstractmethod
    def _make_music(self, divisions=None):
        pass
