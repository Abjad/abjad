from abjad import *


#def test_HairpinSpanner___copy___01():
#   '''Do not copy incomplete hairpins.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   spannertools.CrescendoSpanner(staff[:4])
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   staff.append(staff[0].copy())
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tc'8\n}"
#   '''
#   \new Staff {
#           c'8 \<
#           cs'8
#           d'8
#           ef'8 \!
#           e'8
#           f'8
#           fs'8
#           g'8
#           c'8
#   }
#   '''


def test_HairpinSpanner___copy___02():
    '''Do copy complete hairpins.'''
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    spannertools.CrescendoSpanner(staff[:4])
    assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
    #staff.extend(staff.copy(0, 3))
    staff.extend(componenttools.copy_components_and_immediate_parent_of_first_component(staff[0:4]))
    assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n}"
    '''
    \new Staff {
        c'8 \<
        cs'8
        d'8
        ef'8 \!
        e'8
        f'8
        fs'8
        g'8
        c'8 \<
        cs'8
        d'8
        ef'8 \!
    }
    '''
