from abjad.tools import measuretools


def is_background_element_klass(expr):
    r'''.. versionadded:: 1.0

    True when `expr` is any of ``Segment``, ``Measure`` or ``Division``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> selectortools.is_background_element_klass(specificationtools.Segment)
        True

    Otherwise false::

        >>> selectortools.is_background_element_klass(Container)
        False

    Return boolean.
    '''
    from experimental import specificationtools

    return expr in (specificationtools.Segment, measuretools.Measure, specificationtools.Division)
