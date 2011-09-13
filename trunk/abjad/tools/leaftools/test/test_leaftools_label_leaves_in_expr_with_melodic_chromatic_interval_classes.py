from abjad import *


def test_leaftools_label_leaves_in_expr_with_melodic_chromatic_interval_classes_01():


    staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    leaftools.label_leaves_in_expr_with_melodic_chromatic_interval_classes(staff)

    r"""
    \new Staff {
      c'8 ^ \markup { +1 }
      cs'''8 ^ \markup { -2 }
      b'8 ^ \markup { -2 }
      af8 ^ \markup { -10 }
      bf,8 ^ \markup { +1 }
      b,8 ^ \markup { +10 }
      a'8 ^ \markup { +1 }
      bf'8 ^ \markup { -4 }
      fs'8 ^ \markup { -1 }
      f'8
    }
    """

    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +1 }\n\tcs'''8 ^ \\markup { -2 }\n\tb'8 ^ \\markup { -2 }\n\taf8 ^ \\markup { -10 }\n\tbf,8 ^ \\markup { +1 }\n\tb,8 ^ \\markup { +10 }\n\ta'8 ^ \\markup { +1 }\n\tbf'8 ^ \\markup { -4 }\n\tfs'8 ^ \\markup { -1 }\n\tf'8\n}"
