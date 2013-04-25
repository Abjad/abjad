from abjad.tools import pitchtools
from experimental.tools.scoremanagertools.makers.InventoryMaterialPackageMaker import InventoryMaterialPackageMaker
from make_illustration_from_output_material import make_illustration_from_output_material
from experimental.tools.scoremanagertools.editors.OctaveTranspositionMappingInventoryEditor import OctaveTranspositionMappingInventoryEditor


class OctaveTranspositionMappingInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'octave transposition mapping inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x,
        pitchtools.OctaveTranspositionMappingInventory))
    output_material_editor = OctaveTranspositionMappingInventoryEditor
    output_material_maker = pitchtools.OctaveTranspositionMappingInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools']
