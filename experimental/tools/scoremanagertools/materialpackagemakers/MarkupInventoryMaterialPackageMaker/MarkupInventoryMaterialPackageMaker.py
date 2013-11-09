# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker \
    import InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.MarkupInventoryEditor \
    import MarkupInventoryEditor


class MarkupInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'markup inventory'

    output_material_checker = staticmethod(
        lambda x: isinstance(x, markuptools.MarkupInventory))

    output_material_editor = MarkupInventoryEditor

    output_material_maker = markuptools.MarkupInventory

    output_material_module_import_statements = [
        'from abjad.tools import markuptools',
        ]

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(markup_inventory, **kwargs):
        notes = []
        for markup in markup_inventory:
            note = Note("c'1")
            markup_copy = markuptools.Markup(markup)
            markup_copy(note)
            marktools.LilyPondCommand('break')(note)
            notes.append(note)
        staff = scoretools.RhythmicStaff(notes)
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
        contextualize(score).proportional_notation_duration = \
            schemetools.SchemeMoment(1, 8)
        if 'title' in kwargs:
            illustration.header_block.title = \
                markuptools.Markup(kwargs.get('title'))
        if 'subtitle' in kwargs:
            illustration.header_block.subtitle = \
                markuptools.Markup(kwargs.get('subtitle'))
        return illustration
