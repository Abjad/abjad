from abjad import *


def test_leaftools_label_leaves_in_expr_with_melodic_diatonic_intervals_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    leaftools.label_leaves_in_expr_with_melodic_diatonic_intervals(staff)

    r'''
    \new Staff {
      c'8 ^ \markup { 2 }
      d'8 ^ \markup { 2 }
      e'8 ^ \markup { 1 }
      f'8 ^ \markup { 2 }
      g'8 ^ \markup { 2 }
      a'8 ^ \markup { 2 }
      b'8 ^ \markup { 1 }
      c''8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +M2 }\n\td'8 ^ \\markup { +M2 }\n\te'8 ^ \\markup { +m2 }\n\tf'8 ^ \\markup { +M2 }\n\tg'8 ^ \\markup { +M2 }\n\ta'8 ^ \\markup { +M2 }\n\tb'8 ^ \\markup { +m2 }\n\tc''8\n}"


def test_leaftools_label_leaves_in_expr_with_melodic_diatonic_intervals_02():

    staff = Staff(notetools.make_notes([0, 13, 11, 8, 2, 3, 9, 10, 6, 5], [Duration(1, 8)]))
    leaftools.label_leaves_in_expr_with_melodic_diatonic_intervals(staff)

    r'''
    \new Staff {
      c'8 ^ \markup { +aug8 }
      cs''8 ^ \markup { -M2 }
      b'8 ^ \markup { -aug2 }
      af'8 ^ \markup { -dim5 }
      d'8 ^ \markup { +m2 }
      ef'8 ^ \markup { +aug4 }
      a'8 ^ \markup { +m2 }
      bf'8 ^ \markup { -dim4 }
      fs'8 ^ \markup { -aug1 }
      f'8
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 ^ \\markup { +aug8 }\n\tcs''8 ^ \\markup { -M2 }\n\tb'8 ^ \\markup { -aug2 }\n\taf'8 ^ \\markup { -dim5 }\n\td'8 ^ \\markup { +m2 }\n\tef'8 ^ \\markup { +aug4 }\n\ta'8 ^ \\markup { +m2 }\n\tbf'8 ^ \\markup { -dim4 }\n\tfs'8 ^ \\markup { -aug1 }\n\tf'8\n}"
