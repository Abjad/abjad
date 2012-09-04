from __future__ import division
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


# TODO: Change leaftools.make_leaves() signature to allow ('c', 4) named pairs
#       This will allow the creation of enharmonic equivalents.
#       Examples: leaftools.make_leaves([('c', 4), ('cs', 4)], [(1, 4)])

# TODO: Extend leaftools.make_leaves() to accept Abjad Pitch instances. Ex:
#       Example: leaftools.make_leaves([NamedChromaticPitch('cs', 4)], [(1, 4)])

def make_leaves(pitches, durations, big_endian=True, tie_rests=False):
    r'''.. versionadded:: 1.1

    Construct a list of notes, rests or chords.

    Set `pitches` is a single pitch, or a list of pitches, or a tuple
    of pitches.

    Integer pitches create notes. ::

        >>> leaftools.make_leaves([2, 4, 19], [(1, 4)])
        [Note("d'4"), Note("e'4"), Note("g''4")]

    Tuple pitches create chords. ::

        >>> leaftools.make_leaves([(0, 1, 2), (3, 4, 5), (6, 7, 8)], [(1, 4)])
        [Chord("<c' cs' d'>4"), Chord("<ef' e' f'>4"), Chord("<fs' g' af'>4")]

    Set `pitches` to a list of none to create rests. ::

        >>> leaftools.make_leaves([None, None, None, None], [(1, 8)])
        [Rest('r8'), Rest('r8'), Rest('r8'), Rest('r8')]

    You can mix and match pitch values. ::

        >>> leaftools.make_leaves([12, (1, 2, 3), None, 12], [(1, 4)])
        [Note("c''4"), Chord("<cs' d' ef'>4"), Rest('r4'), Note("c''4")]

    If the length of `pitches` is less than the length of `durations`,
    the function reads `durations` cyclically. ::

        >>> leaftools.make_leaves([13], [(1, 8), (1, 8), (1, 4), (1, 4)])
        [Note("cs''8"), Note("cs''8"), Note("cs''4"), Note("cs''4")]

    Set `durations` to a single duration, a list of duration, or
    a tuple of durations.

    If the length of `durations` is less than the length of `pitches`,
    the function reads `pitches` cyclically. ::

        >>> leaftools.make_leaves([13, 14, 15, 16], [(1, 8)])
        [Note("cs''8"), Note("d''8"), Note("ef''8"), Note("e''8")]

    Duration values not of the form ``m / 2 ** n`` return
    leaves nested inside a fixed-multiplier tuplet. ::

        >>> leaftools.make_leaves([14], [(1, 12), (1, 12), (1, 12)])
        [Tuplet(2/3, [d''8, d''8, d''8])]

    Set ``big_endian=False`` to return tied leaf durations from least to greatest::

        >>> staff = Staff(leaftools.make_leaves([15], [(13, 16)], big_endian=False))
        >>> f(staff)
        \new Staff {
            ef''16 ~
            ef''2.
        }

    Set `tie_rests` to true to return tied rests for durations like
    ``5/16`` and ``9/16``. ::

        >>> staff = Staff(leaftools.make_leaves([None], [(5, 16)], tie_rests=True))
        >>> f(staff)
        \new Staff {
            r4 ~
            r16
        }

    Return list of leaves.

    .. versionchanged:: 2.0
        renamed ``construct.leaves()`` to
        ``leaftools.make_leaves()``.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools
    from abjad.tools import resttools
    from abjad.tools import tuplettools

    def _make_leaf_on_pitch(pitch, duration, big_endian=big_endian):
        if isinstance(pitch, (int, long, float, pitchtools.NamedChromaticPitch)):
            leaves = notetools.make_tied_note(pitch, duration, big_endian=big_endian)
        elif isinstance(pitch, (tuple, list)):
            leaves = chordtools.make_tied_chord(pitch, duration, big_endian=big_endian)
        elif pitch is None:
            leaves = resttools.make_tied_rest(duration, big_endian=big_endian, tied=tie_rests)
        else:
            raise ValueError('Unknown pitch {!r}.'.format(pitch))
        return leaves

    if pitchtools.is_named_chromatic_pitch_token(pitches):
        pitches = [pitches]

    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    # change durations to duration tokens
    durations = [durationtools.duration_token_to_duration_pair(duration) for duration in durations]

    # set lists of pitches and durations to the same length
    size = max(len(durations), len(pitches))
    durations = sequencetools.repeat_sequence_to_length(durations, size)
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)

    duration_groups = durationtools.group_duration_tokens_by_implied_prolation(durations)

    result = []
    for duration_group in duration_groups:
        # get factors in denominator of duration group other than 1, 2.
        factors = set(mathtools.factors(duration_group[0][1]))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0:len(duration_group)]
        pitches = pitches[len(duration_group):]
        if len(factors) == 0:
            for pitch, duration in zip(ps, duration_group):
                leaves = _make_leaf_on_pitch(pitch, duration, big_endian=big_endian)
                result.extend(leaves)
        else:
            # compute prolation
            denominator = duration_group[0][1]
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / durationtools.Duration(*multiplier)
            duration_group = [ratio * durationtools.Duration(*duration) for duration in duration_group]
            # make leaves
            leaves = []
            for pitch, duration in zip(ps, duration_group):
                leaves.extend(_make_leaf_on_pitch(pitch, duration, big_endian=big_endian))
            tuplet = tuplettools.Tuplet(multiplier, leaves)
            result.append(tuplet)

    return result
