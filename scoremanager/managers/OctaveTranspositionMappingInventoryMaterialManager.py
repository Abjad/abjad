# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager
from scoremanager.editors.OctaveTranspositionMappingInventoryEditor \
    import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    _output_material_checker = staticmethod(lambda x: isinstance(x,
        pitchtools.OctaveTranspositionMappingInventory))

    _output_material_editor = OctaveTranspositionMappingInventoryEditor

    _output_material_maker = pitchtools.OctaveTranspositionMappingInventory

    _output_material_module_import_statements = [
        'from abjad import *',
        ]

    generic_output_name = 'octave transposition mapping inventory'

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        superclass = super(
            OctaveTranspositionMappingInventoryMaterialManager, 
            self,
            )
        superclass.__init__(filesystem_path=filesystem_path, session=session)

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(octave_transposition_mapping_inventory, **kwargs):
        notes = []
        for mapping in octave_transposition_mapping_inventory:
            note = Note("c'4")
            notes.append(note)
        staff = scoretools.Staff(notes)
        staff.context_name = 'RhythmicStaff'
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        vector = layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.top_system_spacing = vector
        override(score).note_head.transparent = True
        override(score).bar_line.transparent = True
        override(score).clef.transparent = True
        override(score).span_bar.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        moment = schemetools.SchemeMoment(1, 24)
        set_(score).proportional_notation_duration = moment
        return illustration
