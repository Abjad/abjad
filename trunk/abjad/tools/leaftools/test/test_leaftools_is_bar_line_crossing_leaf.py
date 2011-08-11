from abjad import *


def test_leaftools_is_bar_line_crossing_leaf_01( ):

    t = Staff("c'8 d'8 e'8 f'8")
    t[2].written_duration *= 2
    contexttools.TimeSignatureMark(2, 8, partial = Duration(1, 8))(t)


    r'''
    \new Staff {
      \time 2/8
      \partial 8
      c'8
      d'8
      e'4
      f'8
    }
    '''

    assert not leaftools.is_bar_line_crossing_leaf(t[0])
    assert not leaftools.is_bar_line_crossing_leaf(t[1])
    assert leaftools.is_bar_line_crossing_leaf(t[2])
    assert not leaftools.is_bar_line_crossing_leaf(t[3])





