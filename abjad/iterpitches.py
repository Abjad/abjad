import typing

from . import _inspect
from . import get as _get
from . import indicators as _indicators
from . import instruments as _instruments
from . import iterate as _iterate
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import score as _score


def iterate_out_of_range(argument) -> typing.Generator:
    r"""
    Iterates out-of-range notes and chords in ``argument``.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 r8 <d fs>8 r8")
        >>> violin = abjad.Violin()
        >>> abjad.attach(violin, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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
    for leaf in _iterate.leaves(argument, pitched=True):
        instrument = _inspect._get_effective(leaf, _instruments.Instrument)
        if instrument is None:
            raise ValueError("no instrument found.")
        if not sounding_pitches_are_in_range(leaf, instrument.pitch_range):
            yield leaf


def respell_with_flats(argument) -> None:
    r"""
    Respells pitches in ``argument`` with flats.

    ..  container:: example

        >>> staff = abjad.Staff("cs'8 ds' es' fs' gs' as' bs'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                cs'8
                ds'8
                es'8
                fs'8
                gs'8
                as'8
                bs'4
            }

        >>> abjad.iterpitches.respell_with_flats(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                df'8
                ef'8
                f'8
                gf'8
                af'8
                bf'8
                c''4
            }

    """
    for leaf in _iterate.leaves(argument):
        if isinstance(leaf, _score.Note):
            assert leaf.written_pitch is not None
            leaf.written_pitch = leaf.written_pitch.respell(accidental="flats")
        elif isinstance(leaf, _score.Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch.respell(accidental="flats")
                note_head.written_pitch = pitch


def respell_with_sharps(argument) -> None:
    r"""
    Respells pitches in ``argument`` with sharps.

    ..  container:: example

        >>> staff = abjad.Staff("cf'8 df' ef' ff' gf' af' bf'4")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                cf'8
                df'8
                ef'8
                ff'8
                gf'8
                af'8
                bf'4
            }

        >>> abjad.iterpitches.respell_with_sharps(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                b8
                cs'8
                ds'8
                e'8
                fs'8
                gs'8
                as'4
            }

    """
    for leaf in _iterate.leaves(argument):
        if isinstance(leaf, _score.Note):
            assert leaf.written_pitch is not None
            leaf.written_pitch = leaf.written_pitch.respell(accidental="sharps")
        elif isinstance(leaf, _score.Chord):
            for note_head in leaf.note_heads:
                pitch = note_head.written_pitch.respell(accidental="sharps")
                note_head.written_pitch = pitch


def sounding_pitches_are_in_range(argument, pitch_range) -> bool:
    """
    Returns true when all pitches in ``argument`` sound within ``pitch_range``.
    """
    assert isinstance(pitch_range, _pcollections.PitchRange), repr(pitch_range)
    if isinstance(argument, (int, float)):
        pitch = _pitch.NamedPitch(argument)
        return pitch in pitch_range
    if isinstance(argument, _pitch.Pitch):
        return argument in pitch_range
    if hasattr(argument, "written_pitch"):
        sounding_pitch = _inspect._get_sounding_pitch(argument)
        return sounding_pitch in pitch_range
    if hasattr(argument, "written_pitches"):
        sounding_pitches = _inspect._get_sounding_pitches(argument)
        return all(_ in pitch_range for _ in sounding_pitches)
    pitches = list(_iterate.pitches(argument))
    if pitches:
        return all(_ in pitch_range for _ in pitches)
    else:
        try:
            return all(_ in pitch_range for _ in argument)
        except TypeError:
            return False
    return False


def transpose_from_sounding_pitch(argument) -> None:
    r"""
    Transpose notes and chords in ``argument`` from sounding pitch to written pitch.

    ..  container:: example

        >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <d' fs' a'>4
                e'4
                r4
                fs'4
            }

    """
    for leaf in _iterate.leaves(argument, pitched=True):
        instrument = _inspect._get_effective(leaf, _instruments.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        interval *= -1
        if hasattr(leaf, "written_pitch"):
            pitch = leaf.written_pitch
            pitch = interval.transpose(pitch)
            leaf.written_pitch = pitch
        elif hasattr(leaf, "written_pitches"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            leaf.written_pitches = pitches
        start_trill_span = _get.indicator(leaf, _indicators.StartTrillSpan)
        if start_trill_span is not None:
            pitch = start_trill_span.pitch
            pitch = interval.transpose(pitch)
            start_trill_span.pitch = pitch


def transpose_from_written_pitch(argument) -> None:
    r"""
    Transposes notes and chords in ``argument`` from sounding pitch to written pitch.

    ..  container:: example

        >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
        >>> clarinet = abjad.ClarinetInBFlat()
        >>> abjad.attach(clarinet, staff[0])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
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

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <bf d' f'>4
                c'4
                r4
                d'4
            }

    """
    for leaf in _iterate.leaves(argument, pitched=True):
        instrument = _inspect._get_effective(leaf, _instruments.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        if hasattr(leaf, "written_pitch"):
            written_pitch = leaf.written_pitch
            written_pitch = interval.transpose(written_pitch)
            leaf.written_pitch = written_pitch
        elif hasattr(leaf, "written_pitches"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            leaf.written_pitches = pitches
        start_trill_span = _get.indicator(leaf, _indicators.StartTrillSpan)
        if start_trill_span is not None:
            pitch = start_trill_span.pitch
            pitch = interval.transpose(pitch)
            start_trill_span.pitch = pitch
