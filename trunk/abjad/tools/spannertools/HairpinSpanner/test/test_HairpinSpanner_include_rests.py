from abjad import *


def test_HairpinSpanner_include_rests_01():
    '''Hairpin spanner avoids rests.
    '''

    t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
    spannertools.CrescendoSpanner(t[:], include_rests = False)

    r'''
    \new Staff {
        r8
        r8
        r8
        r8
        e'8 \<
        f'8
        fs'8
        g'8 \!
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n\te'8 \\<\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"


def test_HairpinSpanner_include_rests_02():
    '''Hairpin spanner avoids rests.
    '''

    t = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
    spannertools.CrescendoSpanner(t[:], include_rests = False)


    r'''
    \new Staff {
        c'8 \<
        cs'8
        d'8
        ef'8 \!
        r8
        r8
        r8
        r8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\tr8\n\tr8\n\tr8\n\tr8\n}"
