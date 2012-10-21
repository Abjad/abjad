import math
from abjad.tools import containertools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools


# TODO: change name to make_tuplet_from_ratio_and_nonreduced_fraction
def make_tuplet_from_proportions_and_pair(proportions, (n, d)):
    '''Divide nonreduced fraction `(n, d)` according to `proportions`.

    Return container when no prolation is necessary::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1], (7, 16))
        {c'4..}

    Return fixed-duration tuplet when prolation is necessary::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1, 2], (7, 16))
        FixedDurationTuplet(7/16, [c'8, c'4])

    ::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4])

    ::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16])

    ::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8])

    ::

        >>> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2, 4], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8, c'4])

    .. note:: function interprets `d` as tuplet denominator.

    Return tuplet or container.

    .. versionchanged:: 2.0
        renamed ``divide.pair()`` to
        ``tuplettools.make_tuplet_from_proportions_and_pair()``.
    '''
    from abjad.tools import tuplettools

    duration = (n, d)

    if len(proportions) == 0:
        raise ValueError('proportions must contain at least one term.')

    if len(proportions) == 1:
        if 0 < proportions[0]:
            try:
                return containertools.Container([notetools.Note(0, duration)])
            except AssignabilityError:
                return containertools.Container(notetools.make_notes(0, duration))
        elif proportions[0] < 0:
            try:
                return containertools.Container([resttools.Rest(duration)])
            except AssignabilityError:
                return containertools.Container(resttools.make_rests(duration))
        else:
            raise ValueError('no divide zero values.')

    if 1 < len(proportions):
        exponent = int(math.log(mathtools.weight(proportions), 2) - math.log(n, 2))
        denominator = int(d * 2 ** exponent)
        music = []
        for x in proportions:
            if not x:
                raise ValueError('no divide zero values.')
            if 0 < x:
                try:
                    music.append(notetools.Note(0, (x, denominator)))
                except AssignabilityError:
                    music.extend(notetools.make_notes(0, (x, denominator)))
            else:
                music.append(resttools.Rest((-x, denominator)))
        return tuplettools.FixedDurationTuplet(duration, music)
