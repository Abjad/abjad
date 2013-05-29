from abjad import *
#from abjad.tools import markuptools
#from make_illustration_from_output_material import make_illustration_from_output_material
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker import \
    InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.MarkupInventoryEditor import MarkupInventoryEditor


class MarkupInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'markup inventory'
    #illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, markuptools.MarkupInventory))
    output_material_editor = MarkupInventoryEditor
    output_material_maker = markuptools.MarkupInventory
    output_material_module_import_statements = ['from abjad.tools import markuptools']

    ### PUBLIC METHODS ###

    @staticmethod
    #def make_illustration_from_output_material(markup_inventory, **kwargs):
    def illustration_maker(markup_inventory, **kwargs):

        notes = []
        for markup in markup_inventory:
            note = Note("c'1")
            markup_copy = markuptools.Markup(markup)
            markup_copy(note)
            marktools.LilyPondCommandMark('break')(note)
            notes.append(note)

        staff = stafftools.RhythmicStaff(notes)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        illustration.layout_block.indent = 0
        illustration.layout_block.ragged_right = True
        illustration.paper_block.top_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 6, 0)
        illustration.paper_block.markup_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)

        score.override.note_head.transparent = True
        score.override.bar_line.transparent = True
        score.override.bar_number.transparent = True
        score.override.clef.transparent = True
        score.override.span_bar.transparent = True
        score.override.staff_symbol.transparent = True
        score.override.stem.transparent = True
        score.override.time_signature.stencil = False
        score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 8)

        if 'title' in kwargs:
            illustration.header_block.title = markuptools.Markup(kwargs.get('title'))
        if 'subtitle' in kwargs:
            illustration.header_block.subtitle = markuptools.Markup(kwargs.get('subtitle'))

        return illustration
