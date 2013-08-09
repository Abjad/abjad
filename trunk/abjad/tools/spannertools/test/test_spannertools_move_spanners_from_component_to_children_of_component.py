# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_move_spanners_from_component_to_children_of_component_01():
    r'''From parent to children.
    '''

    voice = Voice(Container(notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
    beam = spannertools.BeamSpanner(voice[:])

    r'''
    \new Voice {
        {
            c'8 [
            d'8
        }
        {
            e'8
            f'8 ]
        }
    }
    '''

    spannertools.move_spanners_from_component_to_children_of_component(voice[0])

    assert more(voice[0]).get_spanners() == set([])
    assert more(voice[0][0]).get_spanners() == set([beam])
