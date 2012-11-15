from abjad import *
from abjad.tools.quantizationtools import *
import py


def test_QGrid___call___01():
    
    q_grid = QGrid()
    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert isinstance(result, list) and len(result) == 1
    assert result[0].lilypond_format == "c'4"

    annotation = marktools.get_annotation_attached_to_component(result[0])

    assert isinstance(annotation.value, tuple) and len(annotation.value) == 4
    assert annotation.value[0].attachments == ('A',)
    assert annotation.value[1].attachments == ('B',)
    assert annotation.value[2].attachments == ('C',)
    assert annotation.value[3].attachments == ('D',)


def test_QGrid___call___02():

    q_grid = QGrid()
    q_grid.subdivide_leaves([(0, (1, 1, 1))])
    q_grid.subdivide_leaves([(1, (1, 1))])
    q_grid.subdivide_leaves([(-2, (1, 1, 1))])
    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)
    q_grid.fit_q_events([a, b, c, d, e, f, g])
    result = q_grid((1, 4))

    assert isinstance(result, list) and len(result) == 1
    assert result[0].lilypond_format == "\\times 2/3 {\n\tc'8\n\tc'16\n\tc'16\n\t\\times 2/3 {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}\n}"

    annotation = marktools.get_annotations_attached_to_component(result[0].leaves[0])[0]
    assert isinstance(annotation.value, tuple) and len(annotation.value) == 2
    assert annotation.value[0].attachments == ('A',)
    assert annotation.value[1].attachments == ('B',)
    
    assert not marktools.get_annotations_attached_to_component(result[0].leaves[1])

    annotation = marktools.get_annotation_attached_to_component(result[0].leaves[2])
    assert isinstance(annotation.value, tuple) and len(annotation.value) == 3
    assert annotation.value[0].attachments == ('C',)
    assert annotation.value[1].attachments == ('D',)
    assert annotation.value[2].attachments == ('E',)
    
    assert not marktools.get_annotations_attached_to_component(result[0].leaves[3])
    assert not marktools.get_annotations_attached_to_component(result[0].leaves[4])
    assert not marktools.get_annotations_attached_to_component(result[0].leaves[5])


def test_QGrid___call___03():
    '''Non-binary works too.'''

    q_grid = QGrid()
    q_grid.subdivide_leaves([(0, (1, 1))])

    a = QEventProxy(SilentQEvent(0,        ['A']), 0)
    b = QEventProxy(SilentQEvent((1, 20),  ['B']), (1, 20))
    c = QEventProxy(SilentQEvent((9, 20),  ['C']), (9, 20))
    d = QEventProxy(SilentQEvent((1, 2),   ['D']), (1, 2))
    e = QEventProxy(SilentQEvent((11, 20), ['E']), (11, 20))
    f = QEventProxy(SilentQEvent((19, 20), ['F']), (19, 20))
    g = QEventProxy(SilentQEvent(1,        ['G']), 1)

    q_grid.fit_q_events([a, b, c, d, e, f, g])

    result = q_grid((1, 3))

    assert isinstance(result, list) and len(result) == 1
    assert result[0].lilypond_format == "\\times 2/3 {\n\tc'4\n\tc'4\n}"


