from .GraceContainer import GraceContainer


class AcciaccaturaContainer(GraceContainer):
    r"""
    Acciaccatura container.

    Acciaccaturas are played before the beat.

    LilyPond positions acciaccaturas immediately before main notes.

    LilyPond formats one-note acciaccaturas with a slashed stem and a slur.

    ..  note:: LilyPond fails to format multinote acciaccaturas
        with a slashed stem. This means that multinote
        acciaccaturas look exactly like appoggiaturas.

    ..  container:: example

        Acciaccatura notes:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> notes = [abjad.Note("c'16"), abjad.Note("d'16")]
        >>> acciaccatura_container = abjad.AcciaccaturaContainer(notes)
        >>> abjad.attach(acciaccatura_container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                \acciaccatura {
                    c'16
                    d'16
                }
                d'4
                e'4
                f'4
            }

    Fill acciaccatura containers with notes, rests or chords.

    Attach acciaccatura containers to notes, rests or chords.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Containers'

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _format_open_brackets_slot(self, bundle):
        result = []
        result.append([('grace_brackets', 'open'), [r'\acciaccatura {']])
        return tuple(result)
