from abjad.tools.schemetools.Scheme import Scheme


class SchemeVector(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme vector::

        abjad> schemetools.SchemeVector(True, True, False)
        SchemeVector((True, True, False))

    Scheme vectors and Scheme vector constants differ in only their LilyPond input format.

    Scheme vectors are immutable.
    '''

    def __new__(klass, *args):
        return Scheme.__new__(klass, *args, **{'quoting': "'"})
