import abjad


def test_transpose_from_sounding_pitch_01():
    voice = abjad.Voice("c'4 c'4 c'4 c'4")
    staff = abjad.Staff([voice])
    trill_pitch = abjad.NamedPitch("d'")
    start_trill_span = abjad.StartTrillSpan(pitch=trill_pitch)
    abjad.attach(start_trill_span, voice[1])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, voice[2])
    instrument = abjad.AltoSaxophone()
    abjad.attach(instrument, voice[0])
    abjad.iterpitches.transpose_from_sounding_pitch(voice)
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            \new Voice
            {
                a'4
                \pitchedTrill
                a'4
                \startTrillSpan b'
                a'4
                \stopTrillSpan
                a'4
            }
        }
        """
    )
