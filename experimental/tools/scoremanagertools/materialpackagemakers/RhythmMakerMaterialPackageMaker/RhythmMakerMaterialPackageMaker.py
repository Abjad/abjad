import os
from abjad import *
from experimental.tools.scoremanagertools.editors.get_rhythm_maker_editor import get_rhythm_maker_editor
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker import MaterialPackageMaker
from experimental.tools.scoremanagertools.wizards.RhythmMakerCreationWizard import RhythmMakerCreationWizard
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker


class RhythmMakerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'time-token maker'
    output_material_checker = staticmethod(lambda x: isinstance(x, RhythmMaker))
    output_material_editor = staticmethod(get_rhythm_maker_editor)
    output_material_maker = RhythmMakerCreationWizard
    output_material_module_import_statements = ['from abjad.tools import rhythmmakertools']

    ### PUBLIC METHODS ###

    @staticmethod
    def illustration_builder(output_material, **kwargs):
        meter_tokens = [
            (2, 8), (3, 8), (4, 8), (5, 8),
            (2, 16), (3, 16), (4, 16), (5, 16),
            (2, 4), (2, 4), (2, 4), (2, 4),
            ]
        music = output_material(meter_tokens)
        music = sequencetools.flatten_sequence(music)
        measures = measuretools.make_measures_with_full_measure_spacer_skips(meter_tokens)
        staff = stafftools.RhythmicStaff(measures)
        measuretools.replace_contents_of_measures_in_expr(staff, music)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
        directory_path = score_manager_configuration.score_manager_tools_directory_path
        stylesheet_file_path = os.path.join(directory_path, 'built_in_stylesheets', 'rhythm-letter-16.ly')
        illustration.file_initial_user_includes.append(stylesheet_file_path)
        scoretools.add_double_bar_to_end_of_score(score)
        if 'title' in kwargs:
            illustration.header_block.title = markuptools.Markup(kwargs.get('title'))
        if 'subtitle' in kwargs:
            illustration.header_block.subtitle = markuptools.Markup(kwargs.get('subtitle'))
        return illustration
