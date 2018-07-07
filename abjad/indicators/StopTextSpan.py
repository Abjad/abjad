import typing
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.system.LilyPondFormatBundle import LilyPondFormatBundle


class StopTextSpan(AbjadValueObject):
    r"""
    LilyPond ``\stopTextSpan`` command.

    ..  container:: example

        >>> abjad.StopTextSpan()
        StopTextSpan(command='\\stopTextSpan')

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        '_leak',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        command: str = r'\stopTextSpan',
        *,
        leak: bool = None,
        ) -> None:
        assert isinstance(command, str), repr(command)
        assert command.startswith('\\'), repr(command)
        self._command = command
        if leak is not None:
            leak = bool(leak)
        self._leak = leak

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        string = self.command
        if self.leak:
            string = f'<> {string}'
            bundle.after.leaks.append(string)
        else:
            bundle.after.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        """
        Gets command.
        """
        return self._command

    @property
    def enchained(self) -> bool:
        """
        Is true.
        """
        return True

    @property
    def leak(self) -> typing.Optional[bool]:
        r"""
        Is true when stop text span leaks LilyPond ``<>`` empty chord.

        ..  container:: example

            Without leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(command).staff_padding = 2.5
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTextSpan()
            >>> abjad.attach(command, staff[-2])
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
                    \stopTextSpan
                    r4
                }

            With leak:

            >>> staff = abjad.Staff("c'4 d' e' r")
            >>> command = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(command).staff_padding = 2.5
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(command, staff[-2])
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
                    <> \stopTextSpan
                    r4
                }

        ..  container:: example

            REGRESSION. Leaked contributions appear last in postevent format
            slot:

            >>> staff = abjad.Staff("c'8 d' e' f' r2")
            >>> abjad.attach(abjad.Beam(), staff[:4])
            >>> abjad.attach(abjad.Slur(), staff[:4])
            >>> command = abjad.StartTextSpan(
            ...     left_text=abjad.Markup('pont.').upright(),
            ...     right_text=abjad.Markup('tasto').upright(),
            ...     style='dashed_line_with_arrow',
            ...     )
            >>> abjad.tweak(command).staff_padding = 2.5
            >>> abjad.attach(command, staff[0])
            >>> command = abjad.StopTextSpan(leak=True)
            >>> abjad.attach(command, staff[3])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
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
                    [
                    (
                    d'8
                    e'8
                    f'8
                    ]
                    )
                    <> \stopTextSpan
                    r2
                }

            The leaked text spanner above does not inadvertantly leak the beam
            or slur.

        """
        return self._leak

    @property
    def spanner_stop(self) -> bool:
        """
        Is true.
        """
        return True
