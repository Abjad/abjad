from abjad import *
import handlertools


def test_TerracedDynamicsHandler___call___01():

    terraces = handlertools.dynamics.TerracedDynamicsHandler()
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    terraces(['p', 'f']).apply(staff)

    r'''
    \new Staff {
        c'8 \p
        d'8 \f
        r8
        e'8 \p
        f'8 \f
        r8
        g'8 \p
        r8
        a'32 \f
        b'32 \p
        r8.
        c''8 \f
        d''8 \p
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 \\p\n\td'8 \\f\n\tr8\n\te'8 \\p\n\tf'8 \\f\n\tr8\n\tg'8 \\p\n\tr8\n\ta'32 \\f\n\tb'32 \\p\n\tr8.\n\tc''8 \\f\n\td''8 \\p\n}"
