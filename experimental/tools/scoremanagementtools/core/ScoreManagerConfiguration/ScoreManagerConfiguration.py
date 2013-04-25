import os
from abjad.tools.configurationtools.Configuration import Configuration


class ScoreManagerConfiguration(Configuration):
    '''Score management tools configuration.

    The score management tools output directory is created
    if it does not already exist by referencing the
    `score_management_tools_output_directory` key in the configuration.
    '''

    ### CLASS ATTRIBUTES ###

    score_management_tools_package_importable_name = \
        os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.SCORE_MANAGER_TRANSCRIPTS_DIRECTORY):
            os.mkdirs(self.SCORE_MANAGER_TRANSCRIPTS_DIRECTORY)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Score management tools configuration file created on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            'score_manager_transcripts_directory': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager transcripts written.',
                    'Defaults to $HOME/.score_manager/transcripts/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.SCORE_MANAGER_CONFIGURATION_DIRECTORY, 'transcripts'))
            },
        }
        return options

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def CONFIGURATION_DIRECTORY_PATH(self):
        return self.SCORE_MANAGER_CONFIGURATION_DIRECTORY

    @property
    def CONFIGURATION_FILE_NAME(self):
        return 'score_manager.cfg'

    @property
    def boilerplate_directory_name(self):
        return os.path.join(self.score_management_tools_package_path_name, 'boilerplate')

    @property
    def editors_package_importable_name(self):
        return self.dot_join(['scoremanagementtools', 'editors'])

    @property
    def editors_package_path_name(self):
        return os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'editors')

    @property
    def makers_directory_name(self):
        return os.path.join(self.score_management_tools_package_path_name, 'makers')

    @property
    def makers_package_importable_name(self):
        return self.dot_join([self.score_management_tools_package_importable_name, 'makers'])

    @property
    def score_external_chunks_package_importable_name(self):
        return os.path.basename(os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY'))

    @property
    def score_external_chunks_package_path_name(self):
        return os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY')

    @property
    def score_external_materials_package_importable_name(self):
        return os.path.basename(os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY'))

    @property
    def score_external_materials_package_path_name(self):
        return os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY')

    @property
    def score_external_package_importable_names(self):
        return (
            self.score_external_chunks_package_importable_name,
            self.score_external_materials_package_importable_name,
            self.score_external_specifiers_package_importable_name,
            )

    @property
    def score_external_package_path_names(self):
        return (
            self.score_external_chunks_package_path_name,
            self.score_external_materials_package_path_name,
            self.score_external_specifiers_package_path_name,
            )

    @property
    def score_external_specifiers_package_importable_name(self):
        return os.path.basename(os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY'))

    @property
    def score_external_specifiers_package_path_name(self):
        return os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY')

    @property
    def score_internal_chunks_package_importable_name_infix(self):
        return 'mus.chunks'

    @property
    def score_internal_materials_package_importable_name_infix(self):
        return 'mus.materials'

    @property
    def score_internal_specifiers_package_importable_name_infix(self):
        return 'mus.specifiers'

    @property
    def score_management_tools_fully_qualified_package_name(self):
        return 'experimental.tools.scoremanagementtools'

    @property
    def SCORE_MANAGER_TRANSCRIPTS_DIRECTORY(self):
        return self._settings['score_manager_transcripts_directory']

    @property
    def SCORE_MANAGER_CONFIGURATION_DIRECTORY(self):
        return os.path.join(self.HOME_DIRECTORY_PATH, '.score_manager')

#    @property
#    def score_management_tools_package_importable_name(self):
#        return os.path.basename(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'))

    @property
    def score_management_tools_package_path_name(self):
        return os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')

    @property
    def scores_directory_name(self):
        return os.environ.get('SCORES')

    @property
    def specifier_classes_package_importable_name(self):
        return self.dot_join(['scoremanagementtools', 'specifiers'])

    @property
    def specifier_classes_package_path_name(self):
        return os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'specifiers')

    @property
    def stylesheets_directory_name(self):
        return os.path.join(self.score_management_tools_package_path_name, 'stylesheets')

    @property
    def stylesheets_package_importable_name(self):
        return self.dot_join([self.score_management_tools_package_importable_name, 'stylesheets'])

    @property
    def user_makers_directory_name(self):
        return os.environ.get('USER_SPECIFIC_SCORE_MANAGER_MAKERS_DIRECTORY')

    @property
    def user_makers_package_importable_name(self):
        return os.environ.get('USER_SPECIFIC_SCORE_MANAGER_MAKERS_IMPORTABLE_NAME')

    ### PUBLIC METHODS ###

    def dot_join(self, expr):
        return '.'.join(expr)
