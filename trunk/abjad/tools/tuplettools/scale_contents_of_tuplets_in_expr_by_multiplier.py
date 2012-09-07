import fractions
from abjad.tools import durationtools
from abjad.tools import leaftools


def scale_contents_of_tuplets_in_expr_by_multiplier(tuplet, multiplier):
    '''Scale fixed-duration tuplet by multiplier.
        Preserve tuplet multiplier.
        Return tuplet.
    '''
    from abjad.tools import tuplettools

    # check input
    if not isinstance(tuplet, tuplettools.FixedDurationTuplet):
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
            if isinstance(component, leaftools.Leaf):
                leaftools.scale_preprolated_leaf_duration(component, multiplier)

    # otherwise doctor up tuplet multiplier, if necessary
    elif not durationtools.is_proper_tuplet_multiplier(tuplet.multiplier):
        tuplettools.fix_contents_of_tuplets_in_expr(tuplet)

    # return tuplet
    return tuplet
