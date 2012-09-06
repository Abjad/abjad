import fractions
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def make_notes(pitches, durations, big_endian=True):
    '''Make notes according to `pitches` and `durations`.

    Cycle through `pitches` when the length of `pitches` is less than the 
    length of `durations`::

        >>> notetools.make_notes([0], [(1, 16), (1, 8), (1, 8)])
        [Note("c'16"), Note("c'8"), Note("c'8")]

    Cycle through `durations` when the length of `durations` is less than the 
    length of `pitches`::

        >>> notetools.make_notes([0, 2, 4, 5, 7], [(1, 16), (1, 8), (1, 8)])
        [Note("c'16"), Note("d'8"), Note("e'8"), Note("f'16"), Note("g'8")]

    Create ad hoc tuplets for nonassignable durations::

        >>> notetools.make_notes([0], [(1, 16), (1, 12), (1, 8)])
        [Note("c'16"), Tuplet(2/3, [c'8]), Note("c'8")]

    Set ``big_endian=True`` to express tied values in decreasing duration::

        >>> notetools.make_notes([0], [(13, 16)], big_endian=True)
        [Note("c'2."), Note("c'16")]

    Set ``big_endian=False`` to express tied values in increasing duration::

        >>> notetools.make_notes([0], [(13, 16)], big_endian=False)
        [Note("c'16"), Note("c'2.")]

    Set `pitches` to a single pitch or a sequence of pitches.

    Set `durations` to a single duration or a list of durations.

    Return list of newly constructed notes.

    .. versionchanged:: 2.0
        renamed ``construct.notes()`` to
        ``notetools.make_notes()``.
    '''
    from abjad.tools import notetools
    from abjad.tools import tuplettools

    if pitchtools.is_named_chromatic_pitch_token(pitches):
        pitches = [pitches]

    if isinstance(durations, (numbers.Number, tuple)):
        durations = [durations]

    # this block is a hack to allow the function to accept a Duration
    # as the duration input parameter; better will be to change
    # the rest of the implementation to allow for Durations directly.
    # [VA] We don't want to change to Durations internally because
    # Durations reduce fractions to their minimum expression. e.g.
    # (3, 3) --> Duration(1, 1), and we sometimes generate duration
    # tokens that are not reduced, so we want to preserve the denominator 3.
    # [TB] When do we want (3, 3) instead of (1, 1)?
    # Durations should always reduce;
    # So tokens can represent tuplet multipliers or something
    # else that shouldn't reduce?
    durations = [durationtools.duration_token_to_duration_pair(dur) for dur in durations]

    # set lists of pitches and durations to the same length
    size = max(len(durations), len(pitches))
    durations = sequencetools.repeat_sequence_to_length(durations, size)
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)

    durations = durationtools.group_duration_tokens_by_implied_prolation(durations)

    def _make_unprolated_notes(pitches, durations, big_endian=big_endian):
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(notetools.make_tied_note(pitch, duration, big_endian=big_endian))
        return result

    result = []
    for duration in durations:
        # get factors in denominator of duration group duration other than 1, 2.
        factors = set(mathtools.factors(duration[0][1]))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0:len(duration)]
        pitches = pitches[len(duration):]
        if len(factors) == 0:
            result.extend(_make_unprolated_notes(ps, duration, big_endian=big_endian))
        else:
            # compute prolation
            denominator = duration[0][1]
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / fractions.Fraction(*multiplier)
            duration = [ratio * durationtools.Duration(*d) for d in duration]
            ns = _make_unprolated_notes(ps, duration, big_endian=big_endian)
            t = tuplettools.Tuplet(multiplier, ns)
            result.append(t)

    # return result
    return result
