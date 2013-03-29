from abjad.tools import pitchtools
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.InventoryMaterialPackageMaker import InventoryMaterialPackageMaker
from scf.editors.PitchRangeInventoryEditor import PitchRangeInventoryEditor


class PitchRangeInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'pitch range inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.PitchRangeInventory))
    output_material_editor = PitchRangeInventoryEditor
    output_material_maker = pitchtools.PitchRangeInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools' ]
