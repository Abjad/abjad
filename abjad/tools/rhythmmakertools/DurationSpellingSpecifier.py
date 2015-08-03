# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSpellingSpecifier(AbjadValueObject):
    r'''Duration spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_decrease_durations_monotonically',
        '_forbid_meter_rewriting',
        '_forbidden_written_duration',
        '_rewrite_meter',
        '_spell_metrically',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_durations_monotonically=True,
        forbid_meter_rewriting=None,
        forbidden_written_duration=None,
        rewrite_meter=None,
        spell_metrically=None,
        ):
        from abjad.tools import rhythmmakertools
        assert isinstance(decrease_durations_monotonically, bool)
        if forbidden_written_duration is not None:
            forbidden_written_duration = durationtools.Duration(
                forbidden_written_duration)
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically
        self._forbidden_written_duration = forbidden_written_duration
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

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> print(format(specifier))
                rhythmmakertools.DurationSpellingSpecifier(
                    decrease_durations_monotonically=True,
                    )

        Returns string.
        '''
        return AbjadValueObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of duration spelling specifier.

        ..  container:: example

            ::

                >>> rhythmmakertools.DurationSpellingSpecifier()
                DurationSpellingSpecifier(decrease_durations_monotonically=True)

        Returns string.
        '''
        return AbjadValueObject.__repr__(self)

    ### PRIVATE METHODS ###

    @staticmethod
    def _rewrite_meter_(
        selections, 
        meters, 
        reference_meters=None,
        rewrite_tuplets=False,
        use_messiaen_style_ties=False,
        ):
        from abjad.tools import metertools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import mutate
        meters = [metertools.Meter(_) for _ in meters]
        durations = [durationtools.Duration(_) for _ in meters]
        reference_meters = reference_meters or ()
        selections = DurationSpellingSpecifier._split_at_measure_boundaries(
            selections,
            meters,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        measures = scoretools.make_spacer_skip_measures(durations)
        staff = scoretools.Staff(measures)
        mutate(staff).replace_measure_contents(selections)
        for measure, meter in zip(staff, meters):
            for reference_meter in reference_meters:
                if str(reference_meter) == str(meter):
                    meter = reference_meter
                    break
            mutate(measure[:]).rewrite_meter(
                meter,
                rewrite_tuplets=rewrite_tuplets,
                use_messiaen_style_ties=use_messiaen_style_ties,
                )
        selections = []
        for measure in staff:
            selections.append(measure[:])
        return selections

    @staticmethod
    def _split_at_measure_boundaries(
        selections, 
        meters,
        use_messiaen_style_ties=False,
        ):
        from abjad.tools import metertools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import inspect_
        from abjad.tools.topleveltools import mutate
        meters = [metertools.Meter(_) for _ in meters]
        durations = [durationtools.Duration(_) for _ in meters]
        music = sequencetools.flatten_sequence(selections)
        assert isinstance(music, list), repr(music)
        total_duration = sum(durations)
        music_duration = sum(inspect_(_).get_duration() for _ in music)
        assert total_duration == music_duration
        voice = scoretools.Voice(music)
        mutate(voice[:]).split(
            durations=durations,
            tie_split_notes=True,
            use_messiaen_style_ties=use_messiaen_style_ties,
            )
        selections = list(voice[:])
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''Is true when all durations should be spelled as a tied series of
        monotonically decreasing values. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.decrease_durations_monotonically
                True

        Defaults to true.

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def forbid_meter_rewriting(self):
        r'''Is true when meter rewriting is forbidden.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.forbid_meter_rewriting is None
                True

        Defaults to none.

        Returns boolean or none.
        '''
        return self._forbid_meter_rewriting

    @property
    def forbidden_written_duration(self):
        r'''Gets forbidden written duration.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.forbidden_written_duration is None
                True

        Defaults to none.

        Returns duration or none.
        '''
        return self._forbidden_written_duration

    @property
    def rewrite_meter(self):
        r'''Is true when all output divisions should rewrite meter.
        Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
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

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.spell_metrically is None
                True

        Spells unassignable durations like ``5/16`` and ``9/4`` metrically when
        set to ``'unassignable'``. Leaves other durations unchanged.

        Defaults to none.

        Returns boolean, ``'unassignable'`` or none..
        '''
        return self._spell_metrically