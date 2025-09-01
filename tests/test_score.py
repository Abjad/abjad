import abjad


def test_score_copy_overrides_settings_and_wrappers_01():

    note = abjad.Note("c'4")
    abjad.override(note).NoteHead.color = "#red"
    abjad.setting(note).tupletFullLength = True
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, note)

    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        \once \override NoteHead.color = #red
        \set tupletFullLength = ##t
        c'4
        - \staccato
        """
    )

    chord = abjad.Chord("<c' d' bf'>4")
    abjad.score.copy_overrides_settings_and_wrappers(note, chord)

    assert abjad.lilypond(chord) == abjad.string.normalize(
        r"""
        \once \override NoteHead.color = #red
        \set tupletFullLength = ##t
        <c' d' bf'>4
        - \staccato
        """
    )
