from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__KeySignatureMark_01():
    target = Staff([Note("fs'", 1)])
    contexttools.KeySignatureMark('g', 'major')(target[0])

    r'''\new Staff {
        \key g \major
        fs'1
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
    assert 1 == len(contexttools.get_key_signature_marks_attached_to_component(result[0]))
