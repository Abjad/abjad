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
    assert container.lilypond_format == '{\n}'


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
    assert container.lilypond_format == "{\n\tc'8\n\td'8\n\te'8\n}"


def test_Container___init___03():
    '''Init container with RTM-syntax string.
    '''

    container = Container('rtm: (1 (1 1 1)) (2 (2 (1 (1 1 1)) 2))')

    r'''
    {
        \times 2/3 {
            c'8
            c'8
            c'8
        }
        \times 4/5 {
            c'4
            \times 2/3 {
                c'16
                c'16
                c'16
            }
            c'4
        }
    }
    '''

    assert isinstance(container, Container)
    assert container.lilypond_format == "{\n\t\\times 2/3 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n\t\\times 4/5 {\n\t\tc'4\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\tc'16\n\t\t\tc'16\n\t\t}\n\t\tc'4\n\t}\n}"

def test_Container___init___04():
    '''Init container with "reduced ly" syntax string.
    '''

    container = Container('abj: 2/3 { 8 8 8 }')

    '''
    {
        \times 2/3 {
            c'8
            c'8
            c'8
        }
    }
    '''

    assert isinstance(container, Container)
    assert container.lilypond_format == "{\n\t\\times 2/3 {\n\t\tc'8\n\t\tc'8\n\t\tc'8\n\t}\n}"
