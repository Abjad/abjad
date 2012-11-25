from abjad import *


def test_rhythmtreetools_parse_rtm_syntax_01():

    rtm = '(3 (1 (3 (1 (3 (1 (3 (1 1 1 1))))))))'
    result = rhythmtreetools.parse_rtm_syntax(rtm)

    r'''
    \fraction \times 3/4 {
        c'4
        \fraction \times 3/4 {
            c'4
            \fraction \times 3/4 {
                c'4
                \fraction \times 3/4 {
                    c'4
                    c'4
                    c'4
                    c'4
                }
            }
        }
    }
    '''

    assert result.lilypond_format == "\\fraction \\times 3/4 {\n\tc'4\n\t\\fraction \\times 3/4 {\n\t\tc'4\n\t\t\\fraction \\times 3/4 {\n\t\t\tc'4\n\t\t\t\\fraction \\times 3/4 {\n\t\t\t\tc'4\n\t\t\t\tc'4\n\t\t\t\tc'4\n\t\t\t\tc'4\n\t\t\t}\n\t\t}\n\t}\n}"

