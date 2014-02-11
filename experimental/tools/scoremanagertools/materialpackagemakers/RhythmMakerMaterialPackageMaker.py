# -*- encoding: utf-8 -*-
import os
from abjad import *
from experimental.tools.scoremanagertools.materialpackagemakers.MaterialPackageMaker \
    import MaterialPackageMaker
from experimental.tools.scoremanagertools.wizards.RhythmMakerCreationWizard \
    import RhythmMakerCreationWizard


class RhythmMakerMaterialPackageMaker(MaterialPackageMaker):

    ### CLASS VARIABLES ###

    generic_output_name = 'time-menu_entry maker'


    output_material_maker = RhythmMakerCreationWizard

    output_material_module_import_statements = [
        'from abjad.tools import rhythmmakertools',
        ]

    ### STATIC METHODS ###

    @staticmethod
    def output_material_checker(expr):
        return isinstance(expr, rhythmmakertools.RhythmMaker)

    @staticmethod
    def output_material_editor(target=None, session=None):
        if target:
            wizard = RhythmMakerCreationWizard()
            rhythm_maker_editor = wizard.get_handler_editor(
                target.__class__.__name__, target=target)
            return rhythm_maker_editor

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
        measures = scoretools.make_spacer_skip_measures(
            meter_tokens)
        staff = scoretools.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        mutate(staff).replace_measure_contents(music)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        score_manager_configuration = \
            scoremanagertools.scoremanager.ScoreManagerConfiguration()
        directory_path = \
            score_manager_configuration.score_manager_tools_directory_path
        stylesheet_file_path = os.path.join(
            directory_path, 'stylesheets', 'rhythm-letter-16.ily')
        illustration.file_initial_user_includes.append(stylesheet_file_path)
        score.add_final_bar_line()
        if 'title' in kwargs:
            illustration.header_block.title = \
                markuptools.Markup(kwargs.get('title'))
        if 'subtitle' in kwargs:
            illustration.header_block.subtitle = \
                markuptools.Markup(kwargs.get('subtitle'))
        return illustration
