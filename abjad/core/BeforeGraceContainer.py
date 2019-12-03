import typing

from abjad.system.Tag import Tag

from .Container import Container


class BeforeGraceContainer(Container):
    r"""
    Grace container.

    .. container:: example

        Grace container models LilyPond's different types of "left-positioned"
        grace music:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("cs'16 ds'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    cs'16
                    ds'16
                }
                d'4
                e'4
                f'4
            }

        LilyPond engraves grace music at a reduced size.

        LilyPond positions grace music immediately before a "main note" which
        follows.

    ..  container:: example

        Fill grace containers with notes, rests or chords:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Detach grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

        >>> abjad.detach(abjad.BeforeGraceContainer, voice[1])
        (BeforeGraceContainer("<cs' ds'>16 e'16"),)

        >>> abjad.detach(abjad.BeforeGraceContainer, voice[1])
        ()

        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Move grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.BeforeGraceContainer("<cs' ds'>16 e'")
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                d'4
                e'4
                f'4
            }

        >>> result = abjad.detach(abjad.BeforeGraceContainer, voice[1])
        >>> container = result[0]
        >>> abjad.attach(container, voice[3])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                d'4
                e'4
                \grace {
                    <cs' ds'>16
                    e'16
                }
                f'4
            }

    LilyPond provides four types of left-positioned grace music: acciaccaturas,
    appoggiaturas, grace notes and slashed grace notes; see
    ``abjad.BeforeGraceContainer.command`` to choose between these. LilyPond's
    left-positioned grace music contrasts with "right-positioned" after-grace
    music; see ``abjad.AfterGraceContainer``.

    Note that neither LilyPond nor Abjad attempts to model the ways that
    different categories of grace music have been performed historically.
    Typographic differences in slurring and slashing are provided. But
    distinctions between (for example) on-the-beat versus before-the-beat
    performance are left implicit.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    __slots__ = ("_command", "_main_leaf")

    _commands = (
        r"\acciaccatura",
        r"\appoggiatura",
        r"\grace",
        r"\slashedGrace",
    )

    ### INITIALIZER ###

    def __init__(
        self, components=None, *, command: str = r"\grace", tag: Tag = None
    ) -> None:
        if command not in self._commands:
            message = f"unknown command: {repr(command)}.\n"
            message += "  must be in {self._commands}"
            raise Exception(message)
        self._command = command
        self._main_leaf = None
        Container.__init__(self, components, tag=tag)

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> typing.Tuple:
        """
        Gets new grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        import abjad

        if not isinstance(leaf, abjad.Leaf):
            raise TypeError(f"must attach to leaf {leaf!r}.")
        leaf._before_grace_container = self
        self._main_leaf = leaf

    def _detach(self):
        if self._main_leaf is not None:
            main_leaf = self._main_leaf
            main_leaf._before_grace_container = None
            self._main_leaf = None
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        string = f"{self.command} {{"
        result.append([("grace_brackets", "open"), [string]])
        return tuple(result)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    ### PUBLIC PROPERTIES ###

    @property
    def command(self) -> str:
        r"""
        Gets command. Chooses between LilyPond's four types of left-positioned
        grace music.

        .. container:: example

            **(Vanilla) grace notes.** LilyPond formats single grace notes with
            neither a slash nor a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer("cs'16")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            LilyPond likewise formats runs of grace notes with neither a slash
            nor a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer("cs'16 ds'")
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \grace {
                        cs'16
                        ds'16
                    }
                    d'4
                    e'4
                    f'4
                }

        .. container:: example

            **Acciaccaturas.** LilyPond formats single acciaccaturas with
            both a slash and a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\acciaccatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \acciaccatura {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ..  container:: example exception

                But LilyPond fails to slash runs of acciaccaturas. This
                behavior is a longstanding LilyPond bug:

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16 ds'", command=r"\acciaccatura"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'4
                        \acciaccatura {
                            cs'16
                            ds'16
                        }
                        d'4
                        e'4
                        f'4
                    }

                ..  note:: LilyPond fails to slash runs of acciaccaturas.

        .. container:: example

            **Appoggiaturas.** LilyPond formats single appoggiaturas with
            only a slur; no slash is included:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\appoggiatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \appoggiatura {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            LilyPond likewise formats runs of appoggiaturas with only a slur:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16 ds'", command=r"\appoggiatura"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \appoggiatura {
                        cs'16
                        ds'16
                    }
                    d'4
                    e'4
                    f'4
                }

        .. container:: example

            **Slashed grace notes.** LilyPond formats single slashed grace
            notes with only a slash; no slur is included:

            >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
            >>> container = abjad.BeforeGraceContainer(
            ...     "cs'16", command=r"\slashedGrace"
            ... )
            >>> abjad.attach(container, voice[1])
            >>> abjad.show(voice) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(voice)
                \new Voice
                {
                    c'4
                    \slashedGrace {
                        cs'16
                    }
                    d'4
                    e'4
                    f'4
                }

            ..  container:: example exception

                But LilyPond fails to slash runs of "slashed" grace notes. This
                is a longstanding LilyPond bug:

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16 ds'", command=r"\slashedGrace"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'4
                        \slashedGrace {
                            cs'16
                            ds'16
                        }
                        d'4
                        e'4
                        f'4
                    }

                ..  note:: LilyPond fails to slash runs of "slashed" grace
                    notes.

        ..  container:: example

            LilyPond ``\acciaccatura``, ``\appoggiatura`` are syntactic sugar.

            .. container:: example

                **Grace notes with slur may be used instead of appoggiatura:**

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer("cs'16")
                >>> abjad.attach(container, voice[1])
                >>> leaves = abjad.select(voice).leaves()[1:3]
                >>> abjad.slur(leaves)
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'4
                        \grace {
                            cs'16
                            (
                        }
                        d'4
                        )
                        e'4
                        f'4
                    }

            .. container:: example

                **Slashed grace notes with slur may be used instead of
                acciaccatura:**

                >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
                >>> container = abjad.BeforeGraceContainer(
                ...     "cs'16", command=r"\slashedGrace"
                ... )
                >>> abjad.attach(container, voice[1])
                >>> leaves = abjad.select(voice).leaves()[1:3]
                >>> abjad.slur(leaves)
                >>> abjad.show(voice) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(voice)
                    \new Voice
                    {
                        c'4
                        \slashedGrace {
                            cs'16
                            (
                        }
                        d'4
                        )
                        e'4
                        f'4
                    }

        """
        return self._command
