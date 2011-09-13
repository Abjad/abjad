from abjad import *


def test_leaftools_divide_leaves_in_expr_meiotically_01():
    '''Meiose each leaf in two.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    leaftools.divide_leaves_in_expr_meiotically(t)

    r'''
    \new Voice {
      c'16 [
      c'16
      d'16
      d'16
      e'16
      e'16 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'16 [\n\tc'16\n\td'16\n\td'16\n\te'16\n\te'16 ]\n}"


def test_leaftools_divide_leaves_in_expr_meiotically_02():
    '''Meiose one leaf in four.'''

    t = Voice("c'8 d'8 e'8")
    spannertools.BeamSpanner(t[:])
    leaftools.divide_leaves_in_expr_meiotically(t[0], 4)

    r'''
    \new Voice {
      c'32 [
      c'32
      c'32
      c'32
      d'8
      e'8 ]
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Voice {\n\tc'32 [\n\tc'32\n\tc'32\n\tc'32\n\td'8\n\te'8 ]\n}"
