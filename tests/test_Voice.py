import copy

import abjad


def test_Voice___copy___01():
    """
    Voices copy name, engraver removals, engraver consists, grob overrides and
    context settings. Voices do not copy components.
    """

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.set_name("SopranoVoice")
    voice_1.get_remove_commands().append("Forbid_line_break_engraver")
    voice_1.get_consists_commands().append("Time_signature_engraver")
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
    Deletes container from voice.
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

    assert abjad.wf.is_wellformed(voice)
    assert abjad.wf.is_wellformed(container)


def test_Voice___init__01():
    """
    Initializes voice with French note names.
    """

    voice = abjad.Voice("do'8 re' mi' fa'", language="français")

    assert repr(voice) == """Voice("c'8 d'8 e'8 f'8")"""


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


def test_Voice_tag_01():
    """
    Voices may be tagged.
    """

    voice = abjad.Voice("c'4 d'4 e'4 f'4", tag=abjad.Tag("RED"))

    assert abjad.lilypond(voice, tags=True) == abjad.string.normalize(
        r"""
          %! RED
        \new Voice
          %! RED
        {
            c'4
            d'4
            e'4
            f'4
          %! RED
        }
        """
    )
