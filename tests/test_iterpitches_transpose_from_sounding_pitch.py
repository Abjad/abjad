import abjad


def test_transpose_from_sounding_pitch_01():
    staff = abjad.Staff("c'4 c'4 c'4 c'4")
    trill_pitch = abjad.NamedPitch("d'")
    start_trill_span = abjad.StartTrillSpan(pitch=trill_pitch)
    abjad.attach(start_trill_span, staff[1])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, staff[2])
    instrument = abjad.AltoSaxophone()
    abjad.attach(instrument, staff[0])

    abjad.iterpitches.transpose_from_sounding_pitch(staff)

    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            a'4
            \pitchedTrill
            a'4
            \startTrillSpan b'
            a'4
            \stopTrillSpan
            a'4
        }
        """
    )
