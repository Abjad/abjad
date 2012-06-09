from abjad import *
import handlers


def test_ReiteratedDynamicHandler___call___01():

    reiterated_dynamic = handlers.dynamics.ReiteratedDynamicHandler()
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    reiterated_dynamic('f').apply(staff)

    r'''
    \new Staff {
        c'8 \f
        d'8 \f
        r8
        e'8 \f
        f'8 \f
        r8
        g'8 \f
        r8
        a'32 \f
        b'32 \f
        r8.
        c''8 \f
        d''8 \f
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 \\f\n\td'8 \\f\n\tr8\n\te'8 \\f\n\tf'8 \\f\n\tr8\n\tg'8 \\f\n\tr8\n\ta'32 \\f\n\tb'32 \\f\n\tr8.\n\tc''8 \\f\n\td''8 \\f\n}"
