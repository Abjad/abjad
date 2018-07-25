import typing
from abjad import enums
from abjad import markups
from abjad import typings
from abjad.lilypondnames.LilyPondGrobOverride import LilyPondGrobOverride
from abjad.lilypondnames.LilyPondTweakManager import LilyPondTweakManager
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle
from abjad.utilities.String import String
from .LilyPondLiteral import LilyPondLiteral


class StartTextSpan(AbjadValueObject):
    r"""
    LilyPond ``\startTextSpan`` command.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> start_text_span = abjad.StartTextSpan(
        ...     left_text=abjad.Markup('pont.').upright(),
        ...     right_text=abjad.Markup('tasto').upright(),
        ...     style='solid_line_with_arrow',
        ...     )
        >>> abjad.tweak(start_text_span).staff_padding = 2.5
        >>> abjad.attach(start_text_span, staff[0])
        >>> stop_text_span = abjad.StopTextSpan()
        >>> abjad.attach(stop_text_span, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \abjad_solid_line_with_arrow
                - \tweak bound-details.left.text \markup {
                    \concat
                        {
                            \upright
                                pont.
                            \hspace
                                #0.5
                        }
                    }
                - \tweak bound-details.right.text \markup {
                    \upright
                        tasto
                    }
                - \tweak staff-padding #2.5
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
        '_command',
        '_concat_hspace_left',
        '_concat_hspace_right',
        '_direction',
        '_left_broken_text',
        '_left_text',
        '_right_padding',
        '_right_text',
        '_style',
        '_tweaks',
        )

    _publish_storage_format = True

    _styles = (
        'dashed_line_with_arrow',
        'dashed_line_with_hook',
        'invisible_line',
        'solid_line_with_arrow',
        'solid_line_with_hook',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        command: str = r'\startTextSpan',
        concat_hspace_left: typings.Number = 0.5,
        concat_hspace_right: typings.Number = None,
        direction: enums.VerticalAlignment = None,
        left_broken_text: typing.Union[
            bool, LilyPondLiteral, markups.Markup] = None,
        left_text: typing.Union[LilyPondLiteral, markups.Markup] = None,
        right_padding: typings.Number = None,
        right_text: typing.Union[LilyPondLiteral, markups.Markup] = None,
        style: str = None,
        tweaks: typing.Union[
            typing.List[typing.Tuple], LilyPondTweakManager] = None,
        ) -> None:
        assert isinstance(command, str), repr(command)
        assert command.startswith('\\'), repr(command)
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
            prototype = (LilyPondLiteral, markups.Markup)
            assert isinstance(left_text, prototype), repr(left_text)
        self._left_text = left_text
        if right_padding is not None:
            assert isinstance(right_padding, (int, float)), repr(right_padding)
        self._right_padding = right_padding
        if right_text is not None:
            prototype = (LilyPondLiteral, markups.Markup)
            assert isinstance(right_text, prototype), repr(right_text)
        self._right_text = right_text
        if style is not None:
            assert style in self._styles, repr(style)
        self._style = style
        self._tweaks = None
        LilyPondTweakManager.set_tweaks(self, tweaks)

    ### PRIVATE METHODS ###

    def _add_direction(self, string):
        if getattr(self, 'direction', False):
            string = f'{self.direction} {string}'
        return string

    def _get_left_broken_text_tweak(self):
        override = LilyPondGrobOverride(
            grob_name='TextSpanner',
            property_path=(
                'bound-details',
                'left-broken',
                'text',
                ),
            value=self.left_broken_text,
            )
        string = override.tweak_string(self)
        return string

    def _get_left_text_tweak(self):
        import abjad
        if isinstance(self.left_text, LilyPondLiteral):
            markup = self.left_text
        else:
            concat_hspace_left_markup = markups.Markup.hspace(
                self.concat_hspace_left)
            markup_list = [self.left_text, concat_hspace_left_markup]
            markup = markups.Markup.concat(markup_list)
        override = LilyPondGrobOverride(
            grob_name='TextSpanner',
            property_path=(
                'bound-details',
                'left',
                'text',
                ),
            value=markup,
            )
        string = override.tweak_string()
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.style is not None:
            string = rf'- \abjad_{self.style}'
            bundle.after.spanner_starts.append(string)
        if self.left_text:
            string = self._get_left_text_tweak()
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
        override = LilyPondGrobOverride(
            grob_name='TextSpanner',
            property_path=(
                'bound-details',
                'right',
                'padding',
                ),
            value=self.right_padding,
            )
        string = override.tweak_string()
        return string

    def _get_right_text_tweak(self):
        if self.concat_hspace_right is not None:
            number = self.concat_hspace_right
            concat_hspace_right_markup = markups.Markup.hspace(number)
            markup_list = [concat_hspace_right_markup, self.right_text]
            markup = markups.Markup.concat(markup_list)
        else:
            markup = self.right_text
        override = LilyPondGrobOverride(
            grob_name='TextSpanner',
            property_path=(
                'bound-details',
                'right',
                'text',
                ),
            value=markup,
            )
        string = override.tweak_string()
        return string

    def _get_start_command(self):
        string = self._get_parameter_name()
        return rf'\start{string}'

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        r"""
        Gets comand.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")

            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).color = 'blue'
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])

            >>> start_text_span = abjad.StartTextSpan(
            ...     command=r'\startTextSpanOne',
            ...     left_text=abjad.Markup('A').upright(),
            ...     right_text=abjad.Markup('B').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).color = 'red'
            >>> abjad.tweak(start_text_span).staff_padding = 6
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan(command=r'\stopTextSpanOne')
            >>> abjad.attach(stop_text_span, staff[-1])

            >>> markup = abjad.Markup('SPACER', direction=abjad.Up)
            >>> abjad.tweak(markup).transparent = True
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak transparent ##t
                    ^ \markup { SPACER }
                    - \abjad_dashed_line_with_arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak color #blue
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    - \abjad_dashed_line_with_arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    A
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            B
                        }
                    - \tweak color #red
                    - \tweak staff-padding #6
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
    def left_text(self) -> typing.Union[LilyPondLiteral, markups.Markup, None]:
        r"""
        Gets left text.

        ..  container:: example

            LilyPond literals are allowed in place of markup:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> left_string = r'\markup \concat { \upright pont. \hspace #0.5 }'
            >>> right_string = r'\markup \upright tasto'
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.LilyPondLiteral(left_string),
            ...     right_text=abjad.LilyPondLiteral(right_string),
            ...     style='solid_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_solid_line_with_arrow
                    - \tweak bound-details.left.text \markup \concat { \upright pont. \hspace #0.5 }
                    - \tweak bound-details.right.text \markup \upright tasto
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

            Use with custom markup functions.

        """
        return self._left_text

    @property
    def right_padding(self) -> typing.Optional[typings.Number]:
        """
        Gets right padding.
        """
        return self._right_padding

    @property
    def right_text(self) -> typing.Union[
        LilyPondLiteral, markups.Markup, None]:
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
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_dashed_line_with_arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    fs'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     style='dashed_line_with_hook',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_dashed_line_with_hook
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='invisible_line',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_invisible_line
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='solid_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_solid_line_with_arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     style='solid_line_with_hook',
            ...     )
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_solid_line_with_hook
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        Constrained to ``'dashed_line_with_arrow'``,
        ``'dashed_line_with_hook'``, ``'invisible_line'``,
        ``'solid_line_with_arrow'``, ``'solid_line_with_hook'``, none.
        """
        return self._style

    @property
    def tweaks(self) -> typing.Optional[LilyPondTweakManager]:
        r"""
        Gets tweaks

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> start_text_span = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).color = 'blue'
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.attach(start_text_span, staff[0])
            >>> stop_text_span = abjad.StopTextSpan()
            >>> abjad.attach(stop_text_span, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \abjad_dashed_line_with_arrow
                    - \tweak bound-details.left.text \markup {
                        \concat
                            {
                                \upright
                                    pont.
                                \hspace
                                    #0.5
                            }
                        }
                    - \tweak bound-details.right.text \markup {
                        \upright
                            tasto
                        }
                    - \tweak color #blue
                    - \tweak staff-padding #2.5
                    \startTextSpan
                    d'4
                    e'4
                    f'4
                    \stopTextSpan
                }

        ..  container:: example

            REGRESSION. Tweaks survive copy:

            >>> import copy
            >>> start_text_span = abjad.StartTextSpan(
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(start_text_span).color = 'blue'
            >>> abjad.tweak(start_text_span).staff_padding = 2.5
            >>> abjad.f(start_text_span)
            abjad.StartTextSpan(
                command='\\startTextSpan',
                concat_hspace_left=0.5,
                style='dashed_line_with_arrow',
                tweaks=LilyPondTweakManager(('color', 'blue'), ('staff_padding', 2.5)),
                )

            >>> start_text_span_2 = copy.copy(start_text_span)
            >>> abjad.f(start_text_span_2)
            abjad.StartTextSpan(
                command='\\startTextSpan',
                concat_hspace_left=0.5,
                style='dashed_line_with_arrow',
                tweaks=LilyPondTweakManager(('color', 'blue'), ('staff_padding', 2.5)),
                )

        """
        return self._tweaks
