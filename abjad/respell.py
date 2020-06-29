from .core.Chord import Chord
from .core.Iteration import iterate
from .core.Note import Note


def respell_with_flats(selection):
    r"""
    Respells `selection` with flats.

    ..  container:: example

        Respells notes in staff:

        >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                cs'8
                d'8
                ef'8
                e'8
                f'8
            }

        >>> abjad.respell_with_flats(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                df'8
                d'8
                ef'8
                e'8
                f'8
            }

    Returns none.
    """
    for leaf in iterate(selection).leaves():
        if isinstance(leaf, Note):
            leaf.written_pitch = leaf.written_pitch._respell_with_flats()
        elif isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch._respell_with_flats()
                note_head.written_pitch = pitch


def respell_with_sharps(selection):
    r"""
    Respells `selection` with sharps.

    ..  container:: example

        Respells notes in staff:

        >>> staff = abjad.Staff("c'8 cs'8 d'8 ef'8 e'8 f'8")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                cs'8
                d'8
                ef'8
                e'8
                f'8
            }

        >>> abjad.respell_with_sharps(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                cs'8
                d'8
                ds'8
                e'8
                f'8
            }

    Returns none.
    """
    for leaf in iterate(selection).leaves():
        if isinstance(leaf, Note):
            leaf.written_pitch = leaf.written_pitch._respell_with_sharps()
        elif isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch._respell_with_sharps()
                note_head.written_pitch = pitch
