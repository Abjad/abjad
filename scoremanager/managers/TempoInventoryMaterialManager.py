# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager


class TempoInventoryMaterialManager(MaterialPackageManager):
    r'''Tempo inventory material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(TempoInventoryMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(x, indicatortools.TempoInventory)

    def _get_output_material_editor(self, target=None):
        from scoremanager import iotools
        target = target or indicatortools.TempoInventory()
        editor = iotools.ListEditor(
            session=self._session,
            target=target,
            )
        return editor

    def _has_output_material_editor(self):
        return True

    def _make_output_material(self):
        return indicatortools.TempoInventory