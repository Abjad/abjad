# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_replace_leaves_in_expr_with_simultaneous_voices_01():
    c = p(r'{ c8 \times 2/3 { c8 c c } \times 4/5 { c16 c c c c } c8 }')
    result = leaftools.replace_leaves_in_expr_with_simultaneous_voices(c.select_leaves()[2:7])
    assert testtools.compare(
        c.lilypond_format,
        r'''
        {
            c8
            \times 2/3 {
                c8
                <<
                    \new Voice {
                        c8
                        c8
                    }
                    \new Voice {
                        c8
                        c8
                    }
                >>
            }
            \times 4/5 {
                <<
                    \new Voice {
                        c16
                        c16
                        c16
                    }
                    \new Voice {
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
