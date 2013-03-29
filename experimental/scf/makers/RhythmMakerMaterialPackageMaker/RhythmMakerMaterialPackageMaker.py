from make_illustration_from_output_material import make_illustration_from_output_material
from scf.editors.get_time_token_maker_editor import get_time_token_maker_editor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.wizards.RhythmMakerCreationWizard import RhythmMakerCreationWizard
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class RhythmMakerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'time-token maker'
    illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, RhythmMaker))
    output_material_editor = staticmethod(get_time_token_maker_editor)
    output_material_maker = RhythmMakerCreationWizard
    output_material_module_import_statements = ['from abjad.tools import rhythmmakertools']
