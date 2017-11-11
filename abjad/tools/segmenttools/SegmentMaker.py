from abjad.tools.abctools import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    __slots__ = (
        '_lilypond_file',
        '_previous_metadata',
        '_metadata',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._lilypond_file = None
        self._metadata = None
        self._previous_metadata = None

    ### SPECIAL METHODS ###


    def __eq__(self, expr):
        r'''Is true if `expr` is a segment-maker with equivalent properties.
        '''
        import abjad
        return abjad.TestManager.compare_objects(self, expr)

    def __hash__(self):
        r'''Hashes segment-maker.
        '''
        import abjad
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        return hash(hash_values)

    def __illustrate__(self, **kwargs):
        r'''Illustrates segment-maker.

        Returns LilyPond file.
        '''
        lilypond_file = self(**kwargs)
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def metadata(self):
        r'''Gets segment metadata after run.

        Returns typed ordered dictionary or none.
        '''
        return self._metadata

    ### PUBLIC METHODS ###

    def run(
        self,
        metadata=None,
        midi=None,
        previous_metadata=None,
        ):
        r'''Runs segment-maker.

        Returns LilyPond file and segment metadata.
        '''
        import abjad
        metadata = abjad.TypedOrderedDict(metadata)
        previous_metadata = abjad.TypedOrderedDict(previous_metadata)
        self._metadata = metadata
        self._previous_metadata = previous_metadata
        lilypond_file = self._make_lilypond_file(midi=midi)
        assert isinstance(lilypond_file, abjad.LilyPondFile)
        self._lilypond_file = lilypond_file
        return self._lilypond_file
