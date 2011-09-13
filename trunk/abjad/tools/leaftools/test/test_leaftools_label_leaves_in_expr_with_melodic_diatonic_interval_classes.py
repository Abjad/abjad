from abjad import *


def test_leaftools_label_leaves_in_expr_with_melodic_diatonic_interval_classes_01():

    staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    leaftools.label_leaves_in_expr_with_melodic_diatonic_interval_classes(staff)

    r"""
    \new Staff {
      c'8 ^ \markup { +aug8 }
      cs'''8 ^ \markup { -M2 }
      b'8 ^ \markup { -aug2 }
      af8 ^ \markup { -m7 }
      bf,8 ^ \markup { aug1 }
      b,8 ^ \markup { +m7 }
      a'8 ^ \markup { +m2 }
      bf'8 ^ \markup { -dim4 }
      fs'8 ^ \markup { aug1 }
      f'8
    }
    """

    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +aug8 }\n\tcs'''8 ^ \\markup { -M2 }\n\tb'8 ^ \\markup { -aug2 }\n\taf8 ^ \\markup { -m7 }\n\tbf,8 ^ \\markup { aug1 }\n\tb,8 ^ \\markup { +m7 }\n\ta'8 ^ \\markup { +m2 }\n\tbf'8 ^ \\markup { -dim4 }\n\tfs'8 ^ \\markup { aug1 }\n\tf'8\n}"
