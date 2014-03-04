# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class TimeSignatureInventory(TypedList):
    '''An ordered list of time signatures.

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

    Time signature inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

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
    def _item_callable(self):
        from abjad.tools import indicatortools
        return indicatortools.TimeSignature

    @property
    def _one_line_menu_summary(self):
        return ', '.join([time_signature.pair for time_signature in self])
