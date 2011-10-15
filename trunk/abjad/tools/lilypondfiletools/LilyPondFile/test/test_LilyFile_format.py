from abjad import *


def test_LilyFile_format_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
    lilypond_file.file_initial_system_comments = []
    lilypond_file.file_initial_system_includes = []
    lilypond_file.file_initial_user_comments.append('User comments 1.')
    lilypond_file.file_initial_user_comments.append('User comments 2.')
    lilypond_file.file_initial_user_includes.append('external-settings-file-1.ly')
    lilypond_file.file_initial_user_includes.append('external-settings-file-2.ly')
    lilypond_file.default_paper_size = 'letter', 'portrait'
    lilypond_file.global_staff_size = 16
    lilypond_file.header_block.composer = markuptools.Markup('Josquin')
    lilypond_file.header_block.title = markuptools.Markup('Missa sexti tonus')
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.left_margin = 15
    lilypond_file.paper_block.oddFooterMarkup = markuptools.Markup('The odd-page footer')
    lilypond_file.paper_block.evenFooterMarkup = markuptools.Markup('The even-page footer')

    r'''
    % User comments 1.
    % User comments 2.

    \include "external-settings-file-1.ly"
    \include "external-settings-file-2.ly"

    #(set-default-paper-size "letter" 'portrait)
    #(set-global-staff-size 16)

    \header {
        composer = \markup { Josquin }
        title = \markup { Missa sexti tonus }
    }

    \layout {
        indent = #0
        left-margin = #15
    }

    \paper {
        evenFooterMarkup = \markup { The even-page footer }
        oddFooterMarkup = \markup { The odd-page footer }
    }

    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert lilypond_file.format == '% User comments 1.\n% User comments 2.\n\n\\include "external-settings-file-1.ly"\n\\include "external-settings-file-2.ly"\n\n#(set-default-paper-size "letter" \'portrait)\n#(set-global-staff-size 16)\n\n\\header {\n\tcomposer = \\markup { Josquin }\n\ttitle = \\markup { Missa sexti tonus }\n}\n\n\\layout {\n\tindent = #0\n\tleft-margin = #15\n}\n\n\\paper {\n\tevenFooterMarkup = \\markup { The even-page footer }\n\toddFooterMarkup = \\markup { The odd-page footer }\n}\n\n\\score {\n\t\\new Staff {\n\t\tc\'8\n\t\td\'8\n\t\te\'8\n\t\tf\'8\n\t}\n}'
