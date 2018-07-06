import typing
from abjad.lilypondnames.LilyPondContextSetting import LilyPondContextSetting
from abjad.scheme import SchemeSymbol
from .Spanner import Spanner


class PianoPedalSpanner(Spanner):
    r"""
    Piano pedal spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.PianoPedalSpanner()
        >>> abjad.tweak(spanner).color = 'blue'
        >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.pedalSustainStyle = #'mixed
                c'8
                - \tweak SustainPedalLineSpanner.staff-padding #5
                - \tweak color #blue
                \sustainOn
                d'8
                e'8
                f'8
                \sustainOff
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kind',
        '_style',
        )

    _kinds = {
        'sustain': (r'\sustainOn', r'\sustainOff'),
        'sostenuto': (r'\sostenutoOn', r'\sostenutoOff'),
        'corda': (r'\unaCorda', r'\treCorde'),
        }

    _styles = (
        'text',
        'bracket',
        'mixed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        kind: str = 'sustain',
        style: str = 'mixed',
        ) -> None:
        Spanner.__init__(self)
        if kind not in list(self._kinds.keys()):
            raise ValueError(f'kind must be in {list(self._kinds.keys())!r}.')
        self._kind = kind
        if style not in self._styles:
            raise ValueError(f'style must be in {self._styles!r}.')
        self._style = style

    ### PRIVATE PROPERTIES ##

    @property
    def _start_command(self):
        return self._kinds[self.kind][0]

    @property
    def _stop_command(self):
        return self._kinds[self.kind][1]

    ### PRIVATE METHODS ###

    def _copy_keywords(self, new):
        new._kind = self.kind
        new._style = self.style

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only(leaf):
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
            string = self._stop_command_string()
            bundle.after.spanner_starts.append(string)
        elif leaf is self[0]:
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            strings = self._tweaked_start_command_strings()
            bundle.after.spanner_starts.extend(strings)
        elif leaf is self[-1]:
            string = self._stop_command_string()
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self) -> str:
        r"""
        Gets kind of piano pedal spanner.

        ..  container:: example

            Sustain pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sustain')
            >>> abjad.tweak(spanner).color = 'blue'
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    - \tweak color #blue
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Sostenuto pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sostenuto')
            >>> abjad.tweak(spanner).color = 'blue'
            >>> abjad.tweak(spanner).sostenuto_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SostenutoPedalLineSpanner.staff-padding #5
                    - \tweak color #blue
                    \sostenutoOn
                    d'8
                    e'8
                    f'8
                    \sostenutoOff
                }

        ..  container:: example

            Una corda / tre corde pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='corda')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff[0]).staff.una_corda_pedal.color = 'blue'
            >>> abjad.override(staff[0]).staff.una_corda_pedal_line_spanner.staff_padding = 5
            >>> abjad.override(staff[-1]).staff.una_corda_pedal.color = 'blue'
            >>> abjad.override(staff[-1]).staff.una_corda_pedal_line_spanner.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \once \override Staff.UnaCordaPedal.color = #blue
                    \once \override Staff.UnaCordaPedalLineSpanner.staff-padding = #5
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \unaCorda
                    d'8
                    e'8
                    \once \override Staff.UnaCordaPedal.color = #blue
                    \once \override Staff.UnaCordaPedalLineSpanner.staff-padding = #5
                    f'8
                    \treCorde
                }

            Note that when no visible bracket connects start-text and stop-text
            indications (as above) that the first and last leaves in spanner
            must be overriden independently. (Note also that ``abjad.tweak()``
            will apply to only the pedal-down indication and will leave the
            pedal-up indication unmodified.)

        Returns ``'sustain'``, ``'sostenuto'`` or ``'corda'``.
        """
        return self._kind

    @property
    def style(self) -> str:
        r"""
        Gets style of piano pedal spanner.

        ..  container:: example

            Mixed style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='mixed')
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Bracket style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='bracket')
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'bracket
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Text style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='text')
            >>> abjad.override(staff[0]).staff.sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.override(staff[-1]).staff.sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \once \override Staff.SustainPedalLineSpanner.staff-padding = #5
                    \set Staff.pedalSustainStyle = #'text
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    \once \override Staff.SustainPedalLineSpanner.staff-padding = #5
                    f'8
                    \sustainOff
                }

            Note that when no visible bracket connects start-text and stop-text
            indications (as above) that the first and last leaves in spanner
            must be overriden independently. (Note also that ``abjad.tweak()``
            will apply to only the pedal-down indication and will leave the
            pedal-up indication unmodified.)

        Returns ``'mixed'``, ``'bracket'`` or ``'text'``.
        """
        return self._style
