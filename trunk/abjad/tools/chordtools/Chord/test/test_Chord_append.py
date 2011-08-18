from abjad import *


def test_Chord_append_01():
    '''Append tweaked note head.
    '''

    chord = Chord([0, 2], Duration(1, 4))
    note_head = notetools.NoteHead(11)
    note_head.tweak.style = 'harmonic'
    chord.append(note_head)

    r'''
    <
        c'
        d'
        \tweak #'style #'harmonic
        b'
    >4
    '''

    assert note_head._client is chord
    assert chord.format == "<\n\tc'\n\td'\n\t\\tweak #'style #'harmonic\n\tb'\n>4"
