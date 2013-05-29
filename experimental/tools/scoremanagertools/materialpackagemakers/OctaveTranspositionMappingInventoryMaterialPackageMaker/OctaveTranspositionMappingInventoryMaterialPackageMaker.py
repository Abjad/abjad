from abjad import *
#from abjad.tools import pitchtools
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker import \
    InventoryMaterialPackageMaker
#from make_illustration_from_output_material import make_illustration_from_output_material
from experimental.tools.scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor import \
    OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'octave transposition mapping inventory'
    #illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x,
        pitchtools.OctaveTranspositionMappingInventory))
    output_material_editor = OctaveTranspositionMappingInventoryEditor
    output_material_maker = pitchtools.OctaveTranspositionMappingInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools']

    ### PUBLIC METHODS ###

    @staticmethod
    #def make_illustration_from_output_material(octave_transposition_mapping_inventory, **kwargs):
    def illustration_builder(octave_transposition_mapping_inventory, **kwargs):

        notes = []
        for octave_transposition_mapping in octave_transposition_mapping_inventory:
            note = Note("c'4")
            #tempo_mark = contexttools.TempoMark(tempo_mark, target_context=Staff)
            #tempo_mark(note)
            notes.append(note)

        staff = stafftools.RhythmicStaff(notes)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.paper_block.top_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)

        score.override.note_head.transparent = True
        score.override.bar_line.transparent = True
        score.override.clef.transparent = True
        score.override.span_bar.transparent = True
        score.override.staff_symbol.transparent = True
        score.override.stem.transparent = True
        score.override.time_signature.stencil = False
        score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 24)

        return illustration
