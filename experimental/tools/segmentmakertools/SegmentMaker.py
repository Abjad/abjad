# -*- encoding: utf-8 -*-
import abc
from abjad.tools import lilypondfiletools
from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker baseclass.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_score',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        ):
        self._name = name
        self._score = None

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls segment-maker.

        Returns LilyPond file.
        '''
        music = self._make_music()
        assert isinstance(music, lilypondfiletools.LilyPondFile)
        return music

    def __eq__(self, expr):
        r'''Is true if `expr` is a segment-maker with equivalent properties.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes segment-maker.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatManager.get_hash_values(self)
        return hash(hash_values)

    def __illustrate__(self):
        r'''Illustrates segment-maker.

        Returns LilyPond file.
        '''
        return self()

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Gets segment name.

        Returns string.
        '''
        return self._name

    @property
    def score(self):
        r'''Gets segment score.

        Returns score.
        '''
        return self._score
