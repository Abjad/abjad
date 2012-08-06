from abjad.tools import measuretools


def is_background_element_klass(expr):
    r'''.. versionadded:: 1.0

    True when `expr` is any of ``Segment``, ``Measure`` or ``Division``::

        >>> from experimental import *

    ::

        >>> helpertools.is_background_element_klass(segmenttools.Segment)
        True

    Otherwise false::

        >>> helpertools.is_background_element_klass(Container)
        False

    Return boolean.
    '''
    from experimental import divisiontools
    from experimental import segmenttools

    return expr in (segmenttools.Segment, measuretools.Measure, divisiontools.Division)
