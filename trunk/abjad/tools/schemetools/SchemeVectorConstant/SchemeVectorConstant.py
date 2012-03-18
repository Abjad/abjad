from abjad.tools.schemetools.Scheme import Scheme


class SchemeVectorConstant(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme vector constant::

        abjad> schemetools.SchemeVectorConstant(True, True, False)
        SchemeVectorConstant((True, True, False))

    Scheme vectors and Scheme vector constants differ in only their LilyPond input format.

    Scheme vector constants are immutable.
    '''

    __slots__ = ()

    def __init__(self, *args):
        Scheme.__init__(self, *args, **{'quoting': "'#"})
