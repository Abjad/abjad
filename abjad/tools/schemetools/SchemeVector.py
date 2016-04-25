# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.schemetools.Scheme import Scheme


class SchemeVector(Scheme):
    '''Abjad model of Scheme vector.

    ..  container:: example

        **Example 1.** Scheme vector of boolean values:

        ::

            >>> scheme = schemetools.SchemeVector(True, True, False)
            >>> scheme
            SchemeVector(True, True, False)
            >>> print(format(scheme))
            #'(#t #t #f)

    ..  container:: example

        **Example 2.** Scheme vector of symbols:

        ::

            >>> scheme = schemetools.SchemeVector('foo', 'bar', 'blah')
            >>> scheme
            SchemeVector('foo', 'bar', 'blah')
            >>> print(format(scheme))
            #'(foo bar blah)

    Scheme vectors and Scheme vector constants differ in only
    their LilyPond input format.

    Scheme vectors are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *args):
        Scheme.__init__(self, *args, quoting="'")

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
