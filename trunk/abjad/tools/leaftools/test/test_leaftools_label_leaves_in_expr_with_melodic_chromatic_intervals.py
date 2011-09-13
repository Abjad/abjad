from abjad import *


def test_leaftools_label_leaves_in_expr_with_melodic_chromatic_intervals_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaftools.label_leaves_in_expr_with_melodic_chromatic_intervals(staff)

    r'''
    \new Staff {
      c'8 ^ \markup { +2 }
      d'8 ^ \markup { +2 }
      e'8 ^ \markup { +1 }
      f'8 ^ \markup { +2 }
      g'8 ^ \markup { +2 }
      a'8 ^ \markup { +2 }
      b'8 ^ \markup { +1 }
      c''8
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +2 }\n\td'8 ^ \\markup { +2 }\n\te'8 ^ \\markup { +1 }\n\tf'8 ^ \\markup { +2 }\n\tg'8 ^ \\markup { +2 }\n\ta'8 ^ \\markup { +2 }\n\tb'8 ^ \\markup { +1 }\n\tc''8\n}"


def test_leaftools_label_leaves_in_expr_with_melodic_chromatic_intervals_02():

    staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    leaftools.label_leaves_in_expr_with_melodic_chromatic_intervals(staff)

    r"""
    \new Staff {
      c'8 ^ \markup { +25 }
      cs'''8 ^ \markup { -14 }
      b'8 ^ \markup { -15 }
      af8 ^ \markup { -10 }
      bf,8 ^ \markup { +1 }
      b,8 ^ \markup { +22 }
      a'8 ^ \markup { +1 }
      bf'8 ^ \markup { -4 }
      fs'8 ^ \markup { -1 }
      f'8
    }
    """

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +25 }\n\tcs'''8 ^ \\markup { -14 }\n\tb'8 ^ \\markup { -15 }\n\taf8 ^ \\markup { -10 }\n\tbf,8 ^ \\markup { +1 }\n\tb,8 ^ \\markup { +22 }\n\ta'8 ^ \\markup { +1 }\n\tbf'8 ^ \\markup { -4 }\n\tfs'8 ^ \\markup { -1 }\n\tf'8\n}"


def test_leaftools_label_leaves_in_expr_with_melodic_chromatic_intervals_03():
    '''Works with quartertones.'''

    staff = Staff(notetools.make_notes([0, 25.5, 11.5, -4, -14, -13, 9, 10, 6.5, 5.5], [Duration(1, 8)]))
    leaftools.label_leaves_in_expr_with_melodic_chromatic_intervals(staff)

    r"""
    \new Staff {
      c'8 ^ \markup { +25.5 }
      dqf'''8 ^ \markup { -14 }
      bqs'8 ^ \markup { -15.5 }
      af8 ^ \markup { -10 }
      bf,8 ^ \markup { +1 }
      b,8 ^ \markup { +22 }
      a'8 ^ \markup { +1 }
      bf'8 ^ \markup { -3.5 }
      gqf'8 ^ \markup { -1 }
      fqs'8
    }
    """

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +25.5 }\n\tdqf'''8 ^ \\markup { -14 }\n\tbqs'8 ^ \\markup { -15.5 }\n\taf8 ^ \\markup { -10 }\n\tbf,8 ^ \\markup { +1 }\n\tb,8 ^ \\markup { +22 }\n\ta'8 ^ \\markup { +1 }\n\tbf'8 ^ \\markup { -3.5 }\n\tgqf'8 ^ \\markup { -1 }\n\tfqs'8\n}"
