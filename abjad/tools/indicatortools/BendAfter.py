# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BendAfter(AbjadValueObject):
    r'''A fall or doit.

    ..  container:: example

        ::

            >>> note = Note("c'4")
            >>> bend = indicatortools.BendAfter(-4)
            >>> attach(bend, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 - \bendAfter #'-4.0

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bend_amount',
        )


    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, bend_amount=-4):
        if isinstance(bend_amount, type(self)):
            bend_amount = bend_amount.bend_amount
        bend_amount = float(bend_amount)
        self._bend_amount = bend_amount

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

            ::

                >>> bend = indicatortools.BendAfter()
                >>> bend.bend_amount
                -4.0

        Returns float.
        '''
        return self._bend_amount