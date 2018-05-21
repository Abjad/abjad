from .GraceContainer import GraceContainer


class AppoggiaturaContainer(GraceContainer):
    r"""
    Appoggiatura container.

    Appoggiaturas are played on the beat.

    LilyPond positions appoggiaturas immediately before main notes.

    LilyPond formats appoggiaturas with a slur but without a slashed
    stem.

    ..  container:: example

        Appoggiatura notes:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> appoggiatura_container = abjad.AppoggiaturaContainer(notes)
        >>> abjad.attach(appoggiatura_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \appoggiatura {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill appoggiatura containers with notes, rests or chords.

    Attach appoggiatura containers to notes, rests or chords.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        result = []
        result.append([('grace_brackets', 'open'), [r'\appoggiatura {']])
        return tuple(result)
