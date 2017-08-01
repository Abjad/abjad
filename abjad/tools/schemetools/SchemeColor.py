# -*- coding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeColor(Scheme):
    r'''Abjad model of Scheme color.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> abjad.SchemeColor('ForestGreen')
            SchemeColor('ForestGreen')


    ..  container:: example

        ::

            >>> note = abjad.Note("c'4")
            >>> scheme_color = abjad.SchemeColor('ForestGreen')
            >>> abjad.override(note).note_head.color = scheme_color
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            \once \override NoteHead.color = #(x11-color 'ForestGreen)
            c'4

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        string = "(x11-color '{})"
        string = string.format(self._value)
        return string
