import abjad


def test_Meter_rewrite_meter_01():
    string = "| 4/4 c'4 c'8 c'4 c'4 c'8 |"
    container = abjad.parsers.reduced.parse_reduced_ly_syntax(string)
    staff = abjad.Staff()
    staff[:] = container
    abjad.Score([staff], name="Score")
    grace_container = abjad.BeforeGraceContainer("c'16 d'16")
    abjad.attach(grace_container, staff[1])
    meter = abjad.Meter((4, 4))
    abjad.Meter.rewrite_meter(staff[:], meter)
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \time 4/4
            c'4
            \grace {
                c'16
                d'16
            }
            c'8
            c'8
            ~
            c'8
            c'8
            ~
            c'8
            c'8
        }
        """
    ), print(string)
