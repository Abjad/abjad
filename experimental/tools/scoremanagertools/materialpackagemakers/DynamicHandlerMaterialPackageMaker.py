# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker \
    import MaterialPackageMaker
from experimental.tools.scoremanagertools.wizards.DynamicHandlerCreationWizard \
    import DynamicHandlerCreationWizard


class DynamicHandlerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'dynamic handler'

    output_material_maker = DynamicHandlerCreationWizard

    output_material_module_import_statements = [
        'from abjad.tools import durationtools',
        'from experimental.tools import handlertools',
        ]

    ### STATIC METHODS ###

    @staticmethod
    def output_material_checker(expr):
        from experimental.tools import scoremanagertools
        return isinstance(expr, scoremanagertools.handlers.DynamicHandler)

    @staticmethod
    def output_material_editor(target=None, session=None):
        from experimental.tools import scoremanagertools
        if target:
            wizard = scoremanagertools.wizards.DynamicHandlerCreationWizard()
            # TODO: generalize get_handler_editor to get_target_editor?
            dynamic_handler_editor = wizard.get_handler_editor(
                target.__class__.__name__, target=target)
            return dynamic_handler_editor
