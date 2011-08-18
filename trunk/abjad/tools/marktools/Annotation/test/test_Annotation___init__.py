from abjad import *


def test_Annotation___init___01():
    '''Initialize annotation with dictionary.
    '''

    annotation = marktools.Annotation('special dictionary', {})

    assert isinstance(annotation, marktools.Annotation)

