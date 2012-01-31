from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser



def test_LilyPondParser_simple_notation_01( ):
    '''LilyPondParser can create the five basic types of leaves.'''
    parser = LilyPondParser( )
    target = Container("c4 r4 s4 R4 <c e g>4")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_02( ):
    '''LilyPondParser understands dots.'''
    parser = LilyPondParser( )
    target = Container(
        r"c1 c2 c4 c8 c16 c32 c64 c128 "
        r"c1. c2. c4. c8. c16. c32. c64. c128. "
        r"c1.. c2.. c4.. c8.. c16.. c32.. c64.. c128..")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_03( ):
    '''LilyPondParser understands \maxima, \longa and \breve.'''
    parser = LilyPondParser( )
    target = Container(r'c\maxima c\longa c\breve c\breve...')
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_04( ):
    '''LilyPondParser understands octave ticks.'''
    parser = LilyPondParser( )
    target = Container("c,,,4 c,,4 c,4 c4 c'4 c''4 c'''4")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_05( ):
    '''LilyPondParser understand a variety of note names.'''
    parser = LilyPondParser( )
    target = Container('cff4 ctqf4 cf4 cqf4 c4 cqs4 cs4 ctqs4 css4')
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_06( ):
    '''LilyPondParser understands default durations.'''
    parser = LilyPondParser( )
    target = Container('c4 c16.. c16.. c8. c8.')
    input = '{ c c16.. c c8. c }'
    result = parser(input)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_07( ):
    '''LilyPondParser understands chord repetition.'''
    parser = LilyPondParser( )
    target = Container('<e g bf>4 <e g bf>4 <e g bf>4 <c e g>4 <c e g>4')
    input = '{ <e g bf> q q <c e g> q }'
    result = parser(input)
    assert result.format == target.format


def test_LilyPondParser_simple_notation_08( ):
    '''LilyPondParser understands common context types.'''
    parser = LilyPondParser( )
    for context in [scoretools.PianoStaff, Score, Staff, scoretools.StaffGroup, Voice]:
        component = context([ ])
        assert component.format == parser(component.format).format


def test_LilyPondParser_simple_notation_09( ):
    '''LilyPondParser understands variable assignment.'''
    parser = LilyPondParser( )
    target = Container([
        Container([Note(0, (1, 4)), Note(2, (1, 4)), Note(4, (1, 4)), Note(5, (1, 4))]), 
        Container([Note(0, (1, 4)), Note(2, (1, 4)), Note(4, (1, 4)), Note(5, (1, 4))]), 
        Container([Note(0, (1, 4)), Note(2, (1, 4)), Note(4, (1, 4)), Note(5, (1, 4))]), 
    ])
    input = r"foo = { c' d' e' f' } { \foo \foo \foo }"
    result = parser(input)
    assert result.format == target.format

