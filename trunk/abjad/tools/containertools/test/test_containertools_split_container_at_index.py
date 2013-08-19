# -*- encoding: utf-8 -*-
from abjad import *
import py


# containertools.split_container_at_index() works here;
# componenttools.split() doesn't work here.
# hook in old function.
def test_containertools_split_container_at_index_01():
    r'''Split in-score measure without power-of-two time signature denominator.
    Fractured spanners but do not tie over split locus.
    Measure contents necessitate denominator change.
    '''
    py.test.skip('TODO: make this work.')

    staff = Staff([Measure((3, 12), "c'8. d'8.")])
    spannertools.BeamSpanner(staff[0])
    spannertools.SlurSpanner(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/12
                \scaleDurations #'(2 . 3) {
                    c'8. [ (
                    d'8. ] )
                }
            }
        }
        '''
        )

    halves = componenttools.split(
        staff[:1], 
        #1, 
        [Duration(3, 24)],
        fracture_spanners=True,
        )

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 3/24
                \scaleDurations #'(2 . 3) {
                    c'8. [ ] (
                }
            }
            {
                \scaleDurations #'(2 . 3) {
                    d'8. [ ] )
                }
            }
        }
        '''
        )

    assert select(staff).is_well_formed()
    assert len(halves) == 2
