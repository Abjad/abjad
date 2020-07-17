import typing

from . import _inspect
from .instruments import Instrument
from .iterate import Iteration
from .pitch.PitchRange import PitchRange
from .pitch.pitches import NamedPitch, Pitch
from .score import Chord, Note
from .selectx import Selection


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

        >>> for leaf in abjad.iterpitches.iterate_out_of_range(staff):
        ...     leaf
        ...
        Chord('<d fs>8')

    """
    leaves = Selection(components).leaves(pitched=True)
    assert isinstance(leaves, Selection), repr(leaves)
    for leaf in leaves:
        instrument = _inspect._get_effective(leaf, Instrument)
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

        >>> abjad.iterpitches.respell_with_flats(staff)
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

        >>> abjad.iterpitches.respell_with_sharps(staff)
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
        sounding_pitch = _inspect._get_sounding_pitch(argument)
        return pitch_range._contains_pitch(sounding_pitch)
    if hasattr(argument, "written_pitches"):
        sounding_pitches = _inspect._get_sounding_pitches(argument)
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


def transpose_from_sounding_pitch(argument):
    r"""
    Transpose notes and chords in ``argument`` from sounding pitch to written pitch.

    ..  container:: example

        >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c' e' g'>4
                d'4
                r4
                e'4
            }

        >>> abjad.iterpitches.transpose_from_sounding_pitch(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <d' fs' a'>4
                e'4
                r4
                fs'4
            }

    Returns none.
    """
    for leaf in Iteration(argument).leaves(pitched=True):
        instrument = _inspect._get_effective(leaf, Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = NamedPitch("C4") - sounding_pitch
        interval *= -1
        if hasattr(leaf, "written_pitch"):
            pitch = leaf.written_pitch
            pitch = interval.transpose(pitch)
            leaf.written_pitch = pitch
        elif hasattr(leaf, "written_pitches"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            leaf.written_pitches = pitches


def transpose_from_written_pitch(argument):
    r"""
    Transposes notes and chords in ``argument`` from sounding pitch to written pitch.

    ..  container:: example

        >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <c' e' g'>4
                d'4
                r4
                e'4
            }

        >>> abjad.iterpitches.transpose_from_written_pitch(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                <bf d' f'>4
                c'4
                r4
                d'4
            }

    Returns none.
    """
    for leaf in Iteration(argument).leaves(pitched=True):
        instrument = _inspect._get_effective(leaf, Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = NamedPitch("C4") - sounding_pitch
        if hasattr(leaf, "written_pitch"):
            written_pitch = leaf.written_pitch
            written_pitch = interval.transpose(written_pitch)
            leaf.written_pitch = written_pitch
        elif hasattr(leaf, "written_pitches"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            leaf.written_pitches = pitches
