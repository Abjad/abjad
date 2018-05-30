from .Container import Container


class GraceContainer(Container):
    r"""
    Grace container.

    LilyPond positions grace notes immediately before main notes.

    LilyPond formats grace notes with neither a slashed nor a slur.

    .. container:: example

        Grace notes:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> grace_notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> grace_container = abjad.GraceContainer(grace_notes)
        >>> abjad.attach(grace_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill grace containers with notes, rests or chords.

    Attach grace containers to notes, rests or chords.

    ..  container:: example

        Detaches grace container:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> note = abjad.Note("cs'16")
        >>> grace_container = abjad.GraceContainer([note])
        >>> abjad.attach(grace_container, voice[1])
        >>> note = abjad.Note("ds'16")
        >>> after_grace_container = abjad.AfterGraceContainer([note])
        >>> abjad.attach(after_grace_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \grace {
                    cs'16
                }
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

        >>> abjad.detach(abjad.GraceContainer, voice[1])
        (GraceContainer("cs'16"),)
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \afterGrace
                d'4
                {
                    ds'16
                }
                e'4
                f'4
            }

    ..  container:: example

        Grace containers can be moved:

        >>> staff = abjad.Staff("c'4 d'")
        >>> container = abjad.GraceContainer("fs'32")
        >>> abjad.attach(container, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \grace {
                    fs'32
                }
                c'4
                d'4
            }

        >>> result = abjad.detach(abjad.GraceContainer, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
            }

        >>> abjad.attach(result[0], staff[1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                \grace {
                    fs'32
                }
                d'4
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_carrier',
        )

    ### INITIALIZER ###

    def __init__(self, components=None):
        self._carrier = None
        Container.__init__(self, components)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        """
        Gets new grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        import abjad
        if not isinstance(leaf, abjad.Leaf):
            message = 'must attach to leaf: {!r}.'
            message = message.format(leaf)
            raise TypeError(message)
        leaf._grace_container = self
        self._carrier = leaf

    def _detach(self):
        if self._carrier is not None:
            carrier = self._carrier
            carrier._grace_container = None
            self._carrier = None
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        result.append([('grace_brackets', 'open'), [r'\grace {']])
        return tuple(result)

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()
