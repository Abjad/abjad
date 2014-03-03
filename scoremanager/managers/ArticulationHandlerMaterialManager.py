# -*- encoding: utf-8 -*-
from experimental.tools.handlertools.ArticulationHandler \
    import ArticulationHandler
from scoremanager.managers.MaterialManager import MaterialManager
from scoremanager.wizards.ArticulationHandlerCreationWizard \
    import ArticulationHandlerCreationWizard


class ArticulationHandlerMaterialManager(MaterialManager):

    ### CLASS VARIABLES ###

    _output_material_checker = staticmethod(
        lambda x: isinstance(x, ArticulationHandler))

    _output_material_maker = ArticulationHandlerCreationWizard

    ### INITIALIZER ###

    def __init__(self, filesystem_path=None, session=None):
        superclass = super(ArticulationHandlerMaterialManager, self)
        superclass.__init__(filesystem_path=filesystem_path, session=session)
        self._generic_output_name = 'articulation handler'
        self._output_material_module_import_statements = [
            'from abjad import *',
            'from experimental.tools import handlertools',
            ]


    ### PUBLIC METHODS ###

    @staticmethod
    def _output_material_editor(target=None, session=None):
        from scoremanager import wizards
        if target:
            wizard = wizards.ArticulationHandlerCreationWizard()
            articulation_handler_editor = wizard._get_target_editor(
                target.__class__.__name__, target=target)
            return articulation_handler_editor
