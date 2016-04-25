# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


# TODO: dynamics should accept direction strings.
def test_lilypondparsertools_LilyPondParser__indicators__Dynamic_01():

    target = Staff(Note(-12, (1, 2)) * 6)
    dynamic = Dynamic('ppp')
    attach(dynamic, target[0])
    dynamic = Dynamic('mp')
    attach(dynamic, target[1])
    dynamic = Dynamic('rfz')
    attach(dynamic, target[2])
    dynamic = Dynamic('mf')
    attach(dynamic, target[3])
    dynamic = Dynamic('spp')
    attach(dynamic, target[4])
    dynamic = Dynamic('ff')
    attach(dynamic, target[5])

    string = r'''\new Staff { c2\ppp c\mp c2\rfz c\mf c2\spp c\ff }'''

    parser = LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
    for x in result:
        dynamics = inspect_(x).get_indicators(Dynamic)
        assert len(dynamics) == 1
