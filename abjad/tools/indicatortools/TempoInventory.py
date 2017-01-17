# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoInventory(TypedList):
    r'''Tempo list.

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

    __documentation_section__ = 'Collections'

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
        import abjad
        staff = abjad.Staff()
        score = abjad.Score([staff])
        time_signature = abjad.TimeSignature((2, 4))
        abjad.attach(time_signature, staff)
        # the zero note avoids a lilypond spacing problem:
        # score-initial tempo indications slip to the left
        zero_note = abjad.Note("c'2")
        staff.append(zero_note)
        command = abjad.LilyPondCommand('break')
        abjad.attach(command, zero_note)
        for tempo in self.items:
            note = abjad.Note("c'2")
            abjad.attach(tempo, note)
            staff.append(note)
            command = abjad.LilyPondCommand('break')
            abjad.attach(command, note)
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).clef.stencil = False
        abjad.override(score).note_head.no_ledgers = True
        abjad.override(score).note_head.transparent = True
        abjad.override(score).staff_symbol.transparent = True
        abjad.override(score).stem.transparent = True
        abjad.override(score).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.items.remove(lilypond_file['paper'])
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(argument):
            if argument is None:
                tempo = indicatortools.Tempo()
            elif isinstance(argument, tuple):
                tempo = indicatortools.Tempo(*argument)
            elif isinstance(argument, indicatortools.Tempo):
                tempo = copy.copy(argument)
            else:
                raise TypeError(repr(argument))
            return tempo
        from abjad.tools import indicatortools
        return coerce_
