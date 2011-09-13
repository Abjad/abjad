from abjad import *
from abjad.tools.marktools import Annotation


def test_Annotation___repr___01():
    '''Repr of unattached annotation is evaluable.
    '''

    annotation_1 = marktools.Annotation('foo')
    annotation_2 = eval(repr(annotation_1))

    assert isinstance(annotation_1, marktools.Annotation)
    assert isinstance(annotation_2, marktools.Annotation)
    assert annotation_1 == annotation_2
