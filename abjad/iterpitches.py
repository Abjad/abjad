import typing

from .core.Chord import Chord
from .core.Iteration import Iteration
from .core.Note import Note
from .core.Selection import Selection
from .core.inspectx import Inspection
from .instruments import Instrument
from .pitch.PitchRange import PitchRange
from .pitch.pitches import NamedPitch, Pitch


def iterate_out_of_range(components) -> typing.Generator:
    r"""
    Iterates out-of-range notes and chords.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                r8
                <d fs>8
                r8
            }

        >>> for leaf in abjad.iterate_out_of_range(staff):
        ...     leaf
        ...
        Chord('<d fs>8')

    """
    leaves = Selection(components).leaves(pitched=True)
    assert isinstance(leaves, Selection), repr(leaves)
    for leaf in leaves:
        instrument = Inspection(leaf).effective(Instrument)
        if instrument is None:
            raise ValueError("no instrument found.")
        if not sounding_pitches_are_in_range(leaf, instrument.pitch_range):
            yield leaf


def respell_with_flats(selection):
    r"""
    Respells ``selection`` with flats.

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
    for leaf in Iteration(selection).leaves():
        if isinstance(leaf, Note):
            leaf.written_pitch = leaf.written_pitch._respell_with_flats()
        elif isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch._respell_with_flats()
                note_head.written_pitch = pitch


def respell_with_sharps(selection):
    r"""
    Respells ``selection`` with sharps.

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
    for leaf in Iteration(selection).leaves():
        if isinstance(leaf, Note):
            leaf.written_pitch = leaf.written_pitch._respell_with_sharps()
        elif isinstance(leaf, Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch._respell_with_sharps()
                note_head.written_pitch = pitch


def sounding_pitches_are_in_range(argument, pitch_range) -> bool:
    assert isinstance(pitch_range, PitchRange), repr(pitch_range)
    if isinstance(argument, (int, float)):
        pitch = NamedPitch(argument)
        return pitch_range._contains_pitch(pitch)
    if isinstance(argument, Pitch):
        return pitch_range._contains_pitch(argument)
    if hasattr(argument, "written_pitch"):
        sounding_pitch = Inspection(argument).sounding_pitch()
        return pitch_range._contains_pitch(sounding_pitch)
    if hasattr(argument, "written_pitches"):
        sounding_pitches = Inspection(argument).sounding_pitches()
        return all(pitch_range._contains_pitch(_) for _ in sounding_pitches)
    pitches = list(Iteration(argument).pitches())
    if pitches:
        return all(pitch_range._contains_pitch(_) for _ in pitches)
    else:
        try:
            return all(pitch_range._contains_pitch(_) for _ in argument)
        except TypeError:
            return False
    return False
