from abjad.tools import datastructuretools
from abjad.tools import lilypondfiletools
from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lilypond_file',
        '_previous_metadata',
        '_metadata',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        self._lilypond_file = None

    ### SPECIAL METHODS ###

    def __call__(
        self,
        metadata=None,
        previous_metadata=None,
        ):
        r'''Calls segment-maker.

        Returns LilyPond file.
        '''
        metadata = datastructuretools.TypedOrderedDict(
            metadata)
        previous_metadata = datastructuretools.TypedOrderedDict(
            previous_metadata)
        self._metadata = metadata
        self._previous_metadata = previous_metadata
        lilypond_file = self._make_lilypond_file()
        assert isinstance(lilypond_file, lilypondfiletools.LilyPondFile)
        self._lilypond_file = lilypond_file
        return self._lilypond_file, self._metadata

    def __eq__(self, expr):
        r'''Is true if `expr` is a segment-maker with equivalent properties.
        '''
        from abjad.tools import systemtools
        return systemtools.TestManager.compare_objects(self, expr)

    def __hash__(self):
        r'''Hashes segment-maker.
        '''
        from abjad.tools import systemtools
        hash_values = systemtools.StorageFormatAgent(self).get_hash_values()
        return hash(hash_values)

    def __illustrate__(self, **kwargs):
        r'''Illustrates segment-maker.

        Returns LilyPond file.
        '''
        lilypond_file, metadata = self(**kwargs)
        return lilypond_file
