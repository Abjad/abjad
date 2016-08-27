# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools import systemtools
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = self._value
        if stringtools.is_string(self._value):
            values = [self._value]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )
