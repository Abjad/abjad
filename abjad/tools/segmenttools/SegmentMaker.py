from typing import List
from typing import Optional
from typing import Union as U
from .Path import Path
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from abjad.tools.datastructuretools.String import String
from abjad.tools.indicatortools.Part import Part
from abjad.tools.lilypondfiletools.LilyPondFile import LilyPondFile
from abjad.tools.scoretools.Container import Container
from abjad.tools.scoretools.Context import Context
from abjad.tools.scoretools.Score import Score
from abjad.tools.scoretools.Staff import Staff
from abjad.tools.scoretools.Voice import Voice
from abjad.tools.topleveltools.inspect import inspect
from abjad.tools.topleveltools.iterate import iterate


class SegmentMaker(AbjadObject):
    r'''Segment-maker.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-makers'

    __slots__ = (
        '_container_to_part',
        '_environment',
        '_lilypond_file',
        '_metadata',
        '_previous_metadata',
        '_score',
        '_segment_directory',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._container_to_part: OrderedDict = None
        self._environment: str = None
        self._lilypond_file: LilyPondFile = None
        self._metadata: OrderedDict = None
        self._previous_metadata: OrderedDict = None
        self._score: Score = None
        self._segment_directory: Path = None

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

    def _add_container_identifiers(self):
        if getattr(self, '_environment', None) == 'docs':
            return
        segment_name = self.segment_name or ''
        segment_name = String(segment_name).to_segment_lilypond_identifier()
        contexts = []
        try:
            context = self.score['GlobalSkips']
            contexts.append(context)
        except ValueError:
            pass
        try:
            context = self.score['GlobalRests']
            contexts.append(context)
        except ValueError:
            pass
        for voice in iterate(self.score).components(Voice):
            contexts.append(voice)
        container_to_part = OrderedDict()
        for context in contexts:
            if segment_name:
                context_identifier = f'{segment_name}_{context.name}'
            else:
                context_identifier = context.name
            context.identifier = f'%*% {context_identifier}'
            part_container_count = 0
            for container in iterate(context).components(Container):
                if not container.identifier:
                    continue
                if container.identifier.startswith('%*% Part'):
                    part_container_count += 1
                    globals_ = globals()
                    part = container.identifier.strip('%*% ')
                    part = eval(part, globals_)
                    suffix = String().base_26(part_container_count).lower()
                    container_identifier = f'{context_identifier}_{suffix}'
                    container_identifier = String(container_identifier)
                    assert container_identifier.is_lilypond_identifier()
                    assert container_identifier not in container_to_part
                    timespan = inspect(container).get_timespan()
                    pair = (part, timespan)
                    container_to_part[container_identifier] = pair
                    container.identifier = f'%*% {container_identifier}'
        for staff in iterate(self.score).components(Staff):
            if segment_name:
                context_identifier = f'{segment_name}_{staff.name}'
            else:
                context_identifier = staff.name
            staff.identifier = f'%*% {context_identifier}'
        self._container_to_part = container_to_part

    def _make_global_context(self):
        global_rests = Context(
            lilypond_type='GlobalRests',
            name='GlobalRests',
            )
        global_skips = Context(
            lilypond_type='GlobalSkips',
            name='GlobalSkips',
            )
        global_context = Context(
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

    @property
    def score(self) -> Optional[Score]:
        r'''Gets score.
        '''
        return self._score

    @property
    def segment_directory(self) -> Optional[Path]:
        r'''Gets segment directory.
        '''
        return self._segment_directory

    @property
    def segment_name(self) -> Optional[str]:
        r'''Gets segment name.
        '''
        if bool(self.segment_directory):
            return self.segment_directory.name
        return None

    ### PUBLIC METHODS ###

    def run(
        self,
        deactivate: List[str] = None,
        environment: str = None,
        metadata: OrderedDict = None,
        midi: bool = None,
        previous_metadata: OrderedDict = None,
        remove: List[str] = None,
        segment_directory: Path = None,
        ) -> LilyPondFile:
        r'''Runs segment-maker.
        '''
        self._metadata = OrderedDict(metadata)
        self._previous_metadata = OrderedDict(previous_metadata)
        lilypond_file = self._make_lilypond_file(midi=midi)
        self._lilypond_file: LilyPondFile = lilypond_file
        return self._lilypond_file
