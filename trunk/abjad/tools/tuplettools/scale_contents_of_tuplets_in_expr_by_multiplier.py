from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools import durationtools
from abjad.tools import leaftools
from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet
from abjad.tools.tuplettools.fix_contents_of_tuplets_in_expr import fix_contents_of_tuplets_in_expr
from abjad.tools.tuplettools.is_proper_tuplet_multiplier import is_proper_tuplet_multiplier
import fractions


def scale_contents_of_tuplets_in_expr_by_multiplier(tuplet, multiplier):
    '''Scale fixed-duration tuplet by multiplier.
        Preserve tuplet multiplier.
        Return tuplet.
    '''

    # check input
    if not isinstance(tuplet, FixedDurationTuplet):
        raise TypeError('must be tuplet.')
    assert isinstance(multiplier, fractions.Fraction)

    # find new target duration
    old_target_duration = tuplet.target_duration
    new_target_duration = multiplier * old_target_duration

    # change tuplet target duration
    tuplet.target_duration = new_target_duration

    # if multiplier is note head assignable, scale contents graphically
    if durationtools.is_assignable_rational(multiplier):
        for component in tuplet[:]:
            if isinstance(component, _Leaf):
                leaftools.scale_preprolated_leaf_duration(component, multiplier)

    # otherwise doctor up tuplet multiplier, if necessary
    elif not is_proper_tuplet_multiplier(tuplet.multiplier):
            fix_contents_of_tuplets_in_expr(tuplet)

    # return tuplet
    return tuplet
