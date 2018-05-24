import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.Duration import Duration
from .PartitionTable import PartitionTable


class DurationSpecifier(AbjadValueObject):
    """
    Duration specifier.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_decrease_monotonic',
        '_forbid_meter_rewriting',
        '_forbidden_duration',
        '_rewrite_meter',
        '_rewrite_rest_filled',
        '_spell_metrically',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        decrease_monotonic: bool = True,
        forbid_meter_rewriting: bool = None,
        forbidden_duration: typing.Union[tuple, Duration] = None,
        rewrite_meter: bool = None,
        rewrite_rest_filled: bool = None,
        spell_metrically: typing.Union[bool, str, PartitionTable] = None,
        ) -> None:
        if decrease_monotonic is not None:
            decrease_monotonic = bool(decrease_monotonic)
        self._decrease_monotonic = decrease_monotonic
        if forbidden_duration is None:
            forbidden_duration_ = None
        else:
            forbidden_duration_ = Duration(forbidden_duration)
        self._forbidden_duration = forbidden_duration_
        if rewrite_meter is not None:
            rewrite_meter = bool(rewrite_meter)
        self._rewrite_meter = rewrite_meter
        if rewrite_rest_filled is not None:
            rewrite_rest_filled = bool(rewrite_rest_filled)
        self._rewrite_rest_filled = rewrite_rest_filled
        assert (spell_metrically is None or
            isinstance(spell_metrically, bool) or
            spell_metrically == 'unassignable' or
            isinstance(spell_metrically, PartitionTable))
        self._spell_metrically = spell_metrically
        if forbid_meter_rewriting is not None:
            forbid_meter_rewriting = bool(forbid_meter_rewriting)
        self._forbid_meter_rewriting = forbid_meter_rewriting

    ### SPECIAL METHODS ###

    def __format__(self, format_specification='') -> str:
        """
        Formats duration specifier.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> abjad.f(specifier)
            abjad.rmakers.DurationSpecifier(
                decrease_monotonic=True,
                )

        """
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self) -> str:
        """
        Gets interpreter representation.

        ..  container:: example

            >>> abjad.rmakers.DurationSpecifier()
            DurationSpecifier(decrease_monotonic=True)

        """
        return super(DurationSpecifier, self).__repr__()

    ### PRIVATE METHODS ###

    @staticmethod
    def _rewrite_meter_(
        selections,
        meters,
        reference_meters=None,
        rewrite_tuplets=False,
        repeat_ties=False,
        ):
        import abjad
        meters = [abjad.Meter(_) for _ in meters]
        durations = [abjad.Duration(_) for _ in meters]
        reference_meters = reference_meters or ()
        selections = DurationSpecifier._split_at_measure_boundaries(
            selections,
            meters,
            repeat_ties=repeat_ties,
            )
        maker = abjad.MeasureMaker()
        measures = maker(durations)
        staff = abjad.Staff(measures)
        abjad.mutate(staff).replace_measure_contents(selections)
        for measure, meter in zip(staff, meters):
            for reference_meter in reference_meters:
                if str(reference_meter) == str(meter):
                    meter = reference_meter
                    break
            abjad.mutate(measure[:]).rewrite_meter(
                meter,
                rewrite_tuplets=rewrite_tuplets,
                repeat_ties=repeat_ties,
                )
        selections = []
        for measure in staff:
            contents = measure[:]
            for component in contents:
                component._parent = None
            selections.append(contents)
        return selections

    @staticmethod
    def _rewrite_rest_filled_(
        selections,
        multimeasure_rests=None,
        ):
        import abjad
        selections_ = []
        maker = abjad.LeafMaker()
        prototype = (abjad.MultimeasureRest, abjad.Rest)
        for selection in selections:
            if not all(isinstance(_, prototype) for _ in selection):
                selections_.append(selection)
            else:
                duration = abjad.inspect(selection).get_duration()
                if multimeasure_rests:
                    multiplier = abjad.Multiplier(duration)
                    rest = abjad.MultimeasureRest(1)
                    abjad.attach(multiplier, rest, tag=None)
                    rests = abjad.select(rest)
                else:
                    rests = maker([None], [duration])
                selections_.append(rests)
        return selections_

    @staticmethod
    def _split_at_measure_boundaries(
        selections,
        meters,
        repeat_ties=False,
        ):
        import abjad
        meters = [abjad.Meter(_) for _ in meters]
        durations = [abjad.Duration(_) for _ in meters]
        selections = abjad.sequence(selections).flatten(depth=-1)
        meter_duration = sum(durations)
        music_duration = sum(
            abjad.inspect(_).get_duration() for _ in selections)
        if not meter_duration == music_duration:
            message = f'Duration of meters is {meter_duration!s}'
            message += f' but duration of selections is {music_duration!s}:'
            message += f'\nmeters: {meters}.'
            message += f'\nmusic: {selections}.'
            raise Exception(message)
        voice = abjad.Voice(selections)
        abjad.mutate(voice[:]).split(
            durations=durations,
            tie_split_notes=True,
            repeat_ties=repeat_ties,
            )
        components = abjad.mutate(voice).eject_contents()
        component_durations = [
            abjad.inspect(_).get_duration() for _ in components]
        parts = abjad.sequence(component_durations)
        parts = parts.partition_by_weights(
            weights=durations,
            allow_part_weights=abjad.Exact,
            )
        part_lengths = [len(_) for _ in parts]
        parts = abjad.sequence(components).partition_by_counts(
            counts=part_lengths,
            overhang=abjad.Exact,
            )
        selections = [abjad.select(_) for _ in parts]
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_monotonic(self) -> typing.Optional[bool]:
        """
        Is true when all durations should be spelled as a tied series of
        monotonically decreasing values.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.decrease_monotonic
            True

        """
        return self._decrease_monotonic

    @property
    def forbid_meter_rewriting(self) -> typing.Optional[bool]:
        """
        Is true when meter rewriting is forbidden.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.forbid_meter_rewriting is None
            True

        """
        return self._forbid_meter_rewriting

    @property
    def forbidden_duration(self) -> typing.Optional[Duration]:
        """
        Gets forbidden written duration.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.forbidden_duration is None
            True

        """
        return self._forbidden_duration

    @property
    def rewrite_meter(self) -> typing.Optional[bool]:
        """
        Is true when all output divisions should rewrite meter.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.rewrite_meter is None
            True

        """
        return self._rewrite_meter

    @property
    def rewrite_rest_filled(self) -> typing.Optional[bool]:
        """
        Is true when rhythm-maker rewrites rest-filled divisions.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.rewrite_rest_filled is None
            True

        """
        return self._rewrite_rest_filled

    @property
    def spell_metrically(self) -> typing.Union[bool, str, PartitionTable, None]:
        """
        Is true when durations should spell according to approximate common
        practice understandings of meter.

        ..  container:: example

            >>> specifier = abjad.rmakers.DurationSpecifier()
            >>> specifier.spell_metrically is None
            True

        Spells unassignable durations like ``5/16`` and ``9/4`` metrically when
        set to ``'unassignable'``. Leaves other durations unchanged.
        """
        return self._spell_metrically
