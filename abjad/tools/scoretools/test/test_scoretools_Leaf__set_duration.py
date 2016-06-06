# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Leaf__set_duration_01():
    r'''Change leaf to tied duration.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    voice[1]._set_duration(Duration(5, 32))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ~
            d'32 ]
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()

def test_scoretools_Leaf__set_duration_02():
    r'''Change tied leaf to tied value.
    Duplicate ties are not created.
    '''

    voice = Voice("c'8 c'8 c'8 c'8")
    tie = spannertools.Tie()
    attach(tie, voice[:2])
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~ [
            c'8 ]
            c'8
            c'8
        }
        '''
        )

    voice[1]._set_duration(Duration(5, 32))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 ~ [
            c'8 ~
            c'32 ]
            c'8
            c'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Leaf__set_duration_03():
    r'''Change leaf to nontied duration.
    Same as voice.written_duration = Duration(3, 16).
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    voice[1]._set_duration(Duration(3, 16))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8. ]
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Leaf__set_duration_04():
    r'''Change leaf to tied duration without power-of-two denominator.
    Tuplet inserted over new tied notes.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    voice[1]._set_duration(Duration(5, 48))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8 ~
                d'32 ]
            }
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Leaf__set_duration_05():
    r'''Change leaf to untied duration without power-of-two denominator.
    Tuplet inserted over input leaf.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:2])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            d'8 ]
            e'8
            f'8
        }
        '''
        )

    voice[1]._set_duration(Duration(1, 12))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8 ]
            }
            e'8
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Leaf__set_duration_06():
    r'''Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf written
    duration does not.
    '''

    note = Note(0, (1, 8))
    attach(Multiplier(1, 2), note)

    assert format(note) == "c'8 * 1/2"

    note._set_duration(Duration(1, 32))

    assert inspect_(note).is_well_formed()
    assert format(note) == "c'8 * 1/4"


def test_scoretools_Leaf__set_duration_07():
    r'''Change leaf with LilyPond multiplier to untied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    '''

    note = Note(0, (1, 8))
    attach(Multiplier(1, 2), note)

    assert format(note) == "c'8 * 1/2"

    note._set_duration(Duration(3, 32))

    assert inspect_(note).is_well_formed()
    assert format(note) == "c'8 * 3/4"


def test_scoretools_Leaf__set_duration_08():
    r'''Change leaf with LilyPond multiplier to tied duration with
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    '''

    note = Note(0, (1, 8))
    attach(Multiplier(1, 2), note)

    assert format(note) == "c'8 * 1/2"

    note._set_duration(Duration(5, 32))

    assert inspect_(note).is_well_formed()
    assert format(note) == "c'8 * 5/4"


def test_scoretools_Leaf__set_duration_09():
    r'''Change leaf with LilyPond multiplier to duration without
    power-of-two denominator. LilyPond multiplier changes but leaf
    written duration does not.
    '''

    note = Note(0, (1, 8))
    attach(Multiplier(1, 2), note)

    assert format(note) == "c'8 * 1/2"

    note._set_duration(Duration(1, 24))

    assert inspect_(note).is_well_formed()
    assert format(note) == "c'8 * 1/3"


def test_scoretools_Leaf__set_duration_10():
    r'''Change leaf with LilyPond multiplier.
    Change to tie-necessitating duration without power-of-two denominator.
    LilyPond multiplier changes but leaf written duration does not.
    '''

    note = Note(0, (1, 8))
    attach(Multiplier(1, 2), note)

    assert format(note) == "c'8 * 1/2"

    note._set_duration(Duration(5, 24))

    assert inspect_(note).is_well_formed()
    assert format(note) == "c'8 * 5/3"


def test_scoretools_Leaf__set_duration_11():
    r'''Change rest duration.
    '''

    voice = Voice("c'8 r8 e'8 f'8")
    beam = Beam()
    attach(beam, voice[:3])

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            r8
            e'8 ]
            f'8
        }
        '''
        )

    voice[1]._set_duration(Duration(5, 32))

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            r8
            r32
            e'8 ]
            f'8
        }
        '''
        )

    assert inspect_(voice).is_well_formed()
