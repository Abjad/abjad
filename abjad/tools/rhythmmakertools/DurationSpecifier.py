from abjad.tools.abctools import AbjadValueObject


class DurationSpecifier(AbjadValueObject):
    r'''Duration spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_decrease_monotonic',
        '_forbid_meter_rewriting',
        '_forbidden_duration',
        '_rewrite_meter',
        '_spell_metrically',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_monotonic=True,
        forbid_meter_rewriting=None,
        forbidden_duration=None,
        rewrite_meter=None,
        spell_metrically=None,
        ):
        import abjad
        from abjad.tools import rhythmmakertools
        assert isinstance(decrease_monotonic, bool)
        self._decrease_monotonic = decrease_monotonic
        if forbidden_duration is not None:
            forbidden_duration = abjad.Duration(forbidden_duration)
        self._forbidden_duration = forbidden_duration
        assert isinstance(rewrite_meter, (bool, type(None)))
        self._rewrite_meter = rewrite_meter
        assert (spell_metrically is None or
            isinstance(spell_metrically, bool) or
            spell_metrically == 'unassignable' or
            isinstance(spell_metrically, rhythmmakertools.PartitionTable))
        self._spell_metrically = spell_metrically
        if forbid_meter_rewriting is not None:
            forbid_meter_rewriting = bool(forbid_meter_rewriting)
        self._forbid_meter_rewriting = forbid_meter_rewriting

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats duration spelling specifier.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> abjad.f(specifier)
            abjad.rhythmmakertools.DurationSpecifier(
                decrease_monotonic=True,
                )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            >>> abjad.rhythmmakertools.DurationSpecifier()
            DurationSpecifier(decrease_monotonic=True)

        Returns string.
        '''
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
        from abjad.tools.topleveltools import mutate
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
        mutate(staff).replace_measure_contents(selections)
        for measure, meter in zip(staff, meters):
            for reference_meter in reference_meters:
                if str(reference_meter) == str(meter):
                    meter = reference_meter
                    break
            mutate(measure[:]).rewrite_meter(
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
            message = 'Duration of meters is {!s}'
            message += ' but duration of selections is {!s}:'
            message = message.format(meter_duration, music_duration)
            message += '\nmeters: {}.'.format(meters)
            message += '\nmusic: {}.'.format(selections)
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
    def decrease_monotonic(self):
        r'''Is true when all durations should be spelled as a tied series of
        monotonically decreasing values. Otherwise false.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> specifier.decrease_monotonic
            True

        Defaults to true.

        Returns true or false.
        '''
        return self._decrease_monotonic

    @property
    def forbid_meter_rewriting(self):
        r'''Is true when meter rewriting is forbidden.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> specifier.forbid_meter_rewriting is None
            True

        Defaults to none.

        Returns boolean or none.
        '''
        return self._forbid_meter_rewriting

    @property
    def forbidden_duration(self):
        r'''Gets forbidden written duration.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> specifier.forbidden_duration is None
            True

        Defaults to none.

        Returns duration or none.
        '''
        return self._forbidden_duration

    @property
    def rewrite_meter(self):
        r'''Is true when all output divisions should rewrite meter.
        Otherwise false.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> specifier.rewrite_meter is None
            True

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._rewrite_meter

    @property
    def spell_metrically(self):
        r'''Is true when durations should spell according to approximate common
        practice understandings of meter. Otherwise false.

        ..  container:: example

            >>> specifier = abjad.rhythmmakertools.DurationSpecifier()
            >>> specifier.spell_metrically is None
            True

        Spells unassignable durations like ``5/16`` and ``9/4`` metrically when
        set to ``'unassignable'``. Leaves other durations unchanged.

        Defaults to none.

        Returns boolean, ``'unassignable'`` or none..
        '''
        return self._spell_metrically
