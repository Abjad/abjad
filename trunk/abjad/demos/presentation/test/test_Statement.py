from abjad.demos.presentation.presentation import *


def test_Statement_01( ):
    '''A statement can be initialized with no arguments.'''
    t = Statement( )
    assert t.text == ' '
    assert t.code == [ ]


def test_Statement_02( ):
    '''A statement's code can be set to an executable string.'''
    text = 'Hello!'
    code = 'x = 3'
    t = Statement(text, code)
    assert t.code == [code]


def test_Statement_03( ):
    '''A statement's code can be a list of executable strings.'''
    text = 'Hello!'
    code = ['x = 3', 'y = x * 2']
    t = Statement(text, code)
    assert t.code == code
