# -*- encoding: utf-8 -*-
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager


class MarkupInventoryMaterialManager(MaterialManager):
    r'''Markup inventory material manager.
    '''

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(MarkupInventoryMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'markup inventory'
        self.output_material_module_import_statements = [
            'from abjad import *',
            ]

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(markup_inventory, **kwargs):
        r'''Illustrates markup inventory.

        Returns LilyPond file.
        '''
        notes = []
        for markup in markup_inventory:
            note = Note("c'1")
            markup_copy = markuptools.Markup(markup)
            markup_copy(note)
            indicatortools.LilyPondCommand('break')(note)
            notes.append(note)
        staff = scoretools.Staff(notes)
        staff.context_name = 'RhythmicStaff'
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.layout_block.indent = 0
        illustration.layout_block.ragged_right = True
        illustration.paper_block.top_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.system_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.markup_system_spacing = \
            layouttools.make_spacing_vector(0, 0, 12, 0)
        override(score).note_head.transparent = True
        override(score).bar_line.transparent = True
        override(score).bar_number.transparent = True
        override(score).clef.transparent = True
        override(score).span_bar.transparent = True
        override(score).staff_symbol.transparent = True
        override(score).stem.transparent = True
        override(score).time_signature.stencil = False
        set_(score).proportional_notation_duration = \
            schemetools.SchemeMoment(1, 8)
        if 'title' in kwargs:
            illustration.header_block.title = \
                markuptools.Markup(kwargs.get('title'))
        if 'subtitle' in kwargs:
            illustration.header_block.subtitle = \
                markuptools.Markup(kwargs.get('subtitle'))
        return illustration

    ### PUBLIC MEHTODS ###

    @staticmethod
    def _check_output_material(material):
        return isinstance(material, markuptools.MarkupInventory)

    @staticmethod
    def _get_output_material_editor(target=None, session=None):
        from scoremanager import editors
        editor = editors.MarkupInventoryEditor(
            session=session,
            target=target,
            )
        return editor

    @staticmethod
    def _make_output_material():
        return markuptools.MarkupInventory
