from abjad import *


def test_Container___init___01():
    '''Init empty container.
    '''

    container = Container([])

    r'''
    {
    }
    '''

    assert isinstance(container, Container)
    assert container.format == '{\n}'


def test_Container___init___02():
    '''Init container with LilyPond note-entry string.
    '''

    container = Container("c'8 d'8 e'8")

    r'''
    {
        c'8
        d'8
        e'8
    }
    '''

    assert isinstance(container, Container)
    assert container.format == "{\n\tc'8\n\td'8\n\te'8\n}"
