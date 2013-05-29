from abjad import *
#from abjad.tools import pitchtools
#from make_illustration_from_output_material import make_illustration_from_output_material
from experimental.tools.scoremanagertools.materialpackagemakers.InventoryMaterialPackageMaker import \
    InventoryMaterialPackageMaker
from experimental.tools.scoremanagertools.editors.PitchRangeInventoryEditor import PitchRangeInventoryEditor


class PitchRangeInventoryMaterialPackageMaker(InventoryMaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'pitch range inventory'
    #illustration_maker = staticmethod(make_illustration_from_output_material)
    output_material_checker = staticmethod(lambda x: isinstance(x, pitchtools.PitchRangeInventory))
    output_material_editor = PitchRangeInventoryEditor
    output_material_maker = pitchtools.PitchRangeInventory
    output_material_module_import_statements = ['from abjad.tools import pitchtools' ]

    ### PUBLIC METHODS ###

    @staticmethod
    #def make_illustration_from_output_material(pitch_range_inventory, **kwargs):
    def illustration_builder(pitch_range_inventory, **kwargs):

        chords = []
        for pitch_range in pitch_range_inventory:
            chord = Chord((pitch_range.start_pitch, pitch_range.stop_pitch), Duration(1))
            if pitch_range.pitch_range_name_markup:
                markuptools.Markup(pitch_range.pitch_range_name_markup)(chord)
            chords.append(chord)

        score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(chords)
        illustration = lilypondfiletools.make_basic_lilypond_file(score)

        rests = resttools.iterate_rests_in_expr(score)
        skiptools.replace_leaves_in_expr_with_skips(list(rests))
        score.override.time_signature.stencil = False
        score.override.bar_line.transparent = True
        score.override.span_bar.transparent = True
        score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 4)

        return illustration
