# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoInventory(TypedList):
    r'''An ordered list of tempo indicators.

    ::

        >>> inventory = indicatortools.TempoInventory([
        ...     (Duration(1, 8), 72, 'Andante'),
        ...     (Duration(1, 8), 84, 'Allegro'),
        ...     ])

    ::

        >>> for tempo in inventory:
        ...     tempo
        ...
        Tempo(reference_duration=Duration(1, 8), units_per_minute=72, textual_indication='Andante')
        Tempo(reference_duration=Duration(1, 8), units_per_minute=84, textual_indication='Allegro')

    Tempo inventories implement list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    # TODO: put testable code in doctest
    def __illustrate__(self):
        r'''Illustrates tempo inventory.

        ::

            >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import lilypondfiletools
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import override
        staff = scoretools.Staff()
        score = scoretools.Score([staff])
        time_signature = indicatortools.TimeSignature((2, 4))
        attach(time_signature, staff)
        # the zero note avoids a lilypond spacing problem:
        # score-initial tempo indications slip to the left
        zero_note = scoretools.Note("c'2")
        staff.append(zero_note)
        command = indicatortools.LilyPondCommand('break')
        attach(command, zero_note)
        for tempo in self.items:
            note = scoretools.Note("c'2")
            attach(tempo, note)
            staff.append(note)
            command = indicatortools.LilyPondCommand('break')
            attach(command, note)
        override(score).bar_line.transparent = True
        override(score).bar_number.stencil = False
        override(score).clef.stencil = False
        override(score).note_head.no_ledgers = True
        override(score).note_head.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.items.remove(lilypond_file['paper'])
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(expr):
            if expr is None:
                tempo = indicatortools.Tempo()
            elif isinstance(expr, tuple):
                tempo = indicatortools.Tempo(*expr)
            elif isinstance(expr, indicatortools.Tempo):
                tempo = copy.copy(expr)
            else:
                raise TypeError(repr(expr))
            return tempo
        from abjad.tools import indicatortools
        return coerce_
