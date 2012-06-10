from abjad import *
import handlertools


def test_NoteAndChordHairpinsHandler_apply_01():


    hairpins = handlertools.dynamics.NoteAndChordHairpinsHandler()
    hairpins.hairpin_tokens.append(('p', '<', 'f'))
    hairpins.hairpin_tokens.append(('p', '<', 'f'))
    hairpins.hairpin_tokens.append(('pp', '<', 'p'))
    hairpins.minimum_prolated_duration = Fraction(1, 8)

    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8 a'32 b'32 r8. c''8 d''8" )
    hairpins.apply(staff)

    r'''
    \new Staff {
        c'8 \< \p
        d'8 \f
        r8
        e'8 \< \p
        f'8 \f
        r8
        g'8 \pp
        r8
        a'32 \p
        b'32
        r8.
        c''8 \< \p
        d''8 \f
    }
    '''

    assert staff.format == "\\new Staff {\n\tc'8 \\< \\p\n\td'8 \\f\n\tr8\n\te'8 \\< \\p\n\tf'8 \\f\n\tr8\n\tg'8 \\pp\n\tr8\n\ta'32 \\p\n\tb'32\n\tr8.\n\tc''8 \\< \\p\n\td''8 \\f\n}"
