# -*- coding: utf-8 -*-
import abjad


def test_scoretools_Voice___len___01():
    r'''Voice length returns the number of elements in voice.
    '''

    voice = abjad.Voice()
    assert len(voice) == 0


def test_scoretools_Voice___len___02():
    r'''Voice length returns the number of elements in voice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    assert len(voice) == 4
