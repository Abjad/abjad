from abjad import *


def test_leaftools_make_leaves_from_note_value_signal_01():

    leaves = leaftools.make_leaves_from_note_value_signal([3, -3, 5, -5], 8)
    staff = Staff(leaves)

    r'''
    \new Staff {
      c'4.
      r4.
      c'2 ~
      c'8
      r2
      r8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'4.\n\tr4.\n\tc'2 ~\n\tc'8\n\tr2\n\tr8\n}"
