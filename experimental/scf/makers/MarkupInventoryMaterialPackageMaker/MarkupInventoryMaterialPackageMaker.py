from abjad.tools import markuptools
from make_illustration_from_output_material import make_illustration_from_output_material
from scf.makers.InventoryMaterialPackageMaker import InventoryMaterialPackageMaker
from scf.editors.MarkupInventoryEditor import MarkupInventoryEditor


class MarkupInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'markup inventory'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, markuptools.MarkupInventory))
    output_material_editor = MarkupInventoryEditor
    output_material_maker = markuptools.MarkupInventory
    output_material_module_import_statements = ['from abjad.tools import markuptools']
