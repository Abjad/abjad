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
        if not os.path.exists(self.transcripts_directory_path):
            os.makedirs(self.transcripts_directory_path)

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
            'transcripts_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager transcripts written.',
                    'Defaults to $HOME/score_manager/transcripts/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.configuration_directory_path, 'transcripts'))
            },
            'user_material_package_makers_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific makers.',
                    'Always set together with user_material_package_makers_package_path.',
                    'Defaults to none.'
                ],
                'spec': "string(default='')"
            },
            'user_material_package_makers_package_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific makers.',
                    'Always set together with user_material_package_makers_directory_path.',
                    'Defaults to none.'
                ],
                'spec': "string(default='')"
            },
            'user_scores_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores. No default provided.',
                    'Defaults to $HOME/Documents/scores/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.home_directory_path, 'Documents', 'scores'))
            },
            'user_sketches_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager to store sketches.',
                    'Defaults to $HOME/score_manager/sketches/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.configuration_directory_path, 'sketches'))
            },
            'user_stylesheets_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house user-specific stylesheets.',
                    'Defaults to $HOME/score_manager/stylesheets/.' 
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.configuration_directory_path, 'stylesheets'))
            },
        }
        return options

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def built_in_editors_directory_path(self):
        '''Editors directory path:

        ::

            >>> configuration.built_in_editors_directory_path
            '.../abjad/experimental/tools/scoremanagertools/editors'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'editors')

    @property
    def built_in_material_package_makers_directory_path(self):
        '''Makers directory path:

        ::

            >>> configuration.built_in_material_package_makers_directory_path
            '.../abjad/experimental/tools/scoremanagertools/materialpackagemakers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'materialpackagemakers')

    @property
    def built_in_materials_directory_path(self):
        '''System materials directory path:

        ::

            >>> configuration.built_in_materials_directory_path
            '.../abjad/experimental/built_in_materials'

        Return string.
        '''
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'built_in_materials')

    @property
    def built_in_materials_package_path(self):
        '''System materials package path:

        ::

            >>> configuration.built_in_materials_package_path
            'built_in_materials'

        Return string.
        '''
        return os.path.basename(self.built_in_materials_directory_path)

    @property
    def built_in_scores_directory_path(self):
        '''Built-in scores directory path:

        ::

            >>> configuration.built_in_scores_directory_path
            '.../abjad/experimental/tools/scoremanagertools/built_in_scores'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'built_in_scores')

    @property
    def built_in_scores_package_path(self):
        '''Built-in scores package path:

        ::

            >>> configuration.built_in_scores_package_path
            'experimental.tools.scoremanagertools.built_in_scores'

        Return string.
        '''
        return 'experimental.tools.scoremanagertools.built_in_scores'

    @property
    def built_in_specifier_classes_directory_path(self):
        '''Specifier classes directory path:

        ::

            >>> configuration.built_in_specifier_classes_directory_path
            '.../abjad/experimental/tools/scoremanagertools/specifiers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'specifiers')

    @property
    def built_in_specifiers_directory_path(self):
        '''Score manager sketches directory path:

        ::

            >>> configuration.built_in_specifiers_directory_path
            '.../abjad/experimental/built_in_specifiers'

        Return string.
        '''
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 
            'built_in_specifiers')

    @property
    def built_in_specifiers_package_path(self):
        '''Score-external specifiers package path:

        ::

            >>> configuration.built_in_specifiers_package_path
            'built_in_specifiers'

        Return string.
        '''
        return os.path.basename(self.built_in_specifiers_directory_path)

    @property
    def configuration_directory_path(self):
        '''Configuration directory path:

        ::

            >>> configuration.configuration_directory_path # doctest: +SKIP
            '~/score_manager'

        Return string.
        '''
        return os.path.join(self.home_directory_path, 'score_manager')

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
            '~/score_manager/score_manager.cfg'

        Return string.
        '''
        return Configuration.configuration_file_path.fget(self)

    @property
    def home_directory_path(self):
        '''Home directory path:

        ::

            >>> configuration.home_directory_path # doctest: +SKIP
            '~'

        (Output will vary according to configuration.)

        Return string.
        '''
        return Configuration.home_directory_path.fget(self)

    @property
    def score_manager_tools_directory_path(self):
        '''Score manager tools directory path:

        ::

            >>> configuration.score_manager_tools_directory_path
            '.../abjad/experimental/tools/scoremanagertools'

        Return string.
        '''
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path,
            'tools',
            'scoremanagertools')

    @property
    def score_manager_tools_package_path(self):
        '''Score manager tools package path:

        ::

            >>> configuration.score_manager_tools_package_path
            'experimental.tools.scoremanagertools'

        Return string.
        '''
        return 'experimental.tools.scoremanagertools'

    @property
    def storage_format(self):
        '''Storage format:

            >>> z(configuration)
            core.ScoreManagerConfiguration()

        Return string.
        '''
        return Configuration.storage_format.fget(self)

    @property
    def transcripts_directory_path(self):
        '''Score manager transcripts directory path:

        ::

            >>> configuration.transcripts_directory_path # doctest: +SKIP
            '~/score_manager/transcripts'

        (Output will vary according to configuration.)

        Return string.
        '''
        return self._settings['transcripts_directory_path']

    @property
    def user_material_package_makers_directory_path(self):
        '''User material package makers directory path:

        ::

            >>> configuration.user_material_package_makers_directory_path # doctest: +SKIP
            '~/music/materialpackagemakers'

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.normpath(os.path.expanduser(
            self._settings['user_material_package_makers_directory_path']
            ))

    @property
    def user_material_package_makers_package_path(self):
        '''User material package makers package path:

        ::

            >>> configuration.user_material_package_makers_package_path # doctest: +SKIP
            '~.music.materialpackagemakers'

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.normpath(os.path.expanduser(
            self._settings['user_material_package_makers_package_path']
            ))

    @property
    def user_scores_directory_path(self):
        '''Scores directory path:

        ::

            >>> configuration.user_scores_directory_path # doctest: +SKIP
            '.../Documents/scores'

        Defaults to ``~/Documents/scores``.

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.normpath(os.path.expanduser(
            self._settings['user_scores_directory_path']
            ))

    @property
    def user_sketches_directory_path(self):
        '''Score-external segments directory path:

        ::

            >>> configuration.user_sketches_directory_path # doctest: +SKIP
            '~/score_manager/sketches'

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.normpath(os.path.expanduser(
            self._settings['user_sketches_directory_path']
            ))

    @property
    def user_sketches_package_path(self):
        '''Score-external segments package path:

        ::

            >>> configuration.user_sketches_package_path # doctest: +SKIP
            'sketches'

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.basename(self.user_sketches_directory_path)

    @property
    def user_stylesheets_directory_path(self):
        '''User stylesheets directory path:

        ::

            >>> configuration.user_stylesheets_directory_path
            '.../score_manager/stylesheets'

        (Output will vary according to configuration.)

        Return string.
        '''
        return os.path.normpath(os.path.expanduser(
            self._settings['user_stylesheets_directory_path']
            ))
