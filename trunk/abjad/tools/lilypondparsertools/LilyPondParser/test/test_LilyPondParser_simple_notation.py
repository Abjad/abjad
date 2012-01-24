from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser



def test_LilyPondParser_leaves_01( ):
    '''LilyPondParser can create the five basic types of leaves.'''
    parser = LilyPondParser( )
    target = Container("c4 r4 s4 R4 <c e g>4")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_leaves_02( ):
    '''LilyPondParser understands dots.'''
    parser = LilyPondParser( )
    target = Container("c4 c8 c16 c32 c4. c8. c16. c32. c4.. c8.. c16.. c32..")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_leaves_03( ):
    '''LilyPondParser understands octave ticks.'''
    parser = LilyPondParser( )
    target = Container("c,,,4 c,,4 c,4 c4 c'4 c''4 c'''4")
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_leaves_04( ):
    '''LilyPondParser understand a variety of note names.'''
    parser = LilyPondParser( )
    target = Container('cff4 ctqf4 cf4 cqf4 c4 cqs4 cs4 ctqs4 css4')
    result = parser(target.format)
    assert result.format == target.format


def test_LilyPondParser_leaves_05( ):
    '''LilyPondParser understands default durations.'''
    parser = LilyPondParser( )
    target = Container('c4 c16.. c16.. c8. c8.')
    input = '{ c c16.. c c8. c }'
    result = parser(input)
    assert result.format == target.format


def test_LilyPondParser_leaves_06( ):
    '''LilyPondParser understands chord repetition.'''
    parser = LilyPondParser( )
    target = Container('<e g bf>4 <e g bf>4 <e g bf>4 <c e g>4 <c e g>4')
    input = '{ <e g bf> q q <c e g> q }'
    result = parser(input)
    assert result.format == target.format
