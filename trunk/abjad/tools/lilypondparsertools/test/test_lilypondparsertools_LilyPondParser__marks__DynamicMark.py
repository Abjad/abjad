# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


# TODO: dynamics should accept direction strings.
def test_lilypondparsertools_LilyPondParser__marks__DynamicMark_01():

    target = Staff(Note(-12, (1, 2)) * 6)
    dynamic = contexttools.DynamicMark('ppp')
    dynamic.attach(target[0])
    dynamic = contexttools.DynamicMark('mp')
    dynamic.attach(target[1])
    dynamic = contexttools.DynamicMark('rfz')
    dynamic.attach(target[2])
    dynamic = contexttools.DynamicMark('mf')
    dynamic.attach(target[3])
    dynamic = contexttools.DynamicMark('spp')
    dynamic.attach(target[4])
    dynamic = contexttools.DynamicMark('ff')
    dynamic.attach(target[5])

    string = r'''\new Staff { c2\ppp c\mp c2\rfz c\mf c2\spp c\ff }'''

    parser = LilyPondParser()
    result = parser(string)
    assert target.lilypond_format == result.lilypond_format and \
        target is not result
    for x in result:
        dynamic_marks = inspect(x).get_marks(contexttools.DynamicMark)
        assert len(dynamic_marks) == 1
