# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker \
    import InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor \
    import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(
    InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'octave transposition mapping inventory'

    output_material_checker = staticmethod(lambda x: isinstance(x,
        pitchtools.OctaveTranspositionMappingInventory))

    output_material_editor = OctaveTranspositionMappingInventoryEditor

    output_material_maker = pitchtools.OctaveTranspositionMappingInventory

    output_material_module_import_statements = [
        'from abjad.tools import pitchtools',
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(
        octave_transposition_mapping_inventory, **kwargs):
        notes = []
        for octave_transposition_mapping in \
            octave_transposition_mapping_inventory:
            note = Note("c'4")
            notes.append(note)
        staff = stafftools.RhythmicStaff(notes)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.paper_block.top_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 6, 0)
        score.override.note_head.transparent = True
        score.override.bar_line.transparent = True
        score.override.clef.transparent = True
        score.override.span_bar.transparent = True
        score.override.staff_symbol.transparent = True
        score.override.stem.transparent = True
        score.override.time_signature.stencil = False
        score.set.proportional_notation_duration = \
            schemetools.SchemeMoment(1, 24)
        return illustration
