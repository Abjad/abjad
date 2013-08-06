# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_melodic_counterpoint_interval_classes_01():


    staff = Staff(notetools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    labeltools.label_leaves_in_expr_with_melodic_counterpoint_interval_classes(staff)

    assert testtools.compare(
        staff.lilypond_format,
        r"""
        \new Staff {
            c'8 ^ \markup { +8 }
            cs'''8 ^ \markup { -2 }
            b'8 ^ \markup { -2 }
            af8 ^ \markup { -7 }
            bf,8 ^ \markup { +1 }
            b,8 ^ \markup { +7 }
            a'8 ^ \markup { +2 }
            bf'8 ^ \markup { -4 }
            fs'8 ^ \markup { +1 }
            f'8
        }
        """
        )
