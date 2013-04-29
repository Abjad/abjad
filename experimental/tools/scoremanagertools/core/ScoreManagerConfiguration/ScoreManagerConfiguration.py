import os
from abjad.tools.configurationtools.Configuration import Configuration
from abjad.tools.configurationtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(Configuration):
    '''Score manager configuration.

        >>> configuration = scoremanagertools.core.ScoreManagerConfiguration()
        >>> configuration
        ScoreManagerConfiguration()
    
    Treated as a singleton.
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

    @property
    def _score_internal_segments_package_path_infix(self):
        return 'mus.chunks'

    @property
    def _score_internal_materials_package_path_infix(self):
        return 'mus.materials'

    @property
    def _score_internal_specifiers_package_path_infix(self):
        return 'mus.specifiers'

    ### READ-ONLY PUBLIC PROPERTIES ###

    def trim(self, asset_path):
        index = asset_path.index('abjad')
        return asset_path[index:]
        
    @property
    def boilerplate_directory_path(self):
        '''Boilerplate directory path:

        ::

            >>> configuration.trim(configuration.boilerplate_directory_path)
            'abjad/experimental/tools/scoremanagertools/boilerplate'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'boilerplate')

    @property
    def configuration_directory_path(self):
        '''Configuration directory path:

        ::

            >>> configuration.configuration_directory_path # doctest: +SKIP
            '~/.score_manager'

        Return string.
        '''
        return self.score_manager_configuration_directory

    @property
    def configuration_file_name(self):
        '''Configuration file name:

        ::

            >>> configuration.configuration_file_name
            'score_manager.cfg'

        Return string.
        '''
        return 'score_manager.cfg'

    @property
    def configuration_file_path(self):
        '''Configuration file path:

        ::

            >>> configuration.configuration_file_path # doctest: +SKIP
            '~/.score_manager/score_manager.cfg'

        Return string.
        '''
        return Configuration.configuration_file_path.fget(self)

    @property
    def editors_directory_path(self):
        '''Editors directory path:

        ::

            >>> configuration.trim(configuration.editors_directory_path)
            'abjad/experimental/tools/scoremanagertools/editors'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'editors')

    @property
    def editors_package_path(self):
        '''Editors package path:

        ::

            >>> configuration.editors_package_path
            'scoremanagertools.editors'

        Return string.
        '''
        return self.dot_join(['scoremanagertools', 'editors'])

    @property
    def handler_tools_directory_path(self):
        '''Handler tools directory path:

        ::

            >>> configuration.trim(configuration.handler_tools_directory_path)
            'abjad/experimental/tools/handlertools'

        Return string.
        '''
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 'tools', 'handlertools')

    @property
    def help_item_width(self):
        '''Help item width:

        ::

            >>> configuration.help_item_width
            5

        Return constant integer.
        '''
        return 5

    @property
    def home_directory_path(self):
        '''Home directory path:

        ::

            >>> configuration.home_directory_path # doctest: +SKIP
            '~'

        Return string.
        '''
        return Configuration.home_directory_path.fget(self)

    @property
    def makers_directory_path(self):
        '''Makers directory path:

        ::

            >>> configuration.trim(configuration.makers_directory_path)
            'abjad/experimental/tools/scoremanagertools/makers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'makers')

    @property
    def makers_package_path(self):
        '''Makers package path:

        ::

            >>> configuration.makers_package_path
            'scoremanagertools.makers'

        Return string.
        '''
        return self.dot_join([self.score_manager_tools_package_name, 'makers'])

    @property
    def score_external_segments_directory_path(self):
        '''Score-external chunks directory path:

        ::

            >>> configuration.score_external_segments_directory_path # doctest: +SKIP
            '~/.score_manager/sketches'

        Return string.
        '''
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_external_segments_package_path(self):
        '''Score-external chunks package path:

        ::

            >>> configuration.score_external_segments_package_path
            'sketches'

        Return string.
        '''
        return os.path.basename(self.score_manager_sketches_directory_path)

    @property
    def score_external_materials_directory_path(self):
        '''Score-external materials directory path:

        ::

            >>> configuration.trim(configuration.score_external_materials_directory_path)
            'abjad/experimental/materials'

        Return string.
        '''
        return self.score_manager_materials_directory_path

    @property
    def score_external_materials_package_path(self):
        '''Score-external materials package path:

        ::

            >>> configuration.score_external_materials_package_path
            'materials'

        Return string.
        '''
        return os.path.basename(self.score_manager_materials_directory_path)

    @property
    def score_external_package_paths(self):
        '''Score-external package paths:

        ::

            >>> for package_path in configuration.score_external_package_paths:
            ...     package_path
            'sketches'
            'materials'
            'specifiers'

        Return string.
        '''
        return (
            self.score_external_segments_package_path,
            self.score_external_materials_package_path,
            self.score_external_specifiers_package_path,
            )

    @property
    def score_external_specifiers_directory_path(self):
        '''Score-external specifiers directory path:

        ::

            >>> configuration.trim(configuration.score_external_specifiers_directory_path)
            'abjad/experimental/specifiers'

        Return string.
        '''
        return self.score_manager_specifiers_directory_path

    @property
    def score_external_specifiers_package_path(self):
        '''Score-external specifiers package path:

        ::

            >>> configuration.score_external_specifiers_package_path
            'specifiers'

        Return string.
        '''
        return os.path.basename(self.score_manager_specifiers_directory_path)

    @property
    def score_manager_configuration_directory(self):
        '''Score manager configuration directory:

        ::

            >>> configuration.score_manager_configuration_directory # doctest: +SKIP
            '~/.score_manager'

        Return string.
        '''
        return os.path.join(self.home_directory_path, '.score_manager')

    @property
    def score_manager_materials_directory_path(self):
        '''Score manager materials directory path:

        ::

            >>> configuration.trim(configuration.score_manager_materials_directory_path)
            'abjad/experimental/materials'

        Return string.
        '''
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'materials')
    
    @property
    def score_manager_sketches_directory_path(self):
        '''Score manager sketches directory path:

        ::

            >>> configuration.score_manager_sketches_directory_path # doctest: +SKIP
            '~/.score_manager/sketches'

        Return string.
        '''
        return self._settings['score_manager_sketches_directory_path']

    @property
    def score_manager_specifiers_directory_path(self):
        '''Score manager sketches directory path:

        ::

            >>> configuration.trim(configuration.score_manager_specifiers_directory_path)
            'abjad/experimental/specifiers'

        Return string.
        '''
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'specifiers')
    
    @property
    def score_manager_tools_directory_path(self):
        '''Score manager tools directory path:

        ::

            >>> configuration.trim(configuration.score_manager_tools_directory_path)
            'abjad/experimental/tools/scoremanagertools'

        Return string.
        '''
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 
            'tools', 
            'scoremanagertools')
        
    @property
    def score_manager_tools_package_name(self):
        '''Score manager tools package name:

        ::

            >>> configuration.score_manager_tools_package_name
            'scoremanagertools'

        Return string.
        '''
        return 'scoremanagertools'

    @property
    def score_manager_tools_package_path(self):
        '''Score manager tools package path:

        ::

            >>> configuration.score_manager_tools_package_path
            'experimental.tools.scoremanagertools'

        Return string.
        '''
        return 'experimental.tools.scoremanagertools'

    # TODO: change name to user_specified_transcripts_directory_path
    @property
    def score_manager_transcripts_directory_path(self):
        '''Score manager transcripts directory path:

        ::

            >>> configuration.score_manager_transcripts_directory_path # doctest: +SKIP
            '~/.score_manager/transcripts'

        Return string.
        '''
        return self._settings['score_manager_transcripts_directory_path']

    # TODO: change name to user_scores_directory_path
    @property
    def scores_directory_path(self):
        '''Scores directory path:

        ::

            >>> configuration.scores_directory_path # doctest: +SKIP
            '~/scores'

        Return string.
        '''
        return os.path.normpath(self._settings['scores_directory_path'])

    @property
    def specifier_classes_directory_path(self):
        '''Specifier classes directory path:

        ::

            >>> configuration.trim(configuration.specifier_classes_directory_path)
            'abjad/experimental/tools/scoremanagertools/specifiers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'specifiers')

    @property
    def specifier_classes_package_path(self):
        '''Specifier classes package path:

        ::

            >>> configuration.specifier_classes_package_path
            'scoremanagertools.specifiers'

        Return string.
        '''
        return self.dot_join(['scoremanagertools', 'specifiers'])

    @property
    def storage_format(self):
        '''Storage format:

            >>> z(configuration)
            core.ScoreManagerConfiguration()

        Return string.
        '''
        return Configuration.storage_format.fget(self)

    @property
    def stylesheets_directory_path(self):
        '''Stylesheets directory path:

        ::

            >>> configuration.trim(configuration.stylesheets_directory_path)
            'abjad/experimental/tools/scoremanagertools/stylesheets'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'stylesheets')

    @property
    def stylesheets_package_path(self):
        '''Stylesheets package path:

        ::

            >>> configuration.stylesheets_package_path
            'scoremanagertools.stylesheets'

        Return string.
        '''
        return self.dot_join([self.score_manager_tools_package_name, 'stylesheets'])

    @property
    def user_specific_makers_directory_path(self):
        '''User-specific makers directory path:

        ::

            >>> configuration.user_specific_makers_directory_path # doctest: +SKIP
            'username/music/makers'

        Return string.
        '''
        return self._settings['user_specific_score_manager_makers_directory_path']

    @property
    def user_specific_makers_package_path(self):
        '''User-specific makers package path:

        ::

            >>> configuration.user_specific_makers_package_path # doctest: +SKIP
            'username.music.makers'

        Return string.
        '''
        return self._settings['user_specific_score_manager_makers_package_path']

    ### PUBLIC METHODS ###

    def dot_join(self, expr):
        return '.'.join(expr)
