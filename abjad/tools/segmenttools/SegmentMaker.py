from typing import List
from typing import Union as U
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.lilypondfiletools.LilyPondFile import LilyPondFile


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
            lilypond_type='GlobalRests',
            name='GlobalRests',
            )
        global_skips = abjad.Context(
            lilypond_type='GlobalSkips',
            name='GlobalSkips',
            )
        global_context = abjad.Context(
            [global_rests, global_skips ],
            lilypond_type='GlobalContext',
            is_simultaneous=True,
            name='GlobalContext',
            )
        return global_context

    def _make_lilypond_file(self, midi=False):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def metadata(self):
        r'''Gets segment metadata after run.

        Returns ordered dictionary or none.
        '''
        return self._metadata

    ### PUBLIC METHODS ###

    def run(
        self,
        deactivate: U[List[str], None] = None,
        environment: U[str, None] = None,
        metadata: U[OrderedDict, None] = None,
        midi: U[bool, None] = None,
        previous_metadata: U[OrderedDict, None] = None,
        remove: U[List[str], None] = None,
        ) -> LilyPondFile:
        r'''Runs segment-maker.
        '''
        self._metadata = OrderedDict(metadata)
        self._previous_metadata = OrderedDict(previous_metadata)
        lilypond_file = self._make_lilypond_file(midi=midi)
        self._lilypond_file: LilyPondFile = lilypond_file
        return self._lilypond_file
