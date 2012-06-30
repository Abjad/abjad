from abjad.tools import measuretools


def is_background_element_klass(expr):
    r'''.. versionadded:: 1.0

    True when `expr` is segment, measure or division class.

    False otherwise.

    Return boolean.
    '''
    from experimental import specificationtools

    return expr in (specificationtools.SegmentSpecification, 
        specificationtools.Division, measuretools.Measure)
