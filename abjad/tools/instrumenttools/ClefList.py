# -*- coding: utf-8 -*-
import copy
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import override
from abjad.tools.datastructuretools.TypedList import TypedList


class ClefList(TypedList):
    r'''An ordered list of clefs.

    ::

        >>> inventory = instrumenttools.ClefList(['treble', 'bass'])

    ::

        >>> inventory
        ClefList([Clef(name='treble'), Clef(name='bass')])

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
        import abjad
        staff = abjad.Staff()
        for clef in self:
            rest = abjad.Rest((1, 8))
            clef = copy.copy(clef)
            attach(clef, rest)
            staff.append(rest)
        override(staff).clef.full_size_change = True
        override(staff).rest.transparent = True
        override(staff).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(staff)
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        from abjad.tools import indicatortools
        return indicatortools.Clef
