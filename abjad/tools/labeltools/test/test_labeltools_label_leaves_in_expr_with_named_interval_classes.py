# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_leaves_in_expr_with_named_interval_classes_01():

    staff = Staff(scoretools.make_notes([0, 25, 11, -4, -14, -13, 9, 10, 6, 5], [Duration(1, 8)]))
    labeltools.label_leaves_in_expr_with_named_interval_classes(staff)

    assert systemtools.TestManager.compare(
        staff,
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
        )
