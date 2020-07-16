import abjad
import abjad.rhythmtrees


def test_parse_rtm_syntax_01():

    rtm = "(3 (1 (3 (1 (3 (1 (3 (1 1 1 1))))))))"
    result = abjad.rhythmtrees.parse_rtm_syntax(rtm)

    assert abjad.lilypond(result) == abjad.String.normalize(
        r"""
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'4
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'4
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'4
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }
            }
        }
        """
    )
