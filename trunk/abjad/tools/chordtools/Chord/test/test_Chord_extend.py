from abjad import *


def test_Chord_extend_01():
    '''Extend tweaked note heads.
    '''

    chord = Chord([3], (1, 4))
    note_heads = []
    note_head = notetools.NoteHead(13)
    note_head.tweak.color = 'blue'
    note_heads.append(note_head)
    note_head = notetools.NoteHead(17)
    note_head.tweak.color = 'green'
    note_heads.append(note_head)
    chord.extend(note_heads)

    r'''
    <
        ef'
        \tweak #'color #blue
        cs''
        \tweak #'color #green
        f''
    >4
    '''

    chord.format == "<\n\tef'\n\t\\tweak #'color #blue\n\tcs''\n\t\\tweak #'color #green\n\tf''\n>4"
