import abjad


def test_AfterGraceContainer_01():
    r"""
    REGRESSION. LilyPond \afterGrace must lexically precede LilyPond \pitchedTrill.
    """

    voice = abjad.Voice("c'1")
    container = abjad.IndependentAfterGraceContainer("e'8")
    voice.append(container)
    voice.append("r4")
    start_trill_span = abjad.StartTrillSpan(pitch=abjad.NamedPitch("D4"))
    abjad.attach(start_trill_span, voice[0])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, voice[-1])

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            \afterGrace
            \pitchedTrill
            c'1
            \startTrillSpan d'
            {
                e'8
            }
            r4
            \stopTrillSpan
        }
        """
    )
