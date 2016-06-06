# -*- coding: utf-8 -*-
from abjad import *


def test_rhythmtreetools_parse_rtm_syntax_01():

    rtm = '(3 (1 (3 (1 (3 (1 (3 (1 1 1 1))))))))'
    result = rhythmtreetools.parse_rtm_syntax(rtm)

    assert format(result) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'4
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }
            }
        }
        '''
        )
