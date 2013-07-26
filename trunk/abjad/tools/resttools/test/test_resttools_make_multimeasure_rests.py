from abjad import *


def test_resttools_make_multimeasure_rests_01():

    mmrs = resttools.make_multimeasure_rests([(4, 8), (6, 8), (7, 8)])
    staff = Staff(mmrs)

    r'''
    \new Staff {
        R2
        R2.
        R2..
    }
    '''

    staff.lilypond_format == '\\new Staff {\n\tR2\n\tR2.\n\tR2..\n}'
