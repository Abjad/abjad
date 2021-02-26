import typing

from .. import enums, markups, typings
from ..bundle import LilyPondFormatBundle
from ..overrides import LilyPondOverride, TweakInterface
from ..storage import StorageFormatManager
from ..string import String


class StartTextSpan:
    r"""
    LilyPond ``\startTextSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup(r"\upright pont."),
        ...     right_text=abjad.Markup(r"\upright tasto"),
        ...     style="solid-line-with-arrow",
        ...     )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                c'4
                - \abjad-solid-line-with-arrow
                - \tweak bound-details.left.text \markup \concat { \upright
                    pont. \hspace #0.5 }
                - \tweak bound-details.right.text \markup {
                    \upright
                        tasto
                    }
                - \tweak staff-padding 2.5
                \startTextSpan
                d'4
                e'4
                f'4
                \stopTextSpan
            }

    ..  container:: example

        >>> abjad.StartTextSpan()
        StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_command",
        "_concat_hspace_left",
        "_concat_hspace_right",
        "_direction",
        "_left_broken_text",
        "_left_text",
        "_right_padding",
        "_right_text",
        "_style",
        "_tweaks",
    )

    _context = "Voice"

    _parameter = "TEXT_SPANNER"

    _persistent = True

    _styles = (
        "dashed-line-with-arrow",
        "dashed-line-with-hook",
        "dashed-line-with-up-hook",
        "invisible-line",
        "solid-line-with-arrow",
        "solid-line-with-hook",
        "solid-line-with-up-hook",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        command: str = r"\startTextSpan",
        concat_hspace_left: typings.Number = 0.5,
        concat_hspace_right: typings.Number = None,
        direction: enums.VerticalAlignment = None,
        left_broken_text: typing.Union[bool, str, markups.Markup] = None,
        left_text: typing.Union[str, markups.Markup] = None,
        right_padding: typings.Number = None,
        right_text: typing.Union[str, markups.Markup] = None,
        style: str = None,
        tweaks: TweakInterface = None,
    ) -> None:
        assert isinstance(command, str), repr(command)
        assert command.startswith("\\"), repr(command)
        self._command = command
        if concat_hspace_left is not None:
            assert isinstance(concat_hspace_left, (int, float))
        self._concat_hspace_left = concat_hspace_left
        if concat_hspace_right is not None:
            assert isinstance(concat_hspace_right, (int, float))
        self._concat_hspace_right = concat_hspace_right
        direction_ = String.to_tridirectional_lilypond_symbol(direction)
        self._direction = direction_
        if left_broken_text is not None:
            assert isinstance(left_broken_text, (bool, markups.Markup))
        self._left_broken_text = left_broken_text
        if left_text is not None:
            prototype = (str, markups.Markup)
            assert isinstance(left_text, prototype), repr(left_text)
        self._left_text = left_text
        if right_padding is not None:
            assert isinstance(right_padding, (int, float)), repr(right_padding)
        self._right_padding = right_padding
        if right_text is not None:
            prototype = (str, markups.Markup)
            assert isinstance(right_text, prototype), repr(right_text)
        self._right_text = right_text
        if style is not None:
            assert style in self._styles, repr(style)
        self._style = style
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

    def _get_left_broken_text_tweak(self):
        override = LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left-broken", "text"),
            value=self.left_broken_text,
        )
        string = override.tweak_string(self)
        return string

    def _get_left_text_directive(self):
        if isinstance(self.left_text, str):
            return self.left_text
        assert len(self.left_text.contents) == 1, repr(self.left_text)
        left_text_string = self.left_text.contents[0]
        hspace_string = fr"\hspace #{self.concat_hspace_left}"
        markup = markups.Markup(
            rf"\markup \concat {{ {left_text_string} {hspace_string} }}",
            literal=True,
        )
        override = LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "left", "text"),
            value=markup,
        )
        string = override.tweak_string()
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.style is not None:
            string = rf"- \abjad-{self.style}"
            bundle.after.spanner_starts.append(string)
        if self.left_text:
            string = self._get_left_text_directive()
            bundle.after.spanner_starts.append(string)
        if self.left_broken_text is not None:
            string = self._get_left_broken_text_tweak()
            bundle.after.spanner_starts.append(string)
        if self.right_text:
            string = self._get_right_text_tweak()
            bundle.after.spanner_starts.append(string)
        if self.right_padding:
            string = self._get_right_padding_tweak()
            bundle.after.spanner_starts.append(string)
        if self.tweaks:
            tweaks = self.tweaks._list_format_contributions()
            bundle.after.spanner_starts.extend(tweaks)
        string = self._add_direction(self.command)
        bundle.after.spanner_starts.append(string)
        return bundle

    def _get_right_padding_tweak(self):
        override = LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "right", "padding"),
            value=self.right_padding,
        )
        string = override.tweak_string()
        return string

    def _get_right_text_tweak(self):
        if isinstance(self.right_text, str):
            return self.right_text
        if self.concat_hspace_right is not None:
            number = self.concat_hspace_right
            assert len(self.right_text.contents) == 1
            right_text = self.right_text.contents[0]
            markup = markups.Markup(
                rf"\markup \concat {{ {right_text} \hspace #{number} }}",
                literal=True,
            )
        else:
            markup = self.right_text
        override = LilyPondOverride(
            grob_name="TextSpanner",
            property_path=("bound-details", "right", "text"),
            value=markup,
        )
        string = override.tweak_string()
        return string

    def _get_start_command(self):
        string = self._get_parameter_name()
        return rf"\start{string}"

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        r"""
        Gets comand.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")

            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="dashed-line-with-arrow",
            ...     )
            >>> abjad.tweak(start_text_span).color = "#blue"
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])

            >>> start_text_span = abjad.StartTextSpan(
            ...     command=r"\startTextSpanOne",
            ...     left_text=abjad.Markup(r"\upright A"),
            ...     right_text=abjad.Markup(r"\upright B"),
            ...     style="dashed-line-with-arrow",
            ...     )
            >>> abjad.tweak(start_text_span).color = "#red"
            >>> abjad.tweak(start_text_span).staff_padding = 6
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan(command=r"\stopTextSpanOne")
            >>> abjad.attach(stop_text_span, staff[-1])

            >>> markup = abjad.Markup("SPACER", direction=abjad.Up)
            >>> abjad.tweak(markup).transparent = True
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \tweak transparent ##t
                    ^ \markup { SPACER }
                    - \abjad-dashed-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak color #blue
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    - \abjad-dashed-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        A \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            B
                        }
                    - \tweak color #red
                    - \tweak staff-padding 6
                    \startTextSpanOne
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                    \stopTextSpanOne
                }

            (Spacer text included to prevent docs from clipping output.)

        """
        return self._command

    @property
    def concat_hspace_left(self) -> typings.Number:
        """
        Gets left hspace.

        Only included in LilyPond output when left text is set.
        """
        return self._concat_hspace_left

    @property
    def concat_hspace_right(self) -> typing.Optional[typings.Number]:
        """
        Gets right hspace.

        Only included in LilyPond output when right text is set.
        """
        return self._concat_hspace_right

    @property
    def context(self) -> str:
        """
        Returns (historically conventional) context ``'Voice'``.

        ..  container:: example

            >>> abjad.StartTextSpan().context
            'Voice'

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
    def enchained(self) -> bool:
        """
        Is true.
        """
        return True

    @property
    def left_broken_text(self) -> typing.Union[bool, markups.Markup, None]:
        """
        Gets left broken text.
        """
        return self._left_broken_text

    @property
    def left_text(self) -> typing.Union[str, markups.Markup, None]:
        r"""
        Gets left text.

        ..  container:: example

            String literals are allowed in place of markup:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> left_text = r'- \tweak bound-details.left.text \markup'
            >>> left_text += r' \concat { \upright pont. \hspace #0.5 }'
            >>> right_text = r'- \tweak bound-details.right.text \markup'
            >>> right_text += r' \upright tasto'
            >>> right_string = r'\markup \upright tasto'
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=left_text,
            ...     right_text=right_text,
            ...     style='solid-line-with-arrow',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup \upright tasto
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        """
        return self._left_text

    @property
    def parameter(self) -> str:
        """
        Returns ``'TEXT_SPANNER'``.

        ..  container:: example

            >>> abjad.StartTextSpan().parameter
            'TEXT_SPANNER'

        Class constant.
        """
        return self._parameter

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartTextSpan().persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def right_padding(self) -> typing.Optional[typings.Number]:
        """
        Gets right padding.
        """
        return self._right_padding

    @property
    def right_text(self) -> typing.Union[str, markups.Markup, None]:
        """
        Gets right text.
        """
        return self._right_text

    @property
    def spanner_start(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartTextSpan().spanner_start
            True

        """
        return True

    @property
    def style(self) -> typing.Optional[str]:
        r"""
        Gets style.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' fs'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="dashed-line-with-arrow",
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-dashed-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    fs'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     style="dashed-line-with-hook",
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-dashed-line-with-hook
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="invisible-line",
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-invisible-line
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     right_text=abjad.Markup(r"\upright tasto"),
            ...     style="solid-line-with-arrow",
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-solid-line-with-arrow
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup(r"\upright pont."),
            ...     style="solid-line-with-hook",
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    c'4
                    - \abjad-solid-line-with-hook
                    - \tweak bound-details.left.text \markup \concat { \upright
                        pont. \hspace #0.5 }
                    - \tweak staff-padding 2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        Constrained to ``'dashed-line-with-arrow'``,
        ``'dashed-line-with-hook'``, ``'invisible-line'``,
        ``'solid-line-with-arrow'``, ``'solid-line-with-hook'``, none.
        """
        return self._style

    @property
    def trend(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> abjad.StartTextSpan().trend
            True

        Class constant.
        """
        return True

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_text_span = abjad.StartTextSpan(
            ...     style='dashed-line-with-arrow',
            ...     )
            >>> abjad.tweak(start_text_span).color = "#blue"
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> string = abjad.storage(start_text_span)
            >>> print(string)
            abjad.StartTextSpan(
                command='\\startTextSpan',
                concat_hspace_left=0.5,
                style='dashed-line-with-arrow',
                tweaks=TweakInterface(('_literal', None), ('color', '#blue'), ('staff_padding', 2.5)),
                )

            >>> start_text_span_2 = copy.copy(start_text_span)
            >>> string = abjad.storage(start_text_span_2)
            >>> print(string)
            abjad.StartTextSpan(
                command='\\startTextSpan',
                concat_hspace_left=0.5,
                style='dashed-line-with-arrow',
                tweaks=TweakInterface(('_literal', None), ('color', '#blue'), ('staff_padding', 2.5)),
                )

        """
        return self._tweaks
