# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import select


def make_nested_tuplet(
    tuplet_duration,
    outer_tuplet_proportions,
    inner_tuplet_subdivision_count,
    ):
    r'''Makes nested tuplet.
    '''

    outer_tuplet = scoretools.Tuplet.from_duration_and_ratio(
        tuplet_duration, outer_tuplet_proportions)
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    selector = select().by_leaf(flatten=True)
    last_leaf = selector(outer_tuplet)[-1]
    right_logical_tie = inspect_(last_leaf).get_logical_tie()
    right_logical_tie.to_tuplet(inner_tuplet_proportions)
    return outer_tuplet