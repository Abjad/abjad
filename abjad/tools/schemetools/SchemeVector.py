# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.schemetools.Scheme import Scheme


class SchemeVector(Scheme):
    '''Abjad model of Scheme vector.

    ::

        >>> import abjad

    ..  container:: example

        Scheme vector of boolean values:

        ::

            >>> scheme = abjad.SchemeVector([True, True, False])
            >>> scheme
            SchemeVector(True, True, False)
            >>> print(format(scheme))
            #'(#t #t #f)

    ..  container:: example

        Scheme vector of symbols:

        ::

            >>> scheme = abjad.SchemeVector(['foo', 'bar', 'blah'])
            >>> scheme
            SchemeVector('foo', 'bar', 'blah')
            >>> print(format(scheme))
            #'(foo bar blah)

    Scheme vectors and Scheme vector constants differ in only their LilyPond
    input format.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, value=[]):
        Scheme.__init__(self, value, quoting="'")

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        values = self._value
        if datastructuretools.String.is_string(self._value):
            values = [self._value]
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=values,
            storage_format_kwargs_names=[],
            )
