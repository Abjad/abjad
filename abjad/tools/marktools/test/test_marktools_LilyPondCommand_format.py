# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_LilyPondCommand_format_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = marktools.LilyPondCommand("#(set-accidental-style 'forget)")
    attach(command, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            #(set-accidental-style 'forget)
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )


def test_marktools_LilyPondCommand_format_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    command = marktools.LilyPondCommand("#(set-accidental-style 'forget)")
    attach(command, staff[1])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8
            #(set-accidental-style 'forget)
            d'8
            e'8
            f'8
        }
        '''
        )


def test_marktools_LilyPondCommand_format_03():
    r'''Barline after leaf.
    '''

    note = Note("c'4")
    command = marktools.LilyPondCommand(r'break', 'after')
    attach(command, note)

    assert testtools.compare(
        note,
        r'''
        c'4
        \break
        '''
        )


def test_marktools_LilyPondCommand_format_04():
    r'''Barline at container closing.
    '''

    staff = Staff()
    command = marktools.LilyPondCommand(r'break')
    attach(command, staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \break
        }
        '''
        )


def test_marktools_LilyPondCommand_format_05():
    r'''Add a natural harmonic.
    '''

    note = Note("c'4")
    command = marktools.LilyPondCommand('flageolet', 'right')
    attach(command, note)
    assert format(note) == "c'4 \\flageolet"


def test_marktools_LilyPondCommandMark_format_06():
    r'''Add then detach natural harmonic.
    '''

    note = Note("c'4")
    command = marktools.LilyPondCommand('flageolet', 'right')
    attach(command, note)
    detach(command, note)
    assert format(note) == "c'4"


def test_marktools_LilyPondCommand_format_07():

    staff = Staff([Note("c'4")])
    command = marktools.LilyPondCommand('compressFullBarRests')
    attach(command, staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \compressFullBarRests
            c'4
        }
        '''
        )


def test_marktools_LilyPondCommand_format_08():

    staff = Staff([Note("c'4")])
    command = marktools.LilyPondCommand('expandFullBarRests')
    attach(command, staff[0])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            \expandFullBarRests
            c'4
        }
        '''
        )


def test_marktools_LilyPondCommand_format_09():
    r'''Voice number can be set on leaves.
    '''

    voice = Voice(scoretools.make_repeated_notes(4))
    command = marktools.LilyPondCommand('voiceOne')
    attach(command, voice[0])

    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceOne
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )


def test_marktools_LilyPondCommand_format_10():
    r'''Voice number can be set to 1, 2, 3, 4, or None.
    Anyhing else will throw a ValueError exception.
    '''

    voice = Voice(scoretools.make_repeated_notes(4))
    command = marktools.LilyPondCommand('voiceOne')
    attach(command, voice[0])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceOne
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )

    detach(command, voice[0])
    command = marktools.LilyPondCommand('voiceTwo')
    attach(command, voice[0])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceTwo
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )

    detach(command, voice[0])
    command = marktools.LilyPondCommand('voiceThree')
    attach(command, voice[0])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceThree
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )

    detach(command, voice[0])
    command = marktools.LilyPondCommand('voiceFour')
    attach(command, voice[0])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceFour
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )

    detach(command, voice[0])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )


def test_marktools_LilyPondCommand_format_11():
    r'''Voice number can be set on a Voice container and on one of the 
    leaves contained in it.
    '''

    voice = Voice(scoretools.make_repeated_notes(4))
    command = marktools.LilyPondCommand('voiceOne')
    attach(command, voice)
    command = marktools.LilyPondCommand('voiceTwo')
    attach(command, voice[1])
    assert testtools.compare(
        voice,
        r'''
        \new Voice {
            \voiceOne
            c'8
            \voiceTwo
            c'8
            c'8
            c'8
        }
        '''
        )
