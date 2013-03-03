import fractions
from abjad.tools import durationtools
from abjad.tools import mathtools


def make_accelerating_notes_with_lilypond_multipliers(pitches, total, start, stop, exp='cosine', written='8'):
    r'''Make accelerating notes with LilyPond multipliers:

    ::

        >>> pitches = ['C#4', 'D4']
        >>> total = Duration(4, 4)
        >>> start = Duration(1, 4)
        >>> stop = Duration(1, 16)
        >>> args = [pitches, total, start, stop]

    ::

        >>> notes = notetools.make_accelerating_notes_with_lilypond_multipliers(*args)

    ::

        >>> staff = Staff(notes)
        >>> beam = beamtools.BeamSpanner(staff[:])
        >>> slur = spannertools.SlurSpanner(staff[:])

    ::

        >>> f(staff)
        \new Staff {
            cs'8 * 245/128 [ (
            d'8 * 109/64
            cs'8 * 161/128
            d'8 * 115/128
            cs'8 * 87/128
            d'8 * 9/16
            cs'8 * 1/2
            d'8 * 61/128 ] )
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Set note pitches cyclically from `pitches`.

    Return as many interpolation values as necessary to fill the `total` duration requested.

    Interpolate durations from `start` to `stop`.

    Set note durations to `written` duration times computed interpolated multipliers.

    Return list of notes.
    '''
    from abjad.tools import notetools

    # initialize input arguments as durations
    total = durationtools.Duration(total)
    start = durationtools.Duration(start)
    stop = durationtools.Duration(stop)
    written = durationtools.Duration(written)

    # change mathtools input arguments to vanilla rationals
    args = [fractions.Fraction(x) for x in (total, start, stop)]
    args.append(exp)

    # calculate lilypond multipliers
    multipliers = mathtools.interpolate_divide(*args)

    # change floats to rationals
    multipliers = [durationtools.Multiplier(int(round(x * 2**10)), 2**10) for x in multipliers]

    # make notes
    result = []
    for i, multiplier in enumerate(multipliers):
        note = notetools.Note(pitches[i % len(pitches)], written)
        note.duration_multiplier = durationtools.Multiplier(multiplier / written)
        result.append(note)

    # return result
    return result
