# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker \
    import InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.TempoMarkInventoryEditor \
    import TempoMarkInventoryEditor


class TempoMarkInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'tempo mark inventory'

    output_material_checker = staticmethod(
        lambda x: isinstance(x, marktools.TempoMarkInventory))

    output_material_editor = TempoMarkInventoryEditor

    output_material_maker = marktools.TempoMarkInventory

    output_material_module_import_statements = [
        'from abjad.tools import marktools',
        'from abjad.tools import durationtools',
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(tempo_mark_inventory, **kwargs):
        notes = []
        for tempo_mark in tempo_mark_inventory:
            note = Note("c'4")
            tempo_mark = marktools.TempoMark(
                tempo_mark, target_context=Staff)
            tempo_mark(note)
            notes.append(note)
        staff = scoretools.RhythmicStaff(notes)
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
        score.set.proportional_notation_duration = \
            schemetools.SchemeMoment(1, 24)
        return illustration
