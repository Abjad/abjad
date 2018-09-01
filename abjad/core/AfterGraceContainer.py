from .Container import Container


class AfterGraceContainer(Container):
    r"""
    After grace container.

    ..  container:: example

        After grace notes:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> string = '#(define afterGraceFraction (cons 15 16))'
        >>> literal = abjad.LilyPondLiteral(string)
        >>> abjad.attach(literal, voice[0])
        >>> notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> after_grace_container = abjad.AfterGraceContainer(notes)
        >>> abjad.attach(after_grace_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                #(define afterGraceFraction (cons 15 16))
                c'4
                \afterGrace
                d'4
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

        LilyPond positions after grace notes at a point 3/4 of the way
        after the note they follow. The resulting spacing is usually too
        loose.

        Customize aftterGraceFraction as shown above.

    After grace notes are played at the very end of the note they follow.

    Use after grace notes when you need to end a piece of music with grace
    notes.

    After grace notes do not subclass grace notes; but acciacatura containers
    and appoggiatura containers do subclass grace notes.

    Fill grace containers with notes, rests or chords.

    Attach after grace containers to notes, rests or chords.

    ..  container:: example

        REGRESSION. After grace containers format correctly with main note
        articulations and markup:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> string = '#(define afterGraceFraction (cons 15 16))'
        >>> literal = abjad.LilyPondLiteral(string)
        >>> abjad.attach(literal, voice[0])
        >>> after_grace_container = abjad.AfterGraceContainer("c'16 d'16")
        >>> abjad.attach(after_grace_container, voice[1])
        >>> leaves = abjad.select(voice).leaves(grace_notes=None)
        >>> markup = abjad.Markup('Allegro', direction=abjad.Up)
        >>> abjad.attach(markup, leaves[1])
        >>> abjad.attach(abjad.Staccato(), leaves[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                #(define afterGraceFraction (cons 15 16))
                c'4
                \afterGrace
                d'4
                ^ \markup { Allegro }
                \staccato
                {
                    c'16
                    d'16
                }
                e'4
                f'4
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = (
        '_main_leaf',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        tag: str = None,
        ) -> None:
        self._main_leaf = None
        Container.__init__(
            self,
            components,
            tag=tag,
            )

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        """
        Gets new after grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        import abjad
        if not isinstance(leaf, abjad.Leaf):
            raise TypeError(f'must attach to leaf (not {leaf!r}).')
        leaf._after_grace_container = self
        self._main_leaf = leaf

    def _detach(self):
        if self._main_leaf is not None:
            main_leaf = self._main_leaf
            main_leaf._after_grace_container = None
            self._main_leaf = None
        return self

    def _format_open_brackets_slot(self, bundle):
        result = []
        result.append([('grace_brackets', 'open'), ['{']])
        return tuple(result)
