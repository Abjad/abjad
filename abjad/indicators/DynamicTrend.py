import typing
from abjad import enums
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.system.Tags import Tags
abjad_tags = Tags()


class DynamicTrend(AbjadValueObject):
    r"""
    Dynamic trend.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.DynamicTrend('<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = #4.5
            }
            {
                c'4
                \p
                \<
                d'4
                e'4
                f'4
                \f
            }

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_left_broken',
        '_shape',
        '_tweaks',
        )

    _context = 'Voice'

    _crescendo_start = r'\<'

    _decrescendo_start = r'\>'

    _format_slot = 'after'

    _known_shapes = (
        '<', 'o<', '<|', 'o<|',
        '>', '>o', '|>', '|>o',
        '--',
        )

    _time_orientation: enums.HorizontalAlignment = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        shape='<',
        *,
        left_broken: bool = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        assert shape in self._known_shapes, repr(shape)
        self._shape = shape
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### PRIVATE METHODS ###

    @staticmethod
    def _constante_hairpin():
        return LilyPondGrobOverride(
            grob_name='Hairpin',
            once=True,
            property_path='stencil',
            value='#constante-hairpin',
            )

    @staticmethod
    def _circled_tip():
        return LilyPondGrobOverride(
            grob_name='Hairpin',
            once=True,
            property_path='circled-tip',
            value=True,
            )

    @staticmethod
    def _flared_hairpin():
        return LilyPondGrobOverride(
            grob_name='Hairpin',
            once=True,
            property_path='stencil',
            value='#abjad-flared-hairpin',
            )

    def _get_lilypond_format(self):
        strings = []
        if '--' in self.shape:
            override = self._constante_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if 'o' in self.shape:
            override = self._circled_tip()
            string = override.tweak_string()
            strings.append(string)
        if '|' in self.shape:
            override = self._flared_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if '<' in self.shape or '--' in self.shape:
            strings.append(self._crescendo_start)
        elif '>' in self.shape:
            strings.append(self._decrescendo_start)
        else:
            raise ValueError(self.shape)
        if self.left_broken is True:
            strings = self._tag_hide(strings)
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        """
        Dynamic trend contributes formatting to the 'spanners' slot
        (rather than the 'commands' slot). The reason for this is that
        the LilyPond \startTrillSpan [pitch] command must appear after
        \< and \> but before \set and other commmands.
        """
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanners.extend(tweaks)
        strings = self._get_lilypond_format()
        bundle.after.spanners.extend(strings)
        return bundle

    @staticmethod
    def _tag_hide(strings):
        import abjad
        abjad_tags = abjad.Tags()
        return LilyPondFormatManager.tag(
            strings,
            deactivate=False,
            tag=abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        r"""
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.DynamicTrend('<').context
            'Voice'

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), voice[0])
            >>> abjad.attach(abjad.DynamicTrend('<'), voice[0])
            >>> abjad.attach(abjad.Dynamic('f'), voice[-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \p
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }


            >>> for leaf in voice:
            ...     print(leaf, abjad.inspect(leaf).effective(abjad.DynamicTrend))
            c'4 DynamicTrend(shape='<')
            d'4 DynamicTrend(shape='<')
            e'4 DynamicTrend(shape='<')
            f'4 DynamicTrend(shape='<')

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def known_shapes(self) -> typing.Tuple[str, ...]:
        r"""

        Gets known shapes.

        ..  container:: example

            >>> for shape in abjad.DynamicTrend().known_shapes:
            ...     shape
            '<'
            'o<'
            '<|'
            'o<|'
            '>'
            '>o'
            '|>'
            '|>o'
            '--'

        """
        return self._known_shapes

    @property
    def left_broken(self) -> typing.Optional[bool]:
        r"""
        Is true when dynamic trend formats with left broken tag.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> trend = abjad.DynamicTrend('<', left_broken=True)
            >>> stop = abjad.Dynamic('f')
            >>> abjad.attach(trend, staff[0])
            >>> abjad.attach(stop, staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = #4.5
            }
            {
                c'4
                \< %! HIDE_TO_JOIN_BROKEN_SPANNERS
                d'4
                e'4
                f'4
                \f
            }

        """
        return self._left_broken

    @property
    def shape(self) -> str:
        r"""
        Gets shape.

        ..  container:: example

            Crescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('<'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \p
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

            Crescendo dal niente:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('o<'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    - \tweak circled-tip ##t
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

            Subito crescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('<|'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \p
                    - \tweak stencil #abjad-flared-hairpin
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

            Subito crescendo dal niente:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('niente', hide=True), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('o<|'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    - \tweak circled-tip ##t
                    - \tweak stencil #abjad-flared-hairpin
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

        ..  container:: example

            Decrescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('>'), staff[0])
            >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \f
                    \>
                    d'4
                    e'4
                    f'4
                    \p
                }

            Decrescendo al niente:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('>o'), staff[0])
            >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \f
                    - \tweak circled-tip ##t
                    \>
                    d'4
                    e'4
                    f'4
                    \!
                }

            Subito decrescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('|>'), staff[0])
            >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \f
                    - \tweak stencil #abjad-flared-hairpin
                    \>
                    d'4
                    e'4
                    f'4
                    \p
                }

            Subito decrescendo al niente:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('f'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('|>o'), staff[0])
            >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \f
                    - \tweak circled-tip ##t
                    - \tweak stencil #abjad-flared-hairpin
                    \>
                    d'4
                    e'4
                    f'4
                    \!
                }

        ..  container:: example

            Constante:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.DynamicTrend('--'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \p
                    - \tweak stencil #constante-hairpin
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

        """
        return self._shape

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.DynamicTrend('<').spanner_start
            True

        """
        return True

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> start = abjad.DynamicTrend('<')
            >>> abjad.tweak(start).color = 'blue'
            >>> abjad.attach(start, staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \p
                    - \tweak color #blue
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> start = abjad.DynamicTrend(tweaks=[('color', 'blue')])
            >>> abjad.tweak(start).color = 'blue'
            >>> abjad.attach(start, staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).dynamic_line_spanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = #4.5
                }
                {
                    c'4
                    \p
                    - \tweak color #blue
                    \<
                    d'4
                    e'4
                    f'4
                    \f
                }

        """
        return self._tweaks
