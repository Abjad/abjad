# -*- encoding: utf-8 -*-
from abjad import *


def make_nested_tuplet(
    tuplet_duration,
    outer_tuplet_proportions,
    inner_tuplet_subdivision_count,
    ):
    outer_tuplet = Tuplet.from_duration_and_ratio(
        tuplet_duration, outer_tuplet_proportions)
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    last_leaf = outer_tuplet.select_leaves()[-1]
    right_tie_chain = inspect(last_leaf).get_tie_chain()
    right_tie_chain.to_tuplet(inner_tuplet_proportions)
    return outer_tuplet
