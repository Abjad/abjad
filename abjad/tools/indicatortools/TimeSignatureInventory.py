# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TimeSignatureInventory(TypedList):
    r'''Time signature list.

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

    __documentation_section__ = 'Collections'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self, format_specification=''):
        r'''Formats time signature inventory.

        ::

            >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        import abjad
        measures = abjad.scoretools.make_spacer_skip_measures(self)
        staff = abjad.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        score = abjad.Score([staff])
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        def coerce(argument):
            if isinstance(argument, tuple):
                return indicatortools.TimeSignature(argument)
            elif isinstance(argument, indicatortools.TimeSignature):
                return copy.copy(argument)
            else:
                message = 'must be pair or time signature: {!r}.'
                message = message.format(argument)
                raise Exception(message)
        return coerce
