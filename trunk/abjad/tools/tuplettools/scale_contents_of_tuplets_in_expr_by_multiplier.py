import fractions
from abjad.tools import durationtools
from abjad.tools import leaftools


def scale_contents_of_tuplets_in_expr_by_multiplier(tuplet, multiplier):
    r'''Scale contents of fixed-duration `tuplet` by `multiplier`::

        >>> tuplet = tuplettools.FixedDurationTuplet((3, 8), "c'8 d'8 e'8 f'8 g'8")

    ::

        >>> f(tuplet)
        \fraction \times 3/5 {
            c'8
            d'8
            e'8
            f'8
            g'8
        }

    ::

        >>> tuplettools.scale_contents_of_tuplets_in_expr_by_multiplier(tuplet, Fraction(2))
        FixedDurationTuplet(3/4, [c'4, d'4, e'4, f'4, g'4])

    ::

        >>> f(tuplet)
        \fraction \times 3/5 {
            c'4
            d'4
            e'4
            f'4
            g'4
        }

    Preserve `tuplet` multiplier.

    Return tuplet.
    '''
    from abjad.tools import tuplettools

    # check input
    if not isinstance(tuplet, tuplettools.FixedDurationTuplet):
        raise TypeError('must be fixed-duration tuplet.')

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
