# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Container___getitem___01():
    r'''Get one container component with positive index.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    voice = Voice(notes)

    assert voice[0] is notes[0]
    assert voice[1] is notes[1]
    assert voice[2] is notes[2]
    assert voice[3] is notes[3]


def test_Container___getitem___02():
    r'''Get one container component with negative index.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    voice = Voice(notes)

    assert voice[-1] is notes[3]
    assert voice[-2] is notes[2]
    assert voice[-3] is notes[1]
    assert voice[-4] is notes[0]


def test_Container___getitem___03():
    r'''Get slice from container.
    '''

    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    voice = Voice(notes)

    assert voice[:1] == notes[:1]
    assert voice[:2] == notes[:2]
    assert voice[:3] == notes[:3]
    assert voice[:4] == notes[:4]


def test_Container___getitem___04():
    r'''Bad index raises IndexError.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")

    assert py.test.raises(IndexError, 'voice[99]')


def test_Container___getitem___05():
    r'''Get one named component in subtree rooted at container.
    '''

    template = scoretemplatetools.StringQuartetScoreTemplate()
    score = template()

    assert score['First Violin Staff'].name == 'First Violin Staff'
    assert score['First Violin Voice'].name == 'First Violin Voice'


def test_Container___getitem___06():
    r'''Bad name raises exception.
    '''

    template = scoretemplatetools.StringQuartetScoreTemplate()
    score = template()

    assert py.test.raises(Exception, "score['Foo']")


def test_Container___getitem___07():
    r'''Duplicate named contexts raise exception.
    '''

    template = scoretemplatetools.StringQuartetScoreTemplate()
    score = template()

    assert score['First Violin Voice'].name == 'First Violin Voice'

    score['Cello Staff'].append(Voice(name='First Violin Voice'))

    assert py.test.raises(Exception, "score['First Violin Voice']")

    extra_first_violin_voice = score['Cello Staff'].pop()

    assert score['First Violin Voice'].name == 'First Violin Voice'
    assert score['First Violin Voice'] is not extra_first_violin_voice
