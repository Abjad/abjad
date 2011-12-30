from abjad import *
import py.test


def test_Chord_note_heads_01():
    '''Returns immutable tuple of note_heads in chord.
    '''

    t = Chord([2, 4, 5], (1, 4))
    note_heads = t.note_heads

    assert isinstance(note_heads, tuple)
    assert len(note_heads) == 3
    assert py.test.raises(AttributeError, 'note_heads.pop()')
    assert py.test.raises(AttributeError, 'note_heads.remove(note_heads[0])')


def test_Chord_note_heads_02():
    '''Chords with equivalent pitch numbers *do* carry equivalent note_head instances.
    '''

    t1 = Chord([2, 4, 5], (1, 4))
    t2 = Chord([2, 4, 5], (1, 4))

    assert t1.note_heads == t2.note_heads


def test_Chord_note_heads_03():
    '''Note head can be assigned with a LilyPond-style note name.
    '''

    t = Chord([0], (1, 4))
    t.note_heads = "c' d' e'"

    assert t.format == "<c' d' e'>4"


def test_Chord_note_heads_04():
    '''Set chord with tweaked note heads.
    '''

    chord = Chord([3, 13, 17], (1, 4))
    note_heads = []
    note_head = notetools.NoteHead(3)
    note_head.tweak.color = 'red'
    note_heads.append(note_head)
    note_head = notetools.NoteHead(13)
    note_head.tweak.color = 'green'
    note_heads.append(note_head)
    note_head = notetools.NoteHead(17)
    note_head.tweak.color = 'blue'
    note_heads.append(note_head)
    chord.note_heads = note_heads

    r'''
    <
        \tweak #'color #red
        ef'
        \tweak #'color #green
        cs''
        \tweak #'color #blue
        f''
    >4
    '''

    assert chord.format == "<\n\t\\tweak #'color #red\n\tef'\n\t\\tweak #'color #green\n\tcs''\n\t\\tweak #'color #blue\n\tf''\n>4"
