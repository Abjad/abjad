# -*- encoding: utf-8 -*-
from experimental.tools.handlertools.ArticulationHandler \
    import ArticulationHandler
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager
from scoremanager.wizards.ArticulationHandlerCreationWizard \
    import ArticulationHandlerCreationWizard


class ArticulationHandlerMaterialPackageManager(MaterialPackageManager):

    ### CLASS VARIABLES ###

    generic_output_name = 'articulation handler'

    output_material_checker = staticmethod(
        lambda x: isinstance(x, ArticulationHandler))

    @staticmethod
    def output_material_editor(target=None, _session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.ArticulationHandlerCreationWizard()
            articulation_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, target=target)
            return articulation_handler_editor

    output_material_maker = ArticulationHandlerCreationWizard

    output_material_module_import_statements = [
        'from abjad import *',
        'from experimental.tools import handlertools',
        ]
