from experimental.tools.handlertools.ArticulationHandler import ArticulationHandler
from scf.editors.get_articulation_handler_editor import get_articulation_handler_editor
from scf.makers.MaterialPackageMaker import MaterialPackageMaker
from scf.wizards.ArticulationHandlerCreationWizard import ArticulationHandlerCreationWizard


class ArticulationHandlerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS ATTRIBUTES ###

    generic_output_name = 'articulation handler'
    output_material_checker = staticmethod(lambda x: isinstance(x, ArticulationHandler))
    output_material_editor = staticmethod(get_articulation_handler_editor)
    output_material_maker = ArticulationHandlerCreationWizard
    output_material_module_import_statements = [
        'from abjad.tools import durationtools',
        'from abjad.tools import pitchtools',
        'from experimental.tools import handlertools',
        ]
