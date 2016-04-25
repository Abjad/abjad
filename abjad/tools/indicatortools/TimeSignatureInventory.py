# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TimeSignatureInventory(TypedList):
    r'''An ordered list of time signatures.

    ..  container:: example

        **Example 1.** Inventory with two time signatures:

        ::

            >>> inventory = indicatortools.TimeSignatureInventory([(5, 8), (4, 4)])

        ::

            >>> inventory
            TimeSignatureInventory([TimeSignature((5, 8)), TimeSignature((4, 4))])

        ::

            >>> (5, 8) in inventory
            True

        ::

            >>> TimeSignature((4, 4)) in inventory
            True

        ::

            >>> (3, 4) in inventory
            False

        ::

            >>> show(inventory) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self, format_specification=''):
        r'''Formats time signature inventory.

        ::

            >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        measures = scoretools.make_spacer_skip_measures(self)
        staff = scoretools.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        score = scoretools.Score([staff])
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        def coerce(expr):
            if isinstance(expr, tuple):
                return indicatortools.TimeSignature(expr)
            elif isinstance(expr, indicatortools.TimeSignature):
                return copy.copy(expr)
            else:
                message = 'must be pair or time signature: {!r}.'
                message = message.format(expr)
                raise Exception(message)
        return coerce

    @property
    def _one_line_menu_summary(self):
        return ', '.join([time_signature.pair for time_signature in self])
