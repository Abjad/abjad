# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList
from abjad.tools.pitchtools.PitchRange import PitchRange


class PitchRangeInventory(TypedList):
    r'''An ordered list of pitch ranges.

    ::

        >>> inventory = pitchtools.PitchRangeInventory([
        ...     '[C3, C6]', 
        ...     '[C4, C6]',
        ...     ])
        >>> inventory
        PitchRangeInventory([PitchRange('[C3, C6]'), PitchRange('[C4, C6]')])

    Pitch range inventories implement list interface and are mutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        r'''Illustrates pitch range inventory.

        ::

            >>> show(inventory) # doctest: +SKIP

        Returns LilyPond file.
        '''
        from abjad.tools import durationtools
        from abjad.tools import lilypondfiletools
        from abjad.tools import indicatortools
        from abjad.tools import markuptools
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        from abjad.tools import spannertools
        from abjad.tools.topleveltools import attach
        from abjad.tools.topleveltools import iterate
        from abjad.tools.topleveltools import override
        start_note_clefs = []
        stop_note_clefs = []
        for pitch_range in self.items:
            start_note_clef = pitchtools.suggest_clef_for_named_pitches(
                pitch_range.start_pitch)
            start_note_clefs.append(start_note_clef)
            stop_note_clef = pitchtools.suggest_clef_for_named_pitches(
                pitch_range.stop_pitch)
            stop_note_clefs.append(stop_note_clef)
        if start_note_clefs == stop_note_clefs:
            clef = start_note_clefs[0]
            staff = scoretools.Staff()
            attach(clef, staff)
            score = scoretools.Score([staff])
            for pitch_range in self.items:
                start_note = scoretools.Note(pitch_range.start_pitch, 1)
                stop_note = scoretools.Note(pitch_range.stop_pitch, 1)
                notes = [start_note, stop_note]
                glissando = spannertools.Glissando()
                staff.extend(notes)
                attach(glissando, notes)
        else:
            result = scoretools.make_empty_piano_score()
            score, treble_staff, bass_staff = result
            for pitch_range in self.items:
                start_note = scoretools.Note(pitch_range.start_pitch, 1)
                start_note_clef = pitchtools.suggest_clef_for_named_pitches(
                    pitch_range.start_pitch)
                stop_note = scoretools.Note(pitch_range.stop_pitch, 1)
                stop_note_clef = pitchtools.suggest_clef_for_named_pitches(
                    pitch_range.stop_pitch)
                notes = [start_note, stop_note]
                glissando = spannertools.Glissando()
                skips = 2 * scoretools.Skip(1)
                treble_clef = indicatortools.Clef('treble')
                bass_clef = indicatortools.Clef('bass')
                if start_note_clef == stop_note_clef == treble_clef:
                    treble_staff.extend(notes)
                    bass_staff.extend(skips)
                elif start_note_clef == stop_note_clef == bass_clef:
                    bass_staff.extend(notes)
                    treble_staff.extend(skips)
                else:
                    assert start_note_clef == bass_clef
                    assert stop_note_clef == treble_clef
                    bass_staff.extend(notes)
                    treble_staff.extend(skips)
                    staff_change = indicatortools.StaffChange(treble_staff)
                    attach(staff_change, stop_note)
                attach(glissando, notes)
        for leaf in iterate(score).by_class(scoretools.Leaf):
            multiplier = durationtools.Multiplier(1, 4)
            attach(multiplier, leaf)
        override(score).bar_line.stencil = False
        override(score).span_bar.stencil = False
        override(score).glissando.thickness = 2
        override(score).time_signature.stencil = False
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
        lilypond_file.items.remove(lilypond_file['layout'])
        lilypond_file.items.remove(lilypond_file['paper'])
        lilypond_file.header_block.tagline = markuptools.Markup('""')
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return PitchRange
