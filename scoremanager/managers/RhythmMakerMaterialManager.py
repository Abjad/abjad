# -*- encoding: utf-8 -*-
import os
from abjad import *
from scoremanager.managers.MaterialManager import MaterialManager


class RhythmMakerMaterialManager(MaterialManager):
    r'''Rhythm-maker material manager.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        superclass = super(RhythmMakerMaterialManager, self)
        superclass.__init__(path=path, session=session)
        self._generic_output_name = 'rhythm-maker'
        self._output_module_import_statements = [
            self._abjad_import_statement,
            ]

    ### SPECIAL METHODS ###

    @staticmethod
    def __illustrate__(output_material, **kwargs):
        r'''Illustrates rhythm-maker.

        Returns LilyPond file.
        '''
        meter_tokens = [
            (2, 8), (3, 8), (4, 8), (5, 8),
            (2, 16), (3, 16), (4, 16), (5, 16),
            (2, 4), (2, 4), (2, 4), (2, 4),
            ]
        music = output_material(meter_tokens)
        music = sequencetools.flatten_sequence(music)
        measures = scoretools.make_spacer_skip_measures(meter_tokens)
        staff = scoretools.Staff(measures)
        staff.context_name = 'RhythmicStaff'
        mutate(staff).replace_measure_contents(music)
        score = Score([staff])
        illustration = lilypondfiletools.make_basic_lilypond_file(score)
        configuration = scoremanager.core.ScoreManagerConfiguration()
        path = configuration.score_manager_directory_path
        stylesheet_file_path = os.path.join(
            path, 
            'stylesheets', 
            'rhythm-letter-16.ily',
            )
        illustration.file_initial_user_includes.append(stylesheet_file_path)
        score.add_final_bar_line()
        if 'title' in kwargs:
            markup = markuptools.Markup(kwargs.get('title'))
            illustration.header_block.title = markup
        if 'subtitle' in kwargs:
            markup = markuptools.Markup(kwargs.get('subtitle'))
            illustration.header_block.subtitle = markup
        return illustration

    ### PRIVATE METHODS ###

    @staticmethod
    def _check_output_material(expr):
        return isinstance(expr, rhythmmakertools.RhythmMaker)

    def _get_output_material_editor(self, target=None):
        if target:
            wizard = RhythmMakerCreationWizard()
            rhythm_maker_editor = wizard._get_target_editor(
                target.__class__.__name__, 
                target=target,
                )
            return rhythm_maker_editor

    def _make_output_material(self):
        from scoremanager import wizards
        return wizards.RhythmMakerCreationWizard