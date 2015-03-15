# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class DurationSpellingSpecifier(AbjadValueObject):
    r'''Duration spelling specifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_decrease_durations_monotonically',
        '_forbid_meter_rewriting',
        '_forbidden_written_duration',
        '_spell_metrically',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_durations_monotonically=True,
        forbid_meter_rewriting=None,
        forbidden_written_duration=None,
        spell_metrically=None,
        ):
        assert isinstance(decrease_durations_monotonically, bool)
        if forbidden_written_duration is not None:
            forbidden_written_duration = durationtools.Duration(
                forbidden_written_duration)
        self._decrease_durations_monotonically = decrease_durations_monotonically
        self._forbidden_written_duration = forbidden_written_duration
        if spell_metrically is not None and spell_metrically != 'unassignable':
            assert isinstance(spell_metrically, bool)
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

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='decrease_durations_monotonically',
                command='ddm',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='forbidden_written_duration',
                command='fwd',
                editor=idetools.getters.get_duration,
                ),
            systemtools.AttributeDetail(
                name='spell_metrically',
                command='sm',
                editor=idetools.getters.get_boolean,
                ),
            systemtools.AttributeDetail(
                name='forbid_meter_rewriting',
                command='fmr',
                editor=idetools.getters.get_boolean,
                ),
            )

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