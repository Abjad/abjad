import typing

from .. import enums
from ..bundle import LilyPondFormatBundle
from ..overrides import LilyPondOverride, TweakInterface
from ..storage import StorageFormatManager
from ..string import String


class StartHairpin:
    r"""
    Hairpin indicator.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.attach(abjad.Dynamic('p'), staff[0])
        >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
        >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
        >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            \with
            {
                \override DynamicLineSpanner.staff-padding = 4.5
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

    __slots__ = ("_direction", "_shape", "_tweaks")

    _context = "Voice"

    _crescendo_start = r"\<"

    _decrescendo_start = r"\>"

    _format_slot = "after"

    _known_shapes = ("<", "o<", "<|", "o<|", ">", ">o", "|>", "|>o", "--")

    _parameter = "DYNAMIC"

    _persistent = True

    # TODO: remove?
    _time_orientation = enums.Right

    ### INITIALIZER ###

    def __init__(
        self,
        shape="<",
        *,
        direction: enums.VerticalAlignment = None,
        tweaks: TweakInterface = None,
    ) -> None:
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        assert shape in self._known_shapes, repr(shape)
        self._shape = shape
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when all initialization values of Abjad value object equal
        the initialization values of ``argument``.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __hash__(self) -> int:
        """
        Hashes Abjad value object.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, "direction", False):
            string = f"{self.direction} {string}"
        return string

    @staticmethod
    def _circled_tip():
        return LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="circled-tip",
            value=True,
        )

    @staticmethod
    def _constante_hairpin():
        return LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="stencil",
            value="#constante-hairpin",
        )

    @staticmethod
    def _flared_hairpin():
        return LilyPondOverride(
            grob_name="Hairpin",
            once=True,
            property_path="stencil",
            value="#abjad-flared-hairpin",
        )

    def _get_lilypond_format(self):
        strings = []
        if "--" in self.shape:
            override = self._constante_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if "o" in self.shape:
            override = self._circled_tip()
            string = override.tweak_string()
            strings.append(string)
        if "|" in self.shape:
            override = self._flared_hairpin()
            string = override.tweak_string()
            strings.append(string)
        if "<" in self.shape or "--" in self.shape:
            string = self._crescendo_start
            string = self._add_direction(string)
            strings.append(string)
        elif ">" in self.shape:
            string = self._decrescendo_start
            string = self._add_direction(string)
            strings.append(string)
        else:
            raise ValueError(self.shape)
        return strings

    def _get_lilypond_format_bundle(self, component=None):
        r"""
        hairpin contributes formatting to the 'spanners' slot
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

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        r"""
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartHairpin('<').context
            'Voice'

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), voice[0])
            >>> abjad.attach(abjad.StartHairpin('<'), voice[0])
            >>> abjad.attach(abjad.Dynamic('f'), voice[-1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(voice)
                >>> print(string)
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
            ...     print(leaf, abjad.get.effective(leaf, abjad.StartHairpin))
            c'4 StartHairpin(shape='<')
            d'4 StartHairpin(shape='<')
            e'4 StartHairpin(shape='<')
            f'4 StartHairpin(shape='<')

        Class constant.

        Override with ``abjad.attach(..., context='...')``.
        """
        return self._context

    @property
    def direction(self) -> typing.Optional[String]:
        """
        Gets direction.
        """
        return self._direction

    @property
    def known_shapes(self) -> typing.Tuple[str, ...]:
        r"""

        Gets known shapes.

        ..  container:: example

            >>> for shape in abjad.StartHairpin().known_shapes:
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
    def parameter(self) -> str:
        """
        Returns ``'DYNAMIC'``.

        ..  container:: example

            >>> abjad.StartHairpin('<').parameter
            'DYNAMIC'

        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartHairpin('<').persistent
            True

        """
        return self._persistent

    @property
    def shape(self) -> str:
        r"""
        Gets shape.

        ..  container:: example

            Crescendo:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> abjad.attach(abjad.StartHairpin('<'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('o<'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('<|'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('o<|'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('>'), staff[0])
            >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('>o'), staff[0])
            >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('|>'), staff[0])
            >>> abjad.attach(abjad.Dynamic('p'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('|>o'), staff[0])
            >>> abjad.attach(abjad.Dynamic('niente', command=r'\!'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
            >>> abjad.attach(abjad.StartHairpin('--'), staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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

            >>> abjad.StartHairpin('<').spanner_start
            True

        """
        return True

    @property
    def trend(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartHairpin('<').trend
            True

        Class constant.
        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(abjad.Dynamic('p'), staff[0])
            >>> start_hairpin = abjad.StartHairpin('<')
            >>> abjad.tweak(start_hairpin).color = "#blue"
            >>> abjad.attach(start_hairpin, staff[0])
            >>> abjad.attach(abjad.Dynamic('f'), staff[-1])
            >>> abjad.override(staff).DynamicLineSpanner.staff_padding = 4.5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override DynamicLineSpanner.staff-padding = 4.5
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
