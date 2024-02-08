import dataclasses
import typing

from . import _getlib
from . import bind as _bind
from . import get as _get
from . import indicators as _indicators
from . import instruments as _instruments
from . import iterate as _iterate
from . import pcollections as _pcollections
from . import pitch as _pitch
from . import score as _score


def iterate_out_of_range(argument) -> typing.Iterator[_score.Leaf]:
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
        instrument = _getlib._get_effective(leaf, _instruments.Instrument)
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
    if isinstance(argument, int | float):
        pitch = _pitch.NamedPitch(argument)
        return pitch in pitch_range
    if isinstance(argument, _pitch.Pitch):
        return argument in pitch_range
    if hasattr(argument, "written_pitch"):
        sounding_pitch = _getlib._get_sounding_pitch(argument)
        return sounding_pitch in pitch_range
    if hasattr(argument, "written_pitches"):
        sounding_pitches = _getlib._get_sounding_pitches(argument)
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
        instrument = _getlib._get_effective(leaf, _instruments.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        interval *= -1
        if hasattr(leaf, "note_head"):
            pitch = leaf.written_pitch
            pitch = interval.transpose(pitch)
            leaf.written_pitch = pitch
        elif hasattr(leaf, "note_heads"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            for note_head, pitch in zip(leaf.note_heads, pitches, strict=True):
                note_head.written_pitch = pitch
        wrapper = _get.indicator(leaf, _indicators.StartTrillSpan, unwrap=False)
        if wrapper is not None:
            start_trill_span = wrapper.unbundle_indicator()
            new_pitch = interval.transpose(start_trill_span.pitch)
            new_start_trill_span = dataclasses.replace(
                start_trill_span, pitch=new_pitch
            )
            wrapper_tag = wrapper.tag
            _bind.detach(wrapper, leaf)
            if wrapper.bundled():
                new_bundle = dataclasses.replace(
                    wrapper.get_item(), indicator=new_start_trill_span
                )
                _bind.attach(new_bundle, leaf, tag=wrapper_tag)
            else:
                _bind.attach(new_start_trill_span, leaf, tag=wrapper_tag)


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
        instrument = _getlib._get_effective(leaf, _instruments.Instrument)
        if not instrument:
            continue
        sounding_pitch = instrument.middle_c_sounding_pitch
        interval = _pitch.NamedPitch("C4") - sounding_pitch
        if hasattr(leaf, "note_head"):
            written_pitch = leaf.written_pitch
            written_pitch = interval.transpose(written_pitch)
            leaf.written_pitch = written_pitch
        elif hasattr(leaf, "note_heads"):
            pitches = [interval.transpose(pitch) for pitch in leaf.written_pitches]
            for note_head, pitch in zip(leaf.note_heads, pitches, strict=True):
                note_head.written_pitch = pitch
        wrapper = _get.indicator(leaf, _indicators.StartTrillSpan, unwrap=False)
        if wrapper is not None:
            start_trill_span = wrapper.unbundle_indicator()
            new_pitch = interval.transpose(start_trill_span.pitch)
            new_start_trill_span = dataclasses.replace(
                start_trill_span, pitch=new_pitch
            )
            _bind.detach(wrapper, leaf)
            if wrapper.bundled():
                new_bundle = dataclasses.replace(
                    wrapper.get_item, indicator=new_start_trill_span
                )
                _bind.attach(new_bundle, leaf)
            else:
                _bind.attach(new_start_trill_span, leaf)
