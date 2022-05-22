import abjad


def test_transpose_from_written_pitch_01():
    staff = abjad.Staff("a'4 a'4 a'4 a'4")
    trill_pitch = abjad.NamedPitch("b'")
    start_trill_span = abjad.StartTrillSpan(pitch=trill_pitch)
    abjad.attach(start_trill_span, staff[1])
    stop_trill_span = abjad.StopTrillSpan()
    abjad.attach(stop_trill_span, staff[2])
    instrument = abjad.AltoSaxophone()
    abjad.attach(instrument, staff[0])

    abjad.iterpitches.transpose_from_written_pitch(staff)

    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            c'4
            \pitchedTrill
            c'4
            \startTrillSpan d'
            c'4
            \stopTrillSpan
            c'4
        }
        """
    )
