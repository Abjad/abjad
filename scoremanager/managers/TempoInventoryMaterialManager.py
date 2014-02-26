# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager
from scoremanager.editors.TempoInventoryEditor import TempoInventoryEditor


class TempoInventoryMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    generic_output_name = 'tempo inventory'

    output_material_checker = staticmethod(
        lambda x: isinstance(x, indicatortools.TempoInventory))

    output_material_editor = TempoInventoryEditor

    output_material_maker = indicatortools.TempoInventory

    output_material_module_import_statements = [
        'from abjad import *',
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(tempo_inventory, **kwargs):
        notes = []
        for tempo in tempo_inventory:
            note = Note("c'4")
            tempo = indicatortools.Tempo(
                tempo, scope=Staff)
            tempo(note)
            notes.append(note)
        staff = scoretools.Staff(notes)
        staff.context_name = 'RhythmicStaff'
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.paper_block.top_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 6, 0)
        override(score).note_head.transparent = True
        override(score).bar_line.transparent = True
        override(score).clef.transparent = True
        override(score).span_bar.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        set_(score).proportional_notation_duration = \
            schemetools.SchemeMoment(1, 24)
        return illustration
