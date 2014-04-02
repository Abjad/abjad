# -*- encoding: utf-8 -*-
from scoremanager.managers.MaterialManager import MaterialManager


class ArticulationHandlerMaterialManager(MaterialManager):
    r'''Articulation handler material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(ArticulationHandlerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'articulation handler'
        self._output_module_import_statements = [
            self._abjad_import_statement,
            'from experimental.tools import handlertools',
            ]

    ### PUBLIC METHODS ###

    @staticmethod
    def _check_output_material(material):
        from experimental.tools import handlertools
        return isinstance(x, handlertools.ArticulationHandler)

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
        wizard = wizards.ArticulationHandlerCreationWizard(
            session=self._session,
            target=target,
            )
        return wizard