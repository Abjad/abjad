from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.constants import *


class BendAfter(AbjadValueObject):
    r'''Fall or doit.

    ..  container:: example

        A fall:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(-4)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4 - \bendAfter #'-4.0

    ..  container:: example

        A doit:

        >>> note = abjad.Note("c'4")
        >>> bend = abjad.BendAfter(2)
        >>> abjad.attach(bend, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4 - \bendAfter #'2.0

    ..  container:: example

        Initializes from other bend:

        >>> abjad.BendAfter(abjad.BendAfter(16))
        BendAfter(bend_amount=16.0)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bend_amount',
        )

    _format_slot = 'right'

    _time_orientation = Right

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

            >>> str(abjad.BendAfter())
            "- \\bendAfter #'-4.0"

        Returns string.
        '''
        return r"- \bendAfter #'{}".format(self.bend_amount)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self.bend_amount)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.articulations.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def bend_amount(self):
        r'''Gets bend amount of bend after.

        ..  container:: example

            Fall:

            >>> bend = abjad.BendAfter(-4)
            >>> bend.bend_amount
            -4.0

        ..  container:: example

            Doit:

            >>> bend = abjad.BendAfter(2)
            >>> bend.bend_amount
            2.0

        Returns float.
        '''
        return self._bend_amount
