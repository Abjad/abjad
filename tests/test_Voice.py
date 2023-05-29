import copy

import abjad


def test_Voice___copy___01():
    """
    Voices copy name, engraver removals, engraver consists, grob overrides and
    context settings. Voices do not copy components.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.name = "SopranoVoice"
    voice_1.remove_commands.append("Forbid_line_break_engraver")
    voice_1.consists_commands.append("Time_signature_engraver")
    abjad.override(voice_1).NoteHead.color = "#red"
    abjad.setting(voice_1).tupletFullLength = True
    voice_2 = copy.copy(voice_1)

    assert abjad.lilypond(voice_2) == abjad.string.normalize(
        r"""
        \context Voice = "SopranoVoice"
        \with
        {
            \remove Forbid_line_break_engraver
            \consists Time_signature_engraver
            \override NoteHead.color = #red
            tupletFullLength = ##t
        }
        {
        }
        """
    )


def test_Voice___delitem___01():
    """
    Delete container from voice.
    """

    voice = abjad.Voice(
        r"""
        c'8
        [
        \glissando
        {
            d'8
            \glissando
            e'8
            \glissando
        }
        f'8 ]
        """
    )

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            {
                d'8
                \glissando
                e'8
                \glissando
            }
            f'8
            ]
        }
        """
    )

    container = voice[1]
    del voice[1:2]

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \glissando
            f'8
            ]
        }
        """
    )

    assert abjad.wf.wellformed(voice)
    assert abjad.wf.wellformed(container)


def test_Voice___len___01():
    """
    Voice length returns the number of elements in voice.
    """

    voice = abjad.Voice()
    assert len(voice) == 0


def test_Voice___len___02():
    """
    Voice length returns the number of elements in voice.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    assert len(voice) == 4


def test_Voice_lilypond_voice_resolution_01():
    """
    Anonymous voice with a sequence of leaves,
    in the middle of which there is a simultaneous,
    which in turn contains two anonymous voices.
    How does LilyPond resolve voices?
    LilyPond identifies three separate voices.
    LilyPond colors the outer four notes (c'8 d'8 b'8 c''8) red.
    LilyPond colors the inner four notes black.
    LilyPond issues clashing note column warnings for the inner notes.
    How should Abjad resolve voices?
    """

    voice = abjad.Voice("c'8 d'8 b'8 c''8")
    voice.insert(2, abjad.Container([abjad.Voice("e'8 f'8"), abjad.Voice("g'8 a'8")]))
    voice[2].simultaneous = True
    abjad.override(voice).NoteHead.color = "#red"

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \new Voice
        \with
        {
            \override NoteHead.color = #red
        }
        {
            c'8
            d'8
            <<
                \new Voice
                {
                    e'8
                    f'8
                }
                \new Voice
                {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        """
    )


def test_Voice_lilypond_voice_resolution_02():
    """
    Named voice with  with a sequence of leaves,
    in the middle of which there is a simultaneous,
    which in turn contains one like-named and one differently named voice.
    How does LilyPond resolve voices?
    """

    voice = abjad.Voice("c'8 d'8 b'8 c''8")
    voice.name = "foo"
    voice.insert(2, abjad.Container([abjad.Voice("e'8 f'8"), abjad.Voice("g'8 a'8")]))
    voice[2].simultaneous = True
    voice[2][0].name = "foo"
    abjad.override(voice).NoteHead.color = "#red"

    assert abjad.lilypond(voice) == abjad.string.normalize(
        r"""
        \context Voice = "foo"
        \with
        {
            \override NoteHead.color = #red
        }
        {
            c'8
            d'8
            <<
                \context Voice = "foo"
                {
                    e'8
                    f'8
                }
                \new Voice
                {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        """
    )

    """
    LilyPond colors six notes red and two notes black.
    LilyPond identifies two voices.
    """


def test_Voice_lilypond_voice_resolution_03():
    """
    Container containing a run of leaves.
    Two like-structured simultaneouss in the middle of the run.
    LilyPond handles this example perfectly.
    LilyPond colors the four note_heads of the soprano voice red.
    LilyPond colors all other note_heads black.
    """

    container = abjad.Container(
        r"""
        c'8
        <<
            \context Voice = "alto" {
                d'8
                e'8
            }
            \context Voice = "soprano" {
                f'8
                g'8
            }
        >>
        <<
            \context Voice = "alto" {
                a'8
                b'8
            }
            \context Voice = "soprano" {
                c''8
                d''8
            }
        >>
        e''8
        """
    )

    abjad.override(container[1][1]).NoteHead.color = "#red"
    abjad.override(container[2][1]).NoteHead.color = "#red"

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            c'8
            <<
                \context Voice = "alto"
                {
                    d'8
                    e'8
                }
                \context Voice = "soprano"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    f'8
                    g'8
                }
            >>
            <<
                \context Voice = "alto"
                {
                    a'8
                    b'8
                }
                \context Voice = "soprano"
                \with
                {
                    \override NoteHead.color = #red
                }
                {
                    c''8
                    d''8
                }
            >>
            e''8
        }
        """
    )
