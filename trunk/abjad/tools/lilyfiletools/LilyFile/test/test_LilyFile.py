from abjad import *


def test_LilyFile_01( ):
    '''LilyFile implements default paper size and global staff size attributes.
    '''

    t = Score([Staff("c'8 d'8 e'8 f'8")])
    lily_file = lilyfiletools.LilyFile( )
    lily_file.append(t)
    lily_file.default_paper_size = '11x17', 'landscape'
    lily_file.global_staff_size = 14
    lily_file.file_initial_system_comments = [ ]
    lily_file.file_initial_system_includes = [ ]

    r'''
    #(set-default-paper-size "11x17" 'landscape)
    #(set-global-staff-size 14)

    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert lily_file.format == '#(set-default-paper-size "11x17" \'landscape)\n#(set-global-staff-size 14)\n\n\\new Score <<\n\t\\new Staff {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n>>'
