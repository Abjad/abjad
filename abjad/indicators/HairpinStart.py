import typing
from abjad import enumerations
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class HairpinStart(AbjadValueObject):
    r"""
    Hairpin start.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.HairpinStart('<'), staff[0])
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
        '_lilypond_tweak_manager',
        '_shape',
        )

    _crescendo_start = r'\<'

    _decrescendo_start = r'\>'

    _format_slot = 'after'

    _known_shapes = (
        '<', 'o<', '<|', 'o<|',
        '>', '>o', '|>', '|>o',
        '--',
        )

    _time_orientation: enumerations.HorizontalAlignment = enumerations.Right

    ### INITIALIZER ###

    def __init__(
        self,
        shape='<',
        *,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        assert shape in self._known_shapes
        self._shape = shape
        self._lilypond_tweak_manager = None
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
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.commands.extend(tweaks)
        strings = self._get_lilypond_format()
        bundle.after.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def known_shapes(self) -> typing.Tuple[str, ...]:
        r"""

        Gets known shapes.

        ..  container:: example

            >>> for shape in abjad.HairpinStart().known_shapes:
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
    def shape(self) -> str:
        r"""
        Gets shape.

        ..  container:: example

            Crescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.HairpinStart('<'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('o<'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('<|'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('o<|'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('>'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('>o'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('|>'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('|>o'), staff[0])
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
            >>> abjad.attach(abjad.HairpinStart('--'), staff[0])
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
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> start = abjad.HairpinStart('<')
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
            >>> start = abjad.HairpinStart(tweaks=[('color', 'blue')])
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
        return self._lilypond_tweak_manager
