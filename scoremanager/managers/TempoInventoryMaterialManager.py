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
        self._generic_output_name = 'tempo inventory'
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(tempo_inventory, **kwargs):
        r'''Illustrates tempo inventory.

        Returns LilyPond file.
        '''
        notes = []
        for tempo in tempo_inventory:
            note = Note("c'4")
            tempo = indicatortools.Tempo(tempo, scope=Staff)
            tempo(note)
            notes.append(note)
        staff = scoretools.Staff(notes)
        staff.context_name = 'RhythmicStaff'
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        vector = layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.top_system_spacing = vector
        override(score).note_head.transparent = True
        override(score).bar_line.transparent = True
        override(score).clef.transparent = True
        override(score).span_bar.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        moment = schemetools.SchemeMoment(1, 24)
        set_(score).proportional_notation_duration = moment
        return illustration

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

    def _make_output_material(self):
        return indicatortools.TempoInventory