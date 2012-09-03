from abjad import *


def test_leaftools_rest_leaf_at_offset_01():

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.SlurSpanner(t[:])

    leaftools.rest_leaf_at_offset(
      t.leaves[1], Duration(1, 32))

    r'''
    \new Staff {
      c'8 (
      d'32
      r16.
      e'8
      f'8 )
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.lilypond_format == "\\new Staff {\n\tc'8 (\n\td'32\n\tr16.\n\te'8\n\tf'8 )\n}"
