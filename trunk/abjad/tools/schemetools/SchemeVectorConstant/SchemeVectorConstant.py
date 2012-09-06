from abjad.tools.schemetools.Scheme import Scheme


class SchemeVectorConstant(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme vector constant::

        >>> schemetools.SchemeVectorConstant(True, True, False)
        SchemeVectorConstant((True, True, False))

    Scheme vectors and Scheme vector constants differ in only their LilyPond input format.

    Scheme vector constants are immutable.
    '''

    ### CLASS ATTRIBUTES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *args):
        Scheme.__init__(self, *args, **{'quoting': "'#"})
