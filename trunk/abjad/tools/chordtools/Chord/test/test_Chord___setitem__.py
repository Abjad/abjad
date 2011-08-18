from abjad import *


def test_Chord___setitem___01():
    '''Set chord item with tweaked note head.
    '''

    chord = Chord([3, 13, 17], (1, 4))
    note_head = notetools.NoteHead(3)
    note_head.tweak.color = 'red'
    chord[0] = note_head

    r'''
    <
        \tweak #'color #red
        ef'
        cs''
        f''
    >4
    '''

    assert chord.format == "<\n\t\\tweak #'color #red\n\tef'\n\tcs''\n\tf''\n>4"
