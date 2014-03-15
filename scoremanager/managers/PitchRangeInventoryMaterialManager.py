# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager


class PitchRangeInventoryMaterialManager(MaterialManager):
    r'''Pitch range inventory material manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(PitchRangeInventoryMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'pitch range inventory'
        self.output_material_module_import_statements = [
            'from abjad import *',
            ]

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(pitch_range_inventory, **kwargs):
        r'''Illustrates pitch range inventory.

        Returns LilyPond file.
        '''
        chords = []
        for pitch_range in pitch_range_inventory:
            pair = (pitch_range.start_pitch, pitch_range.stop_pitch)
            chord = Chord(pair, Duration(1))
            chords.append(chord)
        result = scoretools.make_piano_score_from_leaves(chords)
        score, treble_staff, bass_staff = result
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        rests = iterate(score).by_class(Rest)
        scoretools.replace_leaves_in_expr_with_skips(list(rests))
        override(score).time_signature.stencil = False
        override(score).bar_line.transparent = True
        override(score).span_bar.transparent = True
        moment = schemetools.SchemeMoment(1, 4)
        set_(score).proportional_notation_duration = moment
        return illustration

    ### PUBLIC METHODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(material, pitchtools.PitchRangeInventory)

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        from scoremanager import editors
        editor = editors.PitchRangeInventoryEditor(
            session=session,
            target=target,
            )
        return editor

    @staticmethod
    def _make_output_material():
        return pitchtools.PitchRangeInventory
