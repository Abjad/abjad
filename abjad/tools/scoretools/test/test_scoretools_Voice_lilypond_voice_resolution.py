# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Voice_lilypond_voice_resolution_01():
    r'''Anonymous voice with a sequence of leaves,
    in the middle of which there is a simultaneous,
    which in turn contains two anonymous voices.
    How does LilyPond resolve voices?
    LilyPond identifies three separate voices.
    LilyPond colors the outer four notes (c'8 d'8 b'8 c''8) red.
    LilyPond colors the inner four notes black.
    LilyPond issues clashing note column warnings for the inner notes.
    How should Abjad resolve voices?
    '''

    voice = Voice("c'8 d'8 b'8 c''8")
    voice.insert(2, Container([Voice("e'8 f'8"), Voice("g'8 a'8")]))
    voice[2].is_simultaneous = True
    override(voice).note_head.color = 'red'

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice \with {
            \override NoteHead.color = #red
        } {
            c'8
            d'8
            <<
                \new Voice {
                    e'8
                    f'8
                }
                \new Voice {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        '''
        )



def test_scoretools_Voice_lilypond_voice_resolution_02():
    r'''Named voice with  with a sequence of leaves,
    in the middle of which there is a simultaneous,
    which in turn contains one like-named and one differently named voice.
    How does LilyPond resolve voices?
    '''

    voice = Voice("c'8 d'8 b'8 c''8")
    voice.name = 'foo'
    voice.insert(2, Container([Voice("e'8 f'8"), Voice("g'8 a'8")]))
    voice[2].is_simultaneous = True
    voice[2][0].name = 'foo'
    override(voice).note_head.color = 'red'

    assert format(voice) == stringtools.normalize(
        r'''
        \context Voice = "foo" \with {
            \override NoteHead.color = #red
        } {
            c'8
            d'8
            <<
                \context Voice = "foo" {
                    e'8
                    f'8
                }
                \new Voice {
                    g'8
                    a'8
                }
            >>
            b'8
            c''8
        }
        ''',
        )

    r'''
    LilyPond colors six notes red and two notes black.
    LilyPond identifies two voices.
    '''


def test_scoretools_Voice_lilypond_voice_resolution_03():
    r'''Two like-named voices in two differently named staves.
    LilyPond gives unterminated beam warnings.
    LilyPond gives grob direction programming errors.
    We conclude that LilyPond identifies two separate voices.
    Good example for Abjad voice resolution.
    '''

    container = Container()
    container.append(Staff([Voice("c'8 d'8")]))
    container.append(Staff([Voice("e'8 f'8")]))
    container[0].name = 'staff1'
    container[1].name = 'staff2'
    container[0][0].name = 'voicefoo'
    container[1][0].name = 'voicefoo'
    beam = Beam()
    leaves = select(container).by_leaf()
    statement = 'attach(beam, leaves)'
    pytest.raises(Exception, statement)


def test_scoretools_Voice_lilypond_voice_resolution_04():
    r'''Container containing a run of leaves.
    Two like-structured simultaneouss in the middle of the run.
    LilyPond handles this example perfectly.
    LilyPond colors the four note_heads of the soprano voice red.
    LilyPond colors all other note_heads black.
    '''

    container = Container(
        r'''
        c'8
        <<
            \context Voice = "alto" {
                d'8
                e'8
            }
            \context Voice = "soprano" {
                f'8
                g'8
            }
        >>
        <<
            \context Voice = "alto" {
                a'8
                b'8
            }
            \context Voice = "soprano" {
                c''8
                d''8
            }
        >>
        e''8
        '''
        )

    override(container[1][1]).note_head.color = 'red'
    override(container[2][1]).note_head.color = 'red'

    assert format(container) == stringtools.normalize(
        r'''
        {
            c'8
            <<
                \context Voice = "alto" {
                    d'8
                    e'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead.color = #red
                } {
                    f'8
                    g'8
                }
            >>
            <<
                \context Voice = "alto" {
                    a'8
                    b'8
                }
                \context Voice = "soprano" \with {
                    \override NoteHead.color = #red
                } {
                    c''8
                    d''8
                }
            >>
            e''8
        }
        ''',
        )
