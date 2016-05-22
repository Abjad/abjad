# -*- coding: utf-8 -*-
import copy
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override
from abjad.tools.datastructuretools.TypedList import TypedList


class ClefInventory(TypedList):
    r'''An ordered list of clefs.

    ::

        >>> inventory = indicatortools.ClefInventory(['treble', 'bass'])

    ::

        >>> inventory
        ClefInventory([Clef(name='treble'), Clef(name='bass')])

    ::

        >>> 'treble' in inventory
        True

    ::

        >>> Clef('treble') in inventory
        True

    ::

        >>> 'alto' in inventory
        False

    ::

        >>> show(inventory) # doctest: +SKIP

    Clef inventories implement the list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates clef inventory.

        ::

            >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import scoretools
        staff = scoretools.Staff()
        for clef in self:
            rest = scoretools.Rest((1, 8))
            clef = copy.copy(clef)
            attach(clef, rest)
            staff.append(rest)
        override(staff).clef.full_size_change = True
        override(staff).rest.transparent = True
        override(staff).time_signature.stencil = False
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        return indicatortools.Clef

    @property
    def _one_line_menu_summary(self):
        return ', '.join([clef.name for clef in self])
