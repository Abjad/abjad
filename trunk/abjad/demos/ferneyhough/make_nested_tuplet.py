from abjad import *


def make_nested_tuplet(tuplet_duration, outer_tuplet_proportions, inner_tuplet_subdivision_count):
    outer_tuplet = tuplettools.make_tuplet_from_duration_and_ratio(
        tuplet_duration, outer_tuplet_proportions)
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    right_tie_chain = tietools.get_tie_chain(outer_tuplet.leaves[-2])
    tietools.tie_chain_to_tuplet_with_ratio(right_tie_chain, inner_tuplet_proportions)
    return outer_tuplet

