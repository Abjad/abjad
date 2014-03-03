# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialManager import MaterialManager
from scoremanager.wizards.DynamicHandlerCreationWizard \
    import DynamicHandlerCreationWizard


class DynamicHandlerMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    _output_material_maker = DynamicHandlerCreationWizard

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        superclass = super(DynamicHandlerMaterialManager, self)
        superclass.__init__(filesystem_path=filesystem_path, session=session)
        self._generic_output_name = 'dynamic handler'
        self._output_material_module_import_statements = [
            'from abjad import *',
            'from experimental.tools import handlertools',
            ]

    ### PRIVATE METHODS ###

    # TODO: name verb-first
    @staticmethod
    def _output_material_checker(expr):
        from experimental.tools import handlertools
        return isinstance(expr, handlertools.DynamicHandler)

    # TODO: name verb-first
    @staticmethod
    def _output_material_editor(target=None, session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.DynamicHandlerCreationWizard()
            dynamic_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, 
                target=target,
                )
            return dynamic_handler_editor
