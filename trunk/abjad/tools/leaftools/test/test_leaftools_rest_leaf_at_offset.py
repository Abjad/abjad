# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_rest_leaf_at_offset_01():

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.SlurSpanner(t[:])

    leaftools.rest_leaf_at_offset(
      t.select_leaves()[1], Duration(1, 32))

    r'''
    \new Staff {
      c'8 (
      d'32
      r16.
      e'8
      f'8 )
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff {
            c'8 (
            d'32
            r16.
            e'8
            f'8 )
        }
        '''
        )
