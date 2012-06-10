from abjad import *
import handlertools


def test_TerracedDynamicsHandler_apply_01():

    terraces = handlertools.dynamics.TerracedDynamicsHandler(['f', 'mp', 'mf', 'mp', 'ff'])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    terraces.apply(staff)

    r'''
    \new Staff {
        c'8 \f
        d'8 \mp
        r8
        e'8 \mf
        f'8 \mp
        r8
        g'8 \ff
        r8
        a'32 \f
        b'32 \mp
        r8.
        c''8 \mf
        d''8 \mp
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 \\f\n\td'8 \\mp\n\tr8\n\te'8 \\mf\n\tf'8 \\mp\n\tr8\n\tg'8 \\ff\n\tr8\n\ta'32 \\f\n\tb'32 \\mp\n\tr8.\n\tc''8 \\mf\n\td''8 \\mp\n}"
