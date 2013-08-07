# -*- encoding: utf-8 -*-
from abjad import *


def test_LilyPondCommandMark_format_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(staff)

    r'''
    \new Staff {
        #(set-accidental-style 'forget)
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
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


def test_LilyPondCommandMark_format_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    marktools.LilyPondCommandMark("#(set-accidental-style 'forget)")(staff[1])

    r'''
    \new Staff {
        c'8
        #(set-accidental-style 'forget)
        d'8
        e'8
        f'8
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
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


def test_LilyPondCommandMark_format_03():
    r'''Barline after leaf.
    '''

    note = Note("c'4")
    marktools.LilyPondCommandMark(r'break', 'after')(note)

    r'''
    c'4
    \break
    '''

    assert testtools.compare(
        note.lilypond_format,
        r'''
        c'4
        \break
        '''
        )


def test_LilyPondCommandMark_format_04():
    r'''Barline at container closing.
    '''

    staff = Staff()
    marktools.LilyPondCommandMark(r'break')(staff)

    r'''
    \new Staff {
        \break
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \break
        }
        '''
        )


def test_LilyPondCommandMark_format_05():
    r'''Add a natural harmonic.
    '''

    note = Note("c'4")
    marktools.LilyPondCommandMark('flageolet', 'right')(note)
    assert note.lilypond_format == "c'4 \\flageolet"


def test_LilyPondCommandMark_format_06():
    r'''Add and then remove natural harmonic.
    '''

    note = Note("c'4")
    marktools.LilyPondCommandMark('flageolet', 'right')(note)
    note.select().detach_marks()
    assert note.lilypond_format == "c'4"


def test_LilyPondCommandMark_format_07():

    staff = Staff([Note("c'4")])
    marktools.LilyPondCommandMark('compressFullBarRests')(staff[0])

    r'''
    \new Staff {
        \compressFullBarRests
        c'4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \compressFullBarRests
            c'4
        }
        '''
        )


def test_LilyPondCommandMark_format_08():

    staff = Staff([Note("c'4")])
    marktools.LilyPondCommandMark('expandFullBarRests')(staff[0])

    r'''
    \new Staff {
        \expandFullBarRests
        c'4
    }
    '''

    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            \expandFullBarRests
            c'4
        }
        '''
        )


def test_LilyPondCommandMark_format_09():
    r'''Voice number can be set on leaves.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(voice[0])

    assert testtools.compare(
        voice.lilypond_format,
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


def test_LilyPondCommandMark_format_10():
    r'''Voice number can be set to 1, 2, 3, 4, or None.
    Anyhing else will throw a ValueError exception.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(voice[0])
    assert testtools.compare(
        voice.lilypond_format,
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

    select(voice[0]).detach_marks()
    marktools.LilyPondCommandMark('voiceTwo')(voice[0])
    assert testtools.compare(
        voice.lilypond_format,
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

    select(voice[0]).detach_marks()
    marktools.LilyPondCommandMark('voiceThree')(voice[0])
    assert testtools.compare(
        voice.lilypond_format,
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

    select(voice[0]).detach_marks()
    marktools.LilyPondCommandMark('voiceFour')(voice[0])
    assert testtools.compare(
        voice.lilypond_format,
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

    select(voice[0]).detach_marks()
    assert testtools.compare(
        voice.lilypond_format,
        r'''
        \new Voice {
            c'8
            c'8
            c'8
            c'8
        }
        '''
        )


def test_LilyPondCommandMark_format_11():
    r'''Voice number can be set on a Voice container and on one of the leaves contained in it.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    marktools.LilyPondCommandMark('voiceOne')(voice)
    marktools.LilyPondCommandMark('voiceTwo')(voice[1])
    assert testtools.compare(
        voice.lilypond_format,
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
