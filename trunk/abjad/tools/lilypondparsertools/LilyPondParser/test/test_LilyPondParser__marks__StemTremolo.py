from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__StemTremolo_01():
    target = Staff([Note(0, 1)])
    marktools.StemTremolo(4)(target[0])

    r'''\new Staff {
        c'1 :4
    }
    '''

    parser = LilyPondParser()
    result = parser(target.format)
    assert target.format == result.format and target is not result
    assert 1 == len(marktools.get_stem_tremolos_attached_to_component(result[0]))
