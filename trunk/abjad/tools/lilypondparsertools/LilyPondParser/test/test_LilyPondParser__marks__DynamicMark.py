from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_LilyPondParser__marks__DynamicMark_01():
    # TODO: Dynamics should accept direction strings. #

    target = Staff(Note(-12, (1, 2)) * 6)
    contexttools.DynamicMark('ppp')(target[0])
    contexttools.DynamicMark('mp')(target[1])
    contexttools.DynamicMark('rfz')(target[2])
    contexttools.DynamicMark('mf')(target[3])
    contexttools.DynamicMark('spp')(target[4])
    contexttools.DynamicMark('ff')(target[5])

    input = r'''\new Staff { c2\ppp c\mp c2\rfz c\mf c2\spp c\ff }'''

    parser = LilyPondParser()
    result = parser(input)
    assert target.format == result.format and target is not result
    for x in result:
        assert 1 == len(contexttools.get_dynamic_marks_attached_to_component(x))
