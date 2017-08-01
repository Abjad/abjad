# -*- coding: utf-8 -*-
import abjad


# TODO: dynamics should accept direction strings.
def test_lilypondparsertools_LilyPondParser__indicators__Dynamic_01():

    target = abjad.Staff(abjad.Note(-12, (1, 2)) * 6)
    dynamic = abjad.Dynamic('ppp')
    abjad.attach(dynamic, target[0])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, target[1])
    dynamic = abjad.Dynamic('rfz')
    abjad.attach(dynamic, target[2])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, target[3])
    dynamic = abjad.Dynamic('spp')
    abjad.attach(dynamic, target[4])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, target[5])

    string = r'''\new Staff { c2\ppp c\mp c2\rfz c\mf c2\spp c\ff }'''

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(string)
    assert format(target) == format(result) and target is not result
    for x in result:
        dynamics = abjad.inspect(x).get_indicators(abjad.Dynamic)
        assert len(dynamics) == 1
