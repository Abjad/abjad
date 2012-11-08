import fractions
import numbers
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def make_notes(pitches, durations, decrease_durations_monotonically=True):
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

    Set ``decrease_durations_monotonically=True`` to express tied values in decreasing duration::

        >>> notetools.make_notes([0], [(13, 16)], decrease_durations_monotonically=True)
        [Note("c'2."), Note("c'16")]

    Set ``decrease_durations_monotonically=False`` to express tied values in increasing duration::

        >>> notetools.make_notes([0], [(13, 16)], decrease_durations_monotonically=False)
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
    duration_pairs = [durationtools.Duration(duration) for duration in durations]

    # set lists of pitches and duration pairs to the same length
    size = max(len(duration_pairs), len(pitches))
    duration_pairs = sequencetools.repeat_sequence_to_length(duration_pairs, size)
    pitches = sequencetools.repeat_sequence_to_length(pitches, size)

    durations = durationtools.group_nonreduced_fractions_by_implied_prolation(duration_pairs)

    def _make_unprolated_notes(pitches, durations, decrease_durations_monotonically=decrease_durations_monotonically):
        assert len(pitches) == len(durations)
        result = []
        for pitch, duration in zip(pitches, durations):
            result.extend(notetools.make_tied_note(pitch, duration, decrease_durations_monotonically=decrease_durations_monotonically))
        return result

    result = []
    for duration in durations:
        # get factors in denominator of duration group duration other than 1, 2.
        factors = set(mathtools.factors(duration[0].denominator))
        factors.discard(1)
        factors.discard(2)
        ps = pitches[0:len(duration)]
        pitches = pitches[len(duration):]
        if len(factors) == 0:
            result.extend(_make_unprolated_notes(ps, duration, decrease_durations_monotonically=decrease_durations_monotonically))
        else:
            # compute prolation
            denominator = duration[0].denominator
            numerator = mathtools.greatest_power_of_two_less_equal(denominator)
            multiplier = (numerator, denominator)
            ratio = 1 / fractions.Fraction(*multiplier)
            duration = [ratio * durationtools.Duration(d) for d in duration]
            ns = _make_unprolated_notes(ps, duration, decrease_durations_monotonically=decrease_durations_monotonically)
            t = tuplettools.Tuplet(multiplier, ns)
            result.append(t)

    # return result
    return result
