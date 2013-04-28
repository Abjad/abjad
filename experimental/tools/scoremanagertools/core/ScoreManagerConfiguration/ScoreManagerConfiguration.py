import os
from abjad.tools.configurationtools.Configuration import Configuration
from abjad.tools.configurationtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(Configuration):
    '''Score manager configuration.

    The score manager tools output directory is created
    if it does not already exist by referencing the
    `score_manager_tools_transcripts_directory` key in the configuration.
    '''

    ### CLASS ATTRIBUTES ###
    
    abjad_configuration = AbjadConfiguration()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.score_manager_transcripts_directory_path):
            os.makedirs(self.score_manager_transcripts_directory_path)

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
                    os.path.join(self.score_manager_configuration_directory, 'sketches'))
            },
            'score_manager_transcripts_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager transcripts written.',
                    'Defaults to $HOME/.score_manager/transcripts/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.score_manager_configuration_directory, 'transcripts'))
            },
            'scores_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores. No default provided.'
                ],
                'spec': "string(default='')"
            },
            'user_specific_score_manager_makers_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific makers.',
                    'Always set user_specific_score_manager_makers_directory_path',
                    'together with user_specific_score_manager_makers_package_path.',
                    'Defaults to none.'
                ],
                'spec': "string(default='')"
            },
            'user_specific_score_manager_makers_package_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific makers.',
                    'Always set user_specific_score_manager_makers_directory_path',
                    'together with user_specific_score_manager_makers_package_path.',
                    'Defaults to none.'
                ],
                'spec': "string(default='')"
            },
        }
        return options

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def boilerplate_directory_path(self):
        return os.path.join(self.score_manager_tools_directory_path, 'boilerplate')

    @property
    def configuration_directory_path(self):
        return self.score_manager_configuration_directory

    @property
    def configuration_file_name(self):
        return 'score_manager.cfg'

    @property
    def editors_package_path(self):
        return self.dot_join(['scoremanagertools', 'editors'])

    @property
    def editors_directory_path(self):
        return os.path.join(self.score_manager_tools_directory_path, 'editors')

    @property
    def handler_tools_directory_path(self):
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 'tools', 'handlertools')

    @property
    def makers_directory_path(self):
        return os.path.join(self.score_manager_tools_directory_path, 'makers')

    @property
    def makers_package_path(self):
        return self.dot_join([self.score_manager_tools_package_path, 'makers'])

    @property
    def score_external_chunks_package_path(self):
        return os.path.basename(self.score_manager_sketches_directory_path)

    @property
    def score_manager_sketches_directory_path(self):
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_external_chunks_directory_path(self):
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_external_materials_package_path(self):
        return os.path.basename(self.score_manager_materials_directory_path)

    @property
    def score_external_materials_directory_path(self):
        return self.score_manager_materials_directory_path

    @property
    def score_external_package_paths(self):
        return (
            self.score_external_chunks_package_path,
            self.score_external_materials_package_path,
            self.score_external_specifiers_package_path,
            )

    @property
    def score_external_directory_pathS(self):
        return (
            self.score_external_chunks_directory_path,
            self.score_external_materials_directory_path,
            self.score_external_specifiers_directory_path,
            )

    @property
    def score_external_specifiers_package_path(self):
        return os.path.basename(self.score_manager_specifiers_directory_path)

    @property
    def score_external_specifiers_directory_path(self):
        return self.score_manager_specifiers_directory_path

    @property
    def score_internal_chunks_package_path_infix(self):
        return 'mus.chunks'

    @property
    def score_internal_materials_package_path_infix(self):
        return 'mus.materials'

    @property
    def score_internal_specifiers_package_path_infix(self):
        return 'mus.specifiers'

    @property
    def score_manager_tools_fully_qualified_package_name(self):
        return 'experimental.tools.scoremanagertools'

    @property
    def score_manager_tools_package_path(self):
        return os.path.basename(self.score_manager_tools_directory_path)

    @property
    def score_manager_materials_directory_path(self):
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'materials')
    
    @property
    def score_manager_specifiers_directory_path(self):
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'specifiers')
    
    @property
    def score_manager_tools_directory_path(self):
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 
            'tools', 
            'scoremanagertools')
        
    @property
    def score_manager_transcripts_directory_path(self):
        return self._settings['score_manager_transcripts_directory_path']

    @property
    def score_manager_configuration_directory(self):
        return os.path.join(self.home_directory_path, '.score_manager')

    @property
    def scores_directory_path(self):
        return os.path.normpath(self._settings['scores_directory_path'])

    @property
    def specifier_classes_package_path(self):
        return self.dot_join(['scoremanagertools', 'specifiers'])

    @property
    def specifier_classes_directory_path(self):
        return os.path.join(self.score_manager_tools_directory_path, 'specifiers')

    @property
    def stylesheets_directory_path(self):
        return os.path.join(self.score_manager_tools_directory_path, 'stylesheets')

    @property
    def stylesheets_package_path(self):
        return self.dot_join([self.score_manager_tools_package_path, 'stylesheets'])

    @property
    def user_makers_directory_path(self):
        return self._settings['user_specific_score_manager_makers_directory_path']

    @property
    def user_makers_package_path(self):
        return self._settings['user_specific_score_manager_makers_package_path']

    ### PUBLIC METHODS ###

    def dot_join(self, expr):
        return '.'.join(expr)
