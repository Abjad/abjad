from abjad.tools.tuplettools.Tuplet import Tuplet
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import leaftools
from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
from abjad.tools import durationtools
import fractions
import math


def fix_contents_of_tuplets_in_expr(tuplet):
    '''Scale `tuplet` contents by power of two
    if tuplet multiplier less than 1/2 or greater than 2.
    Return tuplet. ::

        abjad> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'4 d'4 e'4")
        abjad> tuplet
        FixedDurationTuplet(1/4, [c'4, d'4, e'4])
        abjad> tuplettools.fix_contents_of_tuplets_in_expr(tuplet)
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])

    .. versionchanged:: 2.0
        renamed ``tuplettools.contents_fix()`` to
        ``tuplettools.fix_contents_of_tuplets_in_expr()``.
    '''

    # check input
    if not isinstance(tuplet, FixedDurationTuplet):
        raise TypeError('must be fixed-duration tuplet.')

    # find tuplet multiplier
    integer_exponent = int(math.log(tuplet.multiplier, 2))
    leaf_multiplier = fractions.Fraction(2) ** integer_exponent

    # scale leaves in tuplet by power of two
    for component in tuplet[:]:
        if isinstance(component, _Leaf):
            old_written_duration = component.written_duration
            new_written_duration = leaf_multiplier * old_written_duration
            leaftools.set_preprolated_leaf_duration(
                component, new_written_duration)

    return tuplet
