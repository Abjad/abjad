from abjad.tools.schemetools.Scheme import Scheme


class SchemeVector(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme vector::

        >>> schemetools.SchemeVector(True, True, False)
        SchemeVector((True, True, False))

    Scheme vectors and Scheme vector constants differ in only their LilyPond input format.

    Scheme vectors are immutable.
    '''

    ### CLASS ATTRIBUTES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *args):
        Scheme.__init__(self, *args, **{'quoting': "'"})
