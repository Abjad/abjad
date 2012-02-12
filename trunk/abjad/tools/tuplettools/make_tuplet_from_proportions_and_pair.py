from abjad.tools.containertools.Container import Container
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import notetools
from abjad.tools import resttools
from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
import math


def make_tuplet_from_proportions_and_pair(l, (n, d)):
    '''Divide `(n, d)` according to `l`.

    Where no prolation is necessary, return container. ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1], (7, 16))
        {c'4..}

    Where prolation is necessary, return fixed-duration tuplet. ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2], (7, 16))
        FixedDurationTuplet(7/16, [c'8, c'4])

    ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4])

    ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16])

    ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8])

    ::

        abjad> tuplettools.make_tuplet_from_proportions_and_pair([1, 2, 4, 1, 2, 4], (7, 16))
        FixedDurationTuplet(7/16, [c'16, c'8, c'4, c'16, c'8, c'4])

    .. note:: function accepts a pair rather than a rational.

    .. note:: function interprets `d` as tuplet denominator.

    .. versionchanged:: 2.0
        renamed ``divide.pair()`` to
        ``tuplettools.make_tuplet_from_proportions_and_pair()``.
    '''


    duration = (n, d)

    if len(l) == 0:
        raise ValueError('must divide list l of poisitive length.')

    if len(l) == 1:
        if 0 < l[0]:
            try:
                return Container([notetools.Note(0, duration)])
            except AssignabilityError:
                return Container(notetools.make_notes(0, duration))
        elif l[0] < 0:
            try:
                return Container([resttools.Rest(duration)])
            except AssignabilityError:
                return Container(resttools.make_rests(duration))
        else:
            raise ValueError('no divide zero values.')

    if 1 < len(l):
        exponent = int(math.log(mathtools.weight(l), 2) - math.log(n, 2))
        denominator = int(d * 2 ** exponent)
        music = []
        for x in l:
            if not x:
                raise ValueError('no divide zero values.')
            if 0 < x:
                try:
                    music.append(notetools.Note(0, (x, denominator)))
                except AssignabilityError:
                    music.extend(notetools.make_notes(0, (x, denominator)))
            else:
                music.append(resttools.Rest((-x, denominator)))
        return FixedDurationTuplet(duration, music)
