import typing

from .attach import attach
from .iterate import Iteration
from .lilypondfile import LilyPondFile
from .ordereddict import OrderedDict
from .overrides import LilyPondLiteral
from .parentage import Parentage
from .score import Context, Score
from .select import Selection
from .storage import StorageFormatManager
from .tag import Tag
from .timespan import TimespanList


class SegmentMaker:
    """
    Segment-maker.
    """

    ### CLASS VARIABLES ###

    __documentation_section__: typing.Optional[str] = "Segment-makers"

    __slots__ = (
        "_container_to_part_assignment",
        "_environment",
        "_lilypond_file",
        "_metadata",
        "_persist",
        "_previous_metadata",
        "_previous_persist",
        "_score",
        "_segment_directory",
    )

    ### INITIALIZER ###

    def __init__(self):
        self._container_to_part_assignment: typing.Optional[OrderedDict] = None
        self._environment: typing.Optional[str] = None
        self._lilypond_file: typing.Optional[LilyPondFile] = None
        self._metadata = OrderedDict()
        self._persist = OrderedDict()
        self._previous_metadata: typing.Optional[OrderedDict] = None
        self._previous_persist: typing.Optional[OrderedDict] = None
        self._score: typing.Optional[Score] = None
        self._segment_directory = None

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        """
        Is true if ``expr`` is a segment-maker with equivalent properties.
        """
        return StorageFormatManager.compare_objects(self, expr)

    def __hash__(self):
        """
        Hashes segment-maker.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        return hash(hash_values)

    def __illustrate__(self, **keywords) -> LilyPondFile:
        """
        Illustrates segment-maker.
        """
        lilypond_file = self.run(**keywords)
        return lilypond_file

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _check_duplicate_part_assignments(self):
        dictionary = self._container_to_part_assignment
        if not dictionary:
            return
        if not self.score_template:
            return
        part_manifest = self.score_template.part_manifest
        if not part_manifest:
            return
        part_to_timespans = OrderedDict()
        for identifier, (part_assignment, timespan) in dictionary.items():
            for part in part_manifest.expand(part_assignment):
                if part.name not in part_to_timespans:
                    part_to_timespans[part.name] = []
                part_to_timespans[part.name].append(timespan)
        messages = []
        for part_name, timespans in part_to_timespans.items():
            if len(timespans) <= 1:
                continue
            timespan_list = TimespanList(timespans)
            if timespan_list.compute_logical_and():
                message = f"  Part {part_name!r} is assigned"
                message += " to overlapping containers ..."
                messages.append(message)
        if messages:
            message = "\n" + "\n".join(messages)
            raise Exception(message)

    def _make_global_context(self):
        global_rests = Context(lilypond_type="GlobalRests", name="Global_Rests")
        global_skips = Context(lilypond_type="GlobalSkips", name="Global_Skips")
        global_context = Context(
            [global_rests, global_skips],
            lilypond_type="GlobalContext",
            simultaneous=True,
            name="Global_Context",
        )
        return global_context

    def _make_lilypond_file(self, midi=False):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def environment(self) -> typing.Optional[str]:
        """
        Gets environment.
        """
        return self._environment

    @property
    def metadata(self) -> OrderedDict:
        """
        Gets segment metadata after run.
        """
        return self._metadata

    @property
    def persist(self) -> OrderedDict:
        """
        Gets segment persist after run.
        """
        return self._persist

    @property
    def score(self) -> typing.Optional[Score]:
        """
        Gets score.
        """
        return self._score

    @property
    def segment_directory(self):
        """
        Gets segment directory.
        """
        return self._segment_directory

    @property
    def segment_name(self) -> typing.Optional[str]:
        """
        Gets segment name.
        """
        if self.segment_directory is not None:
            return self.segment_directory.name
        return None

    ### PUBLIC METHODS ###

    @staticmethod
    def comment_measure_numbers(score):
        """
        Comments measure numbers in ``score``.
        """
        offset_to_measure_number = {}
        for context in Iteration(score).components(Context):
            if not context.simultaneous:
                break
        site = Tag("abjad.SegmentMaker.comment_measure_numbers()")
        measures = Selection(context).leaves().group_by_measure()
        for i, measure in enumerate(measures):
            measure_number = i + 1
            first_leaf = Selection(measure).leaf(0)
            start_offset = first_leaf._get_timespan().start_offset
            offset_to_measure_number[start_offset] = measure_number
        for leaf in Iteration(score).leaves():
            offset = leaf._get_timespan().start_offset
            measure_number = offset_to_measure_number.get(offset, None)
            if measure_number is None:
                continue
            context = Parentage(leaf).get(Context)
            if context.name is None:
                string = f"% [{context.lilypond_type} measure {measure_number}]"
            else:
                string = f"% [{context.name} measure {measure_number}]"
            literal = LilyPondLiteral(string, "absolute_before")
            tag = Tag("COMMENT_MEASURE_NUMBERS").append(site)
            attach(literal, leaf, tag=tag)

    def run(
        self,
        activate: typing.List[Tag] = None,
        deactivate: typing.List[Tag] = None,
        do_not_print_timing: bool = None,
        environment: str = None,
        metadata: OrderedDict = None,
        midi: bool = None,
        persist: OrderedDict = None,
        previous_metadata: OrderedDict = None,
        previous_persist: OrderedDict = None,
        remove: typing.List[Tag] = None,
        segment_directory=None,
    ) -> LilyPondFile:
        """
        Runs segment-maker.
        """
        self._metadata = OrderedDict(metadata)
        self._persist = OrderedDict(persist)
        self._previous_metadata = OrderedDict(previous_metadata)
        self._previous_persist = OrderedDict(previous_persist)
        lilypond_file = self._make_lilypond_file(midi=midi)
        self._lilypond_file = lilypond_file
        assert isinstance(self._lilypond_file, LilyPondFile)
        return self._lilypond_file
