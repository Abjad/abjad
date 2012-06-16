from abjad import *
from abjad.tools import *


def test_TupletMonadTimeTokenMaker___call___01():

    maker = timetokentools.TupletMonadTimeTokenMaker()

    duration_tokens = [(1, 5), (1, 4), (1, 6), (7, 9)]
    tuplet_lists = maker(duration_tokens)
    tuplets = sequencetools.flatten_sequence(tuplet_lists)
    staff = Staff(tuplets)

    r'''
    \new Staff {
        \times 4/5 {
            c'4
        }
        {
            c'4
        }
        \times 2/3 {
            c'4
        }
        \times 8/9 {
            c'2..
        }
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\t\\times 4/5 {\n\t\tc'4\n\t}\n\t{\n\t\tc'4\n\t}\n\t\\times 2/3 {\n\t\tc'4\n\t}\n\t\\times 8/9 {\n\t\tc'2..\n\t}\n}"
