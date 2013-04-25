import os
from abjad.tools.configurationtools.Configuration import Configuration
from abjad.tools.configurationtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(Configuration):
    '''Score manager configuration.

    The score manager tools output directory is created
    if it does not already exist by referencing the
    `score_manager_tools_output_directory` key in the configuration.
    '''

    ### CLASS ATTRIBUTES ###
    
    abjad_configuration = AbjadConfiguration()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.SCORE_MANAGER_TRANSCRIPTS_DIRECTORY_PATH):
            os.makedirs(self.SCORE_MANAGER_TRANSCRIPTS_DIRECTORY_PATH)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Score manager tools configuration file created on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            'score_manager_sketches_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager to store sketches.',
                    'Defaults to $HOME/.score_manager/sketches/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.SCORE_MANAGER_CONFIGURATION_DIRECTORY, 'sketches'))
            },
            'score_manager_transcripts_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager transcripts written.',
                    'Defaults to $HOME/.score_manager/transcripts/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.SCORE_MANAGER_CONFIGURATION_DIRECTORY, 'transcripts'))
            },
            'scores_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores. No default provided.'
                ],
                'spec': 'string()'
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
        return os.path.join(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'boilerplate')

    @property
    def editors_package_importable_name(self):
        return self.dot_join(['scoremanagertools', 'editors'])

    @property
    def editors_package_path(self):
        return os.path.join(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'editors')

    @property
    def makers_directory_name(self):
        return os.path.join(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'makers')

    @property
    def makers_package_importable_name(self):
        return self.dot_join([self.score_manager_tools_package_importable_name, 'makers'])

    @property
    def score_external_chunks_package_importable_name(self):
        return os.path.basename(self.SCORE_MANAGER_SKETCHES_DIRECTORY_PATH)

    @property
    def SCORE_MANAGER_SKETCHES_DIRECTORY_PATH(self):
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_external_chunks_package_path(self):
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_external_materials_package_importable_name(self):
        return os.path.basename(os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY'))

    @property
    def score_external_materials_package_path(self):
        return os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY')

    @property
    def score_external_package_importable_names(self):
        return (
            self.score_external_chunks_package_importable_name,
            self.score_external_materials_package_importable_name,
            self.score_external_specifiers_package_importable_name,
            )

    @property
    def score_external_package_paths(self):
        return (
            self.score_external_chunks_package_path,
            self.score_external_materials_package_path,
            self.score_external_specifiers_package_path,
            )

    @property
    def score_external_specifiers_package_importable_name(self):
        return os.path.basename(os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY'))

    @property
    def score_external_specifiers_package_path(self):
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
    def score_manager_tools_fully_qualified_package_name(self):
        return 'experimental.tools.scoremanagertools'

    @property
    def score_manager_tools_package_importable_name(self):
        return os.path.basename(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH)

    @property
    def SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH(self):
        return os.path.join(
            self.abjad_configuration.ABJAD_EXPERIMENTAL_DIRECTORY_PATH, 
            'tools', 
            'scoremanagertools')
        
    @property
    def SCORE_MANAGER_TRANSCRIPTS_DIRECTORY_PATH(self):
        return self._settings['score_manager_transcripts_directory_path']

    @property
    def SCORE_MANAGER_CONFIGURATION_DIRECTORY(self):
        return os.path.join(self.HOME_DIRECTORY_PATH, '.score_manager')

    @property
    def SCORES_DIRECTORY_PATH(self):
        return os.path.normpath(self._settings['scores_directory_path'])

    @property
    def specifier_classes_package_importable_name(self):
        return self.dot_join(['scoremanagertools', 'specifiers'])

    @property
    def specifier_classes_package_path(self):
        #return os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'specifiers')
        return os.path.join(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'specifiers')

    @property
    def stylesheets_directory_name(self):
        return os.path.join(self.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'stylesheets')

    @property
    def stylesheets_package_importable_name(self):
        return self.dot_join([self.score_manager_tools_package_importable_name, 'stylesheets'])

    @property
    def user_makers_directory_name(self):
        return os.environ.get('USER_SPECIFIC_SCORE_MANAGER_MAKERS_DIRECTORY')

    @property
    def user_makers_package_importable_name(self):
        return os.environ.get('USER_SPECIFIC_SCORE_MANAGER_MAKERS_IMPORTABLE_NAME')

    ### PUBLIC METHODS ###

    def dot_join(self, expr):
        return '.'.join(expr)
