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
            'user_sketches_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager to store sketches.',
                    'Defaults to $HOME/.score_manager/sketches/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.configuration_directory_path, 'sketches'))
            },
            'transcripts_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you want score manager transcripts written.',
                    'Defaults to $HOME/.score_manager/transcripts/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.configuration_directory_path, 'transcripts'))
            },
            'user_scores_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores. No default provided.'
                ],
                'spec': "string(default='')"
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
        }
        return options

    @property
    def _score_internal_materials_package_path_infix(self):
        return 'music.materials'

    @property
    def _score_internal_segments_package_path_infix(self):
        return 'music.segments'

    @property
    def _score_internal_specifiers_package_path_infix(self):
        return 'music.specifiers'

    ### READ-ONLY PUBLIC PROPERTIES ###

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
        return os.path.join(self.home_directory_path, '.score_manager')

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
    def system_editors_directory_path(self):
        '''Editors directory path:

        ::

            >>> configuration.trim(configuration.system_editors_directory_path)
            'abjad/experimental/tools/scoremanagertools/editors'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'editors')

    # TODO: maybe remove because unused?
    @property
    def system_editors_package_path(self):
        '''Editors package path:

        ::

            >>> configuration.system_editors_package_path
            'scoremanagertools.editors'

        Return string.
        '''
        return '.'.join(['scoremanagertools', 'editors'])

    @property
    def system_material_package_makers_directory_path(self):
        '''Makers directory path:

        ::

            >>> configuration.trim(configuration.system_material_package_makers_directory_path)
            'abjad/experimental/tools/scoremanagertools/materialpackagemakers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'materialpackagemakers')

    @property
    def system_material_package_makers_package_path(self):
        '''Makers package path:

        ::

            >>> configuration.system_material_package_makers_package_path
            'scoremanagertools.materialpackagemakers'

        Return string.
        '''
        return 'scoremanagertools.materialpackagemakers'

    @property
    def system_materials_directory_path(self):
        '''System materials directory path:

        ::

            >>> configuration.system_materials_directory_path
            '/Users/trevorbaca/Documents/abjad/experimental/system_materials'

        Return string.
        '''
        return os.path.join(self.abjad_configuration.abjad_experimental_directory_path, 'system_materials')

    @property
    def system_materials_package_path(self):
        '''System materials package path:

        ::

            >>> configuration.system_materials_package_path
            'system_materials'

        Return string.
        '''
        return os.path.basename(self.system_materials_directory_path)

    @property
    def system_package_paths(self):
        '''System package paths:

        ::

            >>> for package_path in configuration.system_package_paths:
            ...     package_path
            'sketches'
            'system_materials'
            'system_specifiers'

        Return string.
        '''
        return (
            self.user_sketches_package_path,
            self.system_materials_package_path,
            self.system_specifiers_package_path,
            )

    @property
    def system_specifier_classes_directory_path(self):
        '''Specifier classes directory path:

        ::

            >>> configuration.trim(configuration.system_specifier_classes_directory_path)
            'abjad/experimental/tools/scoremanagertools/specifiers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'specifiers')

    # TODO: maybe remove because unused?
    @property
    def system_specifier_classes_package_path(self):
        '''Specifier classes package path:

        ::

            >>> configuration.system_specifier_classes_package_path
            'scoremanagertools.specifiers'

        Return string.
        '''
        return '.'.join(['scoremanagertools', 'specifiers'])

    @property
    def system_specifiers_directory_path(self):
        '''Score manager sketches directory path:

        ::

            >>> configuration.trim(configuration.system_specifiers_directory_path)
            'abjad/experimental/system_specifiers'

        Return string.
        '''
        return os.path.join(
            self.abjad_configuration.abjad_experimental_directory_path, 
            'system_specifiers')

    @property
    def system_specifiers_package_path(self):
        '''Score-external specifiers package path:

        ::

            >>> configuration.system_specifiers_package_path
            'system_specifiers'

        Return string.
        '''
        return os.path.basename(self.system_specifiers_directory_path)

    @property
    def system_stylesheets_directory_path(self):
        '''Stylesheets directory path:

        ::

            >>> configuration.trim(configuration.system_stylesheets_directory_path)
            'abjad/experimental/tools/scoremanagertools/stylesheets'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'stylesheets')

    # TODO: remove because shouldn't be a package?
    @property
    def system_stylesheets_package_path(self):
        '''Stylesheets package path:

        ::

            >>> configuration.system_stylesheets_package_path
            'scoremanagertools.stylesheets'

        Return string.
        '''
        return 'scoremanagertools.stylesheets'

    @property
    def transcripts_directory_path(self):
        '''Score manager transcripts directory path:

        ::

            >>> configuration.transcripts_directory_path # doctest: +SKIP
            '~/.score_manager/transcripts'

        Return string.
        '''
        return self._settings['transcripts_directory_path']

    @property
    def user_material_package_makers_directory_path(self):
        '''User material package makers directory path:

        ::

            >>> configuration.user_material_package_makers_directory_path # doctest: +SKIP
            '~/music/makers'

        Return string.
        '''
        return self._settings['user_material_package_makers_directory_path']

    @property
    def user_material_package_makers_package_path(self):
        '''User material package makers package path:

        ::

            >>> configuration.user_material_package_makers_package_path # doctest: +SKIP
            '~.music.makers'

        Return string.
        '''
        return self._settings['user_material_package_makers_package_path']

    @property
    def user_scores_directory_path(self):
        '''Scores directory path:

        ::

            >>> configuration.user_scores_directory_path # doctest: +SKIP
            '~/scores'

        Return string.
        '''
        return os.path.normpath(self._settings['user_scores_directory_path'])

    @property
    def user_sketches_directory_path(self):
        '''Score-external segments directory path:

        ::

            >>> configuration.user_sketches_directory_path # doctest: +SKIP
            '~/.score_manager/sketches'

        Return string.
        '''
        return self._settings['user_sketches_directory_path']

    @property
    def user_sketches_directory_path(self):
        '''Score manager sketches directory path:

        ::

            >>> configuration.user_sketches_directory_path # doctest: +SKIP
            '~/.score_manager/sketches'

        Return string.
        '''
        return self._settings['user_sketches_directory_path']

    @property
    def user_sketches_package_path(self):
        '''Score-external segments package path:

        ::

            >>> configuration.user_sketches_package_path
            'sketches'

        Return string.
        '''
        return os.path.basename(self.user_sketches_directory_path)

    ### PUBLIC METHODS ###

    def trim(self, asset_filesystem_path):
        index = asset_filesystem_path.index('abjad')
        return asset_filesystem_path[index:]
