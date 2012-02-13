from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__Markup_01():
    target = Staff([Note(0, 1)])
    markuptools.Markup('hello!', 'up')(target[0])

    r'''\new Staff {
        c'1 ^ \markup { hello! }
    }
    '''

    input = r'''\new Staff { c'1 ^ "hello!" }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
    assert 1 == len(markuptools.get_markup_attached_to_component(result[0]))
