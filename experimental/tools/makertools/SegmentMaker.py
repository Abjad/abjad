# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import lilypondfiletools
from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker baseclass.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_file',
        '_previous_segment_metadata',
        '_segment_metadata',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        self._lilypond_file = None

    ### SPECIAL METHODS ###

    def __call__(
        self, 
        segment_metadata=None, 
        previous_segment_metadata=None,
        ):
        r'''Calls segment-maker.

        Returns LilyPond file.
        '''
        segment_metadata = datastructuretools.TypedOrderedDict(
            segment_metadata)
        previous_segment_metadata = datastructuretools.TypedOrderedDict(
            previous_segment_metadata)
        self._segment_metadata = segment_metadata
        self._previous_segment_metadata = previous_segment_metadata
        lilypond_file = self._make_lilypond_file()
        assert isinstance(lilypond_file, lilypondfiletools.LilyPondFile)
        self._lilypond_file = lilypond_file
        return self._lilypond_file, self._segment_metadata

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

    def __illustrate__(self, **kwargs):
        r'''Illustrates segment-maker.

        Returns LilyPond file.
        '''
        lilypond_file, metadata = self(**kwargs)
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_file(self):
        r'''Gets segment LilyPond file.

        Created when segment-maker is called.

        Returns LilyPond file.
        '''
        return self._lilypond_file