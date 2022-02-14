import copy

import abjad


def test_Chord___deepcopy___01():
    """
    Chord deepchopies note-heads.
    """

    chord_1 = abjad.Chord("<c' e' g'>4")
    abjad.tweak(chord_1.note_heads[0]).color = "#red"
    chord_2 = copy.deepcopy(chord_1)

    assert abjad.lilypond(chord_1) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_2) == abjad.string.normalize(
        r"""
        <
            \tweak color #red
            c'
            e'
            g'
        >4
        """
    )

    assert abjad.lilypond(chord_1) == abjad.lilypond(chord_2)
    assert chord_1 is not chord_2

    assert chord_1.note_heads[0] == chord_2.note_heads[0]
    assert chord_1.note_heads[1] == chord_2.note_heads[1]
    assert chord_1.note_heads[2] == chord_2.note_heads[2]

    assert chord_1.note_heads[0] is not chord_2.note_heads[0]
    assert chord_1.note_heads[1] is not chord_2.note_heads[1]
    assert chord_1.note_heads[2] is not chord_2.note_heads[2]
