# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_replace_leaves_in_expr_with_named_simultaneous_voices_01():
    c = p(r'{ c8 \times 2/3 { c8 c c } \times 4/5 { c16 c c c c } c8 }')
    result = leaftools.replace_leaves_in_expr_with_named_simultaneous_voices(c.select_leaves()[2:7], 'upper', 'lower')
    assert testtools.compare(
        c,
        r'''
        {
            c8
            \times 2/3 {
                c8
                <<
                    \context Voice = "upper" {
                        c8
                        c8
                    }
                    \context Voice = "lower" {
                        c8
                        c8
                    }
                >>
            }
            \times 4/5 {
                <<
                    \context Voice = "upper" {
                        c16
                        c16
                        c16
                    }
                    \context Voice = "lower" {
                        c16
                        c16
                        c16
                    }
                >>
                c16
                c16
            }
            c8
        }
        '''
        )
