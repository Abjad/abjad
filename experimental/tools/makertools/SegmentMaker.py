# -*- encoding: utf-8 -*-
from abjad.tools import lilypondfiletools
from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker baseclass.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_file',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        ):
        self._lilypond_file = None
        self._name = name

    ### SPECIAL METHODS ###

    def __call__(self, metadata=None):
        r'''Calls segment-maker.

        Returns LilyPond file.
        '''
        lilypond_file = self._make_lilypond_file()
        assert isinstance(lilypond_file, lilypondfiletools.LilyPondFile)
        self._lilypond_file = lilypond_file
        sticky_settings = {}
        return self._lilypond_file, sticky_settings

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
        lilypond_file, sticky_settings = self()
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_file(self):
        r'''Gets segment LilyPond file.

        Created when segment-maker is called.

        Returns LilyPond file.
        '''
        return self._lilypond_file

    @property
    def name(self):
        r'''Gets segment name.

        Returns string or none.
        '''
        return self._name