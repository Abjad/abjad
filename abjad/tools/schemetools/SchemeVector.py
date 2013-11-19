# -*- encoding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeVector(Scheme):
    '''Abjad model of Scheme vector:

    ::

        >>> schemetools.SchemeVector(True, True, False)
        SchemeVector(True, True, False)

    Scheme vectors and Scheme vector constants differ in only 
    their LilyPond input format.

    Scheme vectors are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Scheme.__init__(self, *args, **{'quoting': "'"})
