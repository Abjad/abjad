# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class BendAfter(AbjadObject):
    r'''A fall or doit.

    ::

        >>> note = Note("c'4")
        >>> bend = indicatortools.BendAfter(-4)
        >>> attach(bend, note)
        >>> show(note) # doctest: +SKIP

    ..  doctest::

        >>> print format(note)
        c'4 - \bendAfter #'-4.0

    '''

    ### INITIALIZER ###

    def __init__(self, bend_amount=-4):
        self._format_slot = 'right'
        if isinstance(bend_amount, type(self)):
            bend_amount = bend_amount.bend_amount
        bend_amount = float(bend_amount)
        self._bend_amount = bend_amount

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies bend after.

        Returns new bend after.
        '''
        new = type(self)(self.bend_amount)
        new.format_slot = self.format_slot
        return new

    def __eq__(self, expr):
        r'''Is true when `expr` is a bend after with bend amount equal to bend
        after. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.bend_amount == expr.bend_amount:
                return True
        return False

    def __str__(self):
        r'''String representation of bend after.

        Returns string.
        '''
        return r"- \bendAfter #'{}".format(self.bend_amount)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self.bend_amount)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def bend_amount(self):
        r'''Amount of bend after.

        ::

            >>> bend.bend_amount
            -4.0

        Returns float.
        '''
        return self._bend_amount
