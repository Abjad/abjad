# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager


class MarkupInventoryMaterialManager(MaterialPackageManager):
    r'''Markup inventory material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MarkupInventoryMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'markup inventory'
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### PUBLIC MEHTODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(material, markuptools.MarkupInventory)

    def _get_output_material_editor(self, target=None):
        from scoremanager import iotools
        target = target or markuptools.MarkupInventory()
        editor = iotools.ListEditor(
            session=self._session,
            target=target,
            )
        return editor

    def _make_output_material(self):
        return markuptools.MarkupInventory