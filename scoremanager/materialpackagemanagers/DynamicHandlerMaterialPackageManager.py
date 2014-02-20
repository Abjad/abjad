# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager
from scoremanager.wizards.DynamicHandlerCreationWizard \
    import DynamicHandlerCreationWizard


class DynamicHandlerMaterialPackageManager(MaterialPackageManager):

    ### CLASS VARIABLES ###

    generic_output_name = 'dynamic handler'

    output_material_maker = DynamicHandlerCreationWizard

    output_material_module_import_statements = [
        'from abjad import *',
        'from experimental.tools import handlertools',
        ]

    ### STATIC METHODS ###

    @staticmethod
    def output_material_checker(expr):
        from experimental.tools import handlertools
        return isinstance(expr, handlertools.DynamicHandler)

    @staticmethod
    def output_material_editor(target=None, session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.DynamicHandlerCreationWizard()
            dynamic_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, 
                target=target,
                )
            return dynamic_handler_editor
