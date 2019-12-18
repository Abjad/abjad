import typing

from abjad import const
from abjad.core.Container import Container
from abjad.core.Context import Context
from abjad.core.Score import Score
from abjad.core.Staff import Staff
from abjad.core.Voice import Voice
from abjad.lilypondfile.LilyPondFile import LilyPondFile
from abjad.system.StorageFormatManager import StorageFormatManager
from abjad.system.Tag import Tag
from abjad.timespans import TimespanList
from abjad.top.inspect import inspect
from abjad.top.iterate import iterate
from abjad.utilities.OrderedDict import OrderedDict
from abjad.utilities.String import String

from .PartAssignment import PartAssignment
from .Path import Path


class SegmentMaker(object):
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
        self._segment_directory: typing.Optional[Path] = None

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        """
        Is true if ``expr`` is a segment-maker with equivalent properties.
        """
        return StorageFormatManager.compare_objects(self, expr)

    def __format__(self, format_specification="") -> str:
        """
        Formats object.
        """
        return StorageFormatManager(self).get_storage_format()

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

    def _add_container_identifiers(self):
        if self.environment == "docs" and not getattr(
            self, "test_container_identifiers", False
        ):
            return
        segment_name = self.segment_name or ""
        segment_name = String(segment_name).to_segment_lilypond_identifier()
        contexts = []
        try:
            context = self.score["Global_Skips"]
            contexts.append(context)
        except ValueError:
            pass
        try:
            context = self.score["Global_Rests"]
            contexts.append(context)
        except ValueError:
            pass
        for voice in iterate(self.score).components(Voice):
            if inspect(voice).has_indicator(const.INTERMITTENT):
                continue
            contexts.append(voice)
        container_to_part_assignment = OrderedDict()
        context_name_counts = {}
        for context in contexts:
            if context.name is None:
                message = "all contexts must be named:\n"
                message += f"    {repr(context)}"
                raise Exception(message)
            count = context_name_counts.get(context.name, 0)
            if count == 0:
                suffixed_context_name = context.name
            else:
                suffix = String.base_26(count)
                suffixed_context_name = f"{context.name}_{suffix}"
            context_name_counts[context.name] = count + 1
            if segment_name:
                context_identifier = f"{segment_name}_{suffixed_context_name}"
            else:
                context_identifier = suffixed_context_name
            context.identifier = f"%*% {context_identifier}"
            part_container_count = 0
            for container in iterate(context).components(Container):
                if not container.identifier:
                    continue
                if container.identifier.startswith("%*% Part"):
                    part_container_count += 1
                    part = container.identifier.strip("%*% ")
                    globals_ = globals()
                    globals_["PartAssignment"] = PartAssignment
                    part = eval(part, globals_)
                    suffix = String().base_26(part_container_count).lower()
                    container_identifier = f"{context_identifier}_{suffix}"
                    container_identifier = String(container_identifier)
                    assert container_identifier.is_lilypond_identifier()
                    assert container_identifier not in container_to_part_assignment
                    timespan = inspect(container).timespan()
                    pair = (part, timespan)
                    container_to_part_assignment[container_identifier] = pair
                    container.identifier = f"%*% {container_identifier}"
        for staff in iterate(self.score).components(Staff):
            if segment_name:
                context_identifier = f"{segment_name}_{staff.name}"
            else:
                context_identifier = staff.name
            staff.identifier = f"%*% {context_identifier}"
        self._container_to_part_assignment = container_to_part_assignment

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
    def segment_directory(self) -> typing.Optional[Path]:
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
        import abjad

        offset_to_measure_number = {}
        for context in abjad.iterate(score).components(abjad.Context):
            if not context.simultaneous:
                break
        site = "abjad.SegmentMaker.comment_measure_numbers()"
        measures = abjad.select(context).leaves().group_by_measure()
        for i, measure in enumerate(measures):
            measure_number = i + 1
            first_leaf = abjad.select(measure).leaf(0)
            start_offset = abjad.inspect(first_leaf).timespan().start_offset
            offset_to_measure_number[start_offset] = measure_number
        for leaf in abjad.iterate(score).leaves():
            offset = abjad.inspect(leaf).timespan().start_offset
            measure_number = offset_to_measure_number.get(offset, None)
            if measure_number is None:
                continue
            context = abjad.inspect(leaf).parentage().get(abjad.Context)
            if context.name is None:
                string = f"% [{context.lilypond_type} measure {measure_number}]"
            else:
                string = f"% [{context.name} measure {measure_number}]"
            literal = abjad.LilyPondLiteral(string, "absolute_before")
            tag = abjad.Tag("COMMENT_MEASURE_NUMBERS").append(site)
            abjad.attach(literal, leaf, tag=tag)

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
        segment_directory: Path = None,
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
