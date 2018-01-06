from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentMaker(AbjadObject):
    r'''Segment-maker.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    __slots__ = (
        '_documents_metadata',
        '_lilypond_file',
        '_previous_metadata',
        '_metadata',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._documents_metadata = None
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

    def __illustrate__(self, **keywords):
        r'''Illustrates segment-maker.

        Returns LilyPond file.
        '''
        lilypond_file = self(**keywords)
        return lilypond_file

    ### PRIVATE METHODS ###
    
    def _make_global_context(self):
        import abjad
        global_rests = abjad.Context(
            context_name='GlobalRests',
            name='GlobalRests',
            )
        global_skips = abjad.Context(
            context_name='GlobalSkips',
            name='GlobalSkips',
            )
        global_context = abjad.Context(
            [global_rests, global_skips ],
            context_name='GlobalContext',
            is_simultaneous=True,
            name='GlobalContext',
            )
        return global_context

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
        documents_metadata=None,
        metadata=None,
        midi=None,
        previous_metadata=None,
        ):
        r'''Runs segment-maker.

        Returns LilyPond file.
        '''
        import abjad
        self._documents_metadata = abjad.TypedOrderedDict(documents_metadata)
        self._metadata = abjad.TypedOrderedDict(metadata)
        self._previous_metadata = abjad.TypedOrderedDict(previous_metadata)
        lilypond_file = self._make_lilypond_file(midi=midi)
        assert isinstance(lilypond_file, abjad.LilyPondFile)
        self._lilypond_file = lilypond_file
        return self._lilypond_file
