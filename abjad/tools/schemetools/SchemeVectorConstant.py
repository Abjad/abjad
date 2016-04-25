# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.schemetools.Scheme import Scheme


class SchemeVectorConstant(Scheme):
    '''Abjad model of Scheme vector constant.

    ..  container:: example

        **Example 1.** Scheme vector constant of boolean values:

        ::

            >>> scheme = schemetools.SchemeVectorConstant(True, True, False)
            >>> scheme
            SchemeVectorConstant(True, True, False)
            >>> print(format(scheme))
            #'#(#t #t #f)

    Scheme vectors and Scheme vector constants differ in
    only their LilyPond input format.

    Scheme vector constants are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        Scheme.__init__(self, *args, quoting="'#")

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        if stringtools.is_string(self._value):
            positional_argument_values = (self._value,)
        else:
            positional_argument_values = self._value
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )
