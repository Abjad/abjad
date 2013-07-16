from abjad import *


def make_nested_tuplet(
    tuplet_duration,
    outer_tuplet_proportions,
    inner_tuplet_subdivision_count,
    ):
    outer_tuplet = tuplettools.make_tuplet_from_duration_and_ratio(
        tuplet_duration, outer_tuplet_proportions)
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    right_tie_chain = outer_tuplet.select_leaves()[-1].select_tie_chain()
    right_tie_chain.to_tuplet(inner_tuplet_proportions)
    return outer_tuplet
