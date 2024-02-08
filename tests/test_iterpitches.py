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


def test_transpose_from_sounding_pitch_02():
    """
    REGRESSION #1577. Do not lose note-head tweaks on chords during transposition.
    """
    staff = abjad.Staff("<d'' fs''>8 e'4")
    abjad.attach(abjad.Violin(), staff[0])
    abjad.tweak(staff[0].note_heads[1], r"\tweak color #red")
    abjad.tweak(staff[1].note_head, r"\tweak color #blue")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            <
                d''
                \tweak color #red
                fs''
            >8
            \tweak color #blue
            e'4
        }
        """
    )
    abjad.iterpitches.transpose_from_sounding_pitch(staff)
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            <
                d''
                \tweak color #red
                fs''
            >8
            \tweak color #blue
            e'4
        }
        """
    )


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


def test_transpose_from_written_pitch_02():
    """
    REGRESSION #1577. Do not lose note-head tweaks on chords during transposition.
    """
    staff = abjad.Staff("<d'' fs''>8 e'4")
    abjad.attach(abjad.Violin(), staff[0])
    abjad.tweak(staff[0].note_heads[1], r"\tweak color #red")
    abjad.tweak(staff[1].note_head, r"\tweak color #blue")
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            <
                d''
                \tweak color #red
                fs''
            >8
            \tweak color #blue
            e'4
        }
        """
    )
    abjad.iterpitches.transpose_from_written_pitch(staff)
    string = abjad.lilypond(staff)
    assert string == abjad.string.normalize(
        r"""
        \new Staff
        {
            <
                d''
                \tweak color #red
                fs''
            >8
            \tweak color #blue
            e'4
        }
        """
    )
