# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialManager import MaterialManager


class ArticulationHandlerMaterialManager(MaterialManager):

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ArticulationHandlerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'articulation handler'
        self._output_material_module_import_statements = [
            'from abjad import *',
            'from experimental.tools import handlertools',
            ]

    ### PUBLIC METHODS ###

    @staticmethod
    def _check_output_material(material):
        from experimental.tools import handlertools
        return isinstance(x, handlertools.ArticulationHandler)

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.ArticulationHandlerCreationWizard()
            articulation_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, 
                target=target,
                )
            return articulation_handler_editor
        else:
            return True

    @staticmethod
    def _make_output_material(target=None, session=None):
        from scoremanager import wizards
        #return wizards.ArticulationHandlerCreationWizard
        wizard = wizards.ArticulationHandlerCreationWizard(
            session=session,
            target=target,
            )
        return wizard
