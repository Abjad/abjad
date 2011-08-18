from abjad import *
import py.test


def test_Container___getitem___01():
    '''Get one container component with positive index.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    t = Voice(notes)

    assert t[0] is notes[0]
    assert t[1] is notes[1]
    assert t[2] is notes[2]
    assert t[3] is notes[3]


def test_Container___getitem___02():
    '''Get one container component with negative index.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    t = Voice(notes)

    assert t[-1] is notes[3]
    assert t[-2] is notes[2]
    assert t[-3] is notes[1]
    assert t[-4] is notes[0]


def test_Container___getitem___03():
    '''Get slice from container.'''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    t = Voice(notes)

    assert t[:1] == notes[:1]
    assert t[:2] == notes[:2]
    assert t[:3] == notes[:3]
    assert t[:4] == notes[:4]


def test_Container___getitem___04():
    '''Bad index raises IndexError.'''

    t = Voice("c'8 d'8 e'8 f'8")

    assert py.test.raises(IndexError, 't[99]')
