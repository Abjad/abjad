# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialManager import MaterialManager


class DynamicHandlerMaterialManager(MaterialManager):
    r'''Dynamic handler material manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(DynamicHandlerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'dynamic handler'
        self.output_material_module_import_statements = [
            'from abjad import *',
            'from experimental.tools import handlertools',
            ]

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(material):
        from experimental.tools import handlertools
        return isinstance(material, handlertools.DynamicHandler)

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.DynamicHandlerCreationWizard()
            dynamic_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, 
                target=target,
                )
            return dynamic_handler_editor
        else:
            return True

    @staticmethod
    def _make_output_material(target=None, session=None):
        from scoremanager import wizards
        wizard = wizards.DynamicHandlerCreationWizard(
            session=session,
            target=target,
            )
        return wizard
