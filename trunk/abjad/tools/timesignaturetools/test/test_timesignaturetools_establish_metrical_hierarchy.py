from abjad import *


def test_timesignaturetools_establish_metrical_hierarchy_01():
    source = p('abj: | 4/4 8 2. 8 |')
    target = p('abj: | 4/4 8 4. ~ 4. 8 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source)
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert source.lilypond_format == target.lilypond_format


def test_timesignaturetools_establish_metrical_hierarchy_02():
    '''Establishes metrical hierarchy when first component's score offset greater than zero.
    '''
    source = p('abj: | 2/4 4 4 ~ || 4/4 8 2. 8 ~ || 2/4 4 4 |')
    target = p('abj: | 2/4 4 4 ~ || 4/4 8 4. ~ 4. 8 ~ || 2/4 4 4 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source[1])
    timesignaturetools.establish_metrical_hierarchy(source[1][:], metrical_hierarchy)
    assert source.lilypond_format == target.lilypond_format


def test_timesignaturetools_establish_metrical_hierarchy_03():
    '''Descends into tuplets.'''
    source = p('abj: | 2/4 2 ~ || 5/4 8 ~ 8 ~ 2/3 { 4 ~ 4 4 ~ } 4 ~ 4 ~ || 2/4 2 |') 
    target = p('abj: | 2/4 2 ~ || 5/4 4 ~ 2/3 { 2 4 ~ } 2 ~ || 2/4 2 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source[1])
    timesignaturetools.establish_metrical_hierarchy(source[1][:], metrical_hierarchy)
    assert source.lilypond_format == target.lilypond_format


def test_timesignaturetools_establish_metrical_hierarchy_04():
    source = p('abj: | 4/4 8. 4.. 4. |')
    target = p('abj: | 4/4 8. 16 ~ 4 ~ 8 4. |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy(source)
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert source.lilypond_format == target.lilypond_format


def test_timesignaturetools_establish_metrical_hierarchy_05():
    metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
    for rhythm_number in range(8):
        notes = timesignaturetools.make_gridded_test_rhythm(4, rhythm_number, denominator=4)
        measure = Measure((4, 4), notes)
        timesignaturetools.establish_metrical_hierarchy(measure[:], metrical_hierarchy)


def test_timesignaturetools_establish_metrical_hierarchy_06():
    source = p('abj: | 4/4 8 4. 2 |')
    target = p('abj: | 4/4 8 4. 2 |')
    metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
    timesignaturetools.establish_metrical_hierarchy(source[:], metrical_hierarchy)
    assert source.lilypond_format == target.lilypond_format

