# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


# TODO: dynamics should accept direction strings.
def test_lilypondparsertools_LilyPondParser__marks__DynamicMark_01():

    target = Staff(Note(-12, (1, 2)) * 6)
    dynamic = marktools.DynamicMark('ppp')
    attach(dynamic, target[0])
    dynamic = marktools.DynamicMark('mp')
    attach(dynamic, target[1])
    dynamic = marktools.DynamicMark('rfz')
    attach(dynamic, target[2])
    dynamic = marktools.DynamicMark('mf')
    attach(dynamic, target[3])
    dynamic = marktools.DynamicMark('spp')
    attach(dynamic, target[4])
    dynamic = marktools.DynamicMark('ff')
    attach(dynamic, target[5])

    string = r'''\new Staff { c2\ppp c\mp c2\rfz c\mf c2\spp c\ff }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
    for x in result:
        dynamic_marks = inspect(x).get_marks(marktools.DynamicMark)
        assert len(dynamic_marks) == 1
