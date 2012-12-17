from abjad import *
from experimental.tools import handlertools


def test_NoteAndChordHairpinHandler_apply_01():

    hairpin = handlertools.dynamics.NoteAndChordHairpinHandler(('p', '<', 'f'))
    staff = Staff("r4 c'8 d'8 r4 e'8 r8")
    hairpin.apply(staff)

    r'''
    \new Staff {
        r4
        c'8 \< \p
        d'8
        r4
        e'8 \f
        r8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tr4\n\tc'8 \\< \\p\n\td'8\n\tr4\n\te'8 \\f\n\tr8\n}"
