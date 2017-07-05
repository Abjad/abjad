# -*- coding: utf-8 -*-
import abjad


def make_nested_tuplet(
    tuplet_duration,
    outer_tuplet_proportions,
    inner_tuplet_subdivision_count,
    ):
    r'''Makes nested tuplet.
    '''

    outer_tuplet = abjad.Tuplet.from_duration_and_ratio(
        tuplet_duration,
        outer_tuplet_proportions,
        )
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    abjad.selector = abjad.select().by_leaf(flatten=True)
    last_leaf = abjad.selector(outer_tuplet)[-1]
    right_logical_tie = abjad.inspect_(last_leaf).get_logical_tie()
    right_logical_tie.to_tuplet(inner_tuplet_proportions)
    return outer_tuplet
