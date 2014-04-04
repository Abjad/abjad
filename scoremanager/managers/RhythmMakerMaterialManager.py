# -*- encoding: utf-8 -*-
import os
from abjad import *
from scoremanager.managers.MaterialPackageManager import MaterialPackageManager


class RhythmMakerMaterialManager(MaterialPackageManager):
    r'''Rhythm-maker material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(RhythmMakerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(expr):
        return isinstance(expr, rhythmmakertools.RhythmMaker)

    def _get_output_material_editor(self, target=None):
        wizard = RhythmMakerCreationWizard()
        editor = wizard._get_target_editor(
            target.__class__.__name__, 
            target=target,
            )
        return editor

    def _make_output_material(self):
        from scoremanager import wizards
        return wizards.RhythmMakerCreationWizard