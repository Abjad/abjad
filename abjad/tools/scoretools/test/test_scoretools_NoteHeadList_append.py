import abjad


def test_scoretools_NoteHeadList_append_01():
    r'''Append tweaked note-head to chord.
    '''

    chord = abjad.Chord("<c' d'>4")
    note_head = abjad.NoteHead("b'")
    note_head.tweak.style = 'harmonic'
    chord.note_heads.append(note_head)

    assert format(chord) == abjad.String.normalize(
        r'''
        <
            c'
            d'
            \tweak style #'harmonic
            b'
        >4
        '''
        )

    assert note_head._client is chord
