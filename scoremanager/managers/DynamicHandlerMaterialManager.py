# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialManager import MaterialManager


class DynamicHandlerMaterialManager(MaterialManager):
    r'''Dynamic handler material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(DynamicHandlerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'dynamic handler'
        self._output_module_import_statements = [
            self._abjad_import_statement,
            'from experimental.tools import handlertools',
            ]

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(material):
        from experimental.tools import handlertools
        return isinstance(material, handlertools.DynamicHandler)

    def _get_output_material_editor(self, target=None):
        from scoremanager import iotools
        if target:
            editor = iotools.Editor(
                session=self._session,
                target=target,
                )
            return editor
        else:
            return True

    def _make_output_material(self, target=None):
        from scoremanager import wizards
        wizard = wizards.DynamicHandlerCreationWizard(
            session=self._session,
            target=target,
            )
        return wizard