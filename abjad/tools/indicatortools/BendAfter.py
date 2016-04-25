# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BendAfter(AbjadValueObject):
    r'''A fall or doit.

    ..  container:: example

        **Example 1.** A fall:

        ::

            >>> note = Note("c'4")
            >>> bend = indicatortools.BendAfter(-4)
            >>> attach(bend, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 - \bendAfter #'-4.0

    ..  container:: example

        **Example 2.** A doit:

        ::

            >>> note = Note("c'4")
            >>> bend = indicatortools.BendAfter(2)
            >>> attach(bend, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 - \bendAfter #'2.0

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bend_amount',
        '_default_scope',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, bend_amount=-4):
        if isinstance(bend_amount, type(self)):
            bend_amount = bend_amount.bend_amount
        bend_amount = float(bend_amount)
        self._bend_amount = bend_amount
        self._default_scope = None

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of bend after.

        ..  container:: example

            ::

                >>> str(indicatortools.BendAfter())
                "- \\bendAfter #'-4.0"

        Returns string.
        '''
        return r"- \bendAfter #'{}".format(self.bend_amount)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

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
        r'''Gets bend amount of bend after.

        ..  container:: example

            **Example 1.** Fall:

            ::

                >>> bend = indicatortools.BendAfter(-4)
                >>> bend.bend_amount
                -4.0

        ..  container:: example

            **Example 2.** Doit:

            ::

                >>> bend = indicatortools.BendAfter(2)
                >>> bend.bend_amount
                2.0 

        Returns float.
        '''
        return self._bend_amount

    @property
    def default_scope(self):
        r'''Gets default scope of bend after.

        ..  container:: example

            >>> bend = indicatortools.BendAfter(-4)
            >>> bend.default_scope is None
            True

        Returns none.
        '''
        return self._default_scope
