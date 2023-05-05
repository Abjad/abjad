import abjad


def test_transpose_from_written_pitch_01():
    voice = abjad.Voice("a'4 a'4 a'4 a'4")
    staff = abjad.Staff([voice])
    trill_pitch = abjad.NamedPitch("b'")
    start_trill_span = abjad.StartTrillSpan(pitch=trill_pitch)
    abjad.attach(start_trill_span, voice[1])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, voice[2])
    instrument = abjad.AltoSaxophone()
    abjad.attach(instrument, voice[0])
    abjad.iterpitches.transpose_from_written_pitch(voice)
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                c'4
                \pitchedTrill
                c'4
                \startTrillSpan d'
                c'4
                \stopTrillSpan
                c'4
            }
        }
        """
    )
