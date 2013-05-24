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

    ### CLASS VARIABLES ###

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
            'user_external_assets_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific assets.',
                    'Always set together with user_external_assets_package_path.',
                    'Defaults to none.'
                ],
                'spec': "string(default='')"
            },
            'user_external_assets_package_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your user-specific assets.',
                    'Always set together with user_external_assets_directory_path.',
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
            '.../tools/scoremanagertools/editors'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'editors')

    @property
    def built_in_material_package_makers_directory_path(self):
        '''Material package makers directory path:

        ::

            >>> configuration.built_in_material_package_makers_directory_path
            '.../tools/scoremanagertools/materialpackagemakers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'materialpackagemakers')

    @property
    def built_in_material_package_makers_package_path(self):
        '''Material package makers package path:

        ::

            >>> configuration.built_in_material_package_makers_package_path
            'experimental.tools.scoremanagertools.materialpackagemakers'

        '''
        return '.'.join([self.score_manager_tools_package_path, 'materialpackagemakers'])

    @property
    def built_in_materials_directory_path(self):
        '''System materials directory path:

        ::

            >>> configuration.built_in_materials_directory_path
            '.../tools/scoremanagertools/built_in_materials'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'built_in_materials')

    @property
    def built_in_materials_package_path(self):
        '''System materials package path:

        ::

            >>> configuration.built_in_materials_package_path
            'experimental.tools.scoremanagertools.built_in_materials'

        Return string.
        '''
        return '.'.join([self.score_manager_tools_package_path, 'built_in_materials'])

    @property
    def built_in_scores_directory_path(self):
        '''Built-in scores directory path:

        ::

            >>> configuration.built_in_scores_directory_path
            '.../tools/scoremanagertools/built_in_scores'

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
            '.../tools/scoremanagertools/specifiers'

        Return string.
        '''
        return os.path.join(self.score_manager_tools_directory_path, 'specifiers')

    @property
    def built_in_specifiers_directory_path(self):
        '''Built-in specifiers directory path:

        ::

            >>> configuration.built_in_specifiers_directory_path
            '.../tools/scoremanagertools/built_in_specifiers'

        Return string.
        '''
        return os.path.join(
            self.score_manager_tools_directory_path,
            'built_in_specifiers')

    @property
    def built_in_specifiers_package_path(self):
        '''Score-external specifiers package path:

        ::

            >>> configuration.built_in_specifiers_package_path
            'experimental.tools.scoremanagertools.built_in_specifiers'

        Return string.
        '''
        return 'experimental.tools.scoremanagertools.built_in_specifiers'

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
            '.../tools/scoremanagertools'

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
    def user_external_assets_directory_path(self):
        '''User external assets directory path:

        ::

            >>> configuration.user_external_assets_directory_path
            '/Users/trevorbaca/Documents/baca/music'

        Return string.
        '''
        return self._settings['user_external_assets_directory_path']

    @property
    def user_external_assets_package_path(self):
        '''User external assets package path:

        ::

            >>> configuration.user_external_assets_package_path # doctest: +SKIP
            '~.music'

        Return string.
        '''
        return self._settings['user_external_assets_package_path']
        
    @property
    def user_external_specifiers_directory_path(self):
        '''User external specifiers directory path:

        ::

            >>> configuration.user_external_specifiers_directory_path
            '/Users/trevorbaca/Documents/baca/music/specifiers'

        Return string.
        '''
        return os.path.join(self.user_external_assets_directory_path, 'specifiers')

    @property
    def user_external_specifiers_package_path(self):
        '''User external specifiers package path:

        ::

            >>> configuration.user_external_specifiers_package_path
            'baca.music.specifiers'

        Return string.
        '''
        return '.'.join([self.user_external_assets_package_path, 'specifiers'])

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
        return self._settings['user_material_package_makers_package_path']

    @property
    def user_materials_directory_path(self):
        '''User materials directory path:

        ::

            >>> configuration.user_materials_directory_path
            '/Users/trevorbaca/Documents/baca/music/materials'

        Return string.
        '''
        return os.path.join(self.user_external_assets_directory_path, 'materials')

    @property
    def user_materials_package_path(self):
        '''Use materials package path:

        ::

            >>> configuration.user_materials_package_path
            'baca.music.materials'

        (Output will vary with user configuration.)

        Return string.
        '''
        return '.'.join([self.user_external_assets_package_path, 'materials'])

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
    def user_scores_package_path(self):
        '''Scores package path:

        ::

            >>> configuration.user_scores_package_path 
            ''

        User scores must be directly importable.

        Return string.
        '''
        return ''

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

    ### PUBLIC METHODS ###

    def filesystem_path_to_packagesystem_path(self, filesystem_path):
        '''Change `filesystem_path` to package path.

        Return string.
        '''

        if filesystem_path is None:
            return
        assert isinstance(filesystem_path, str), repr(filesystem_path)
        filesystem_path = os.path.normpath(filesystem_path)
        if filesystem_path.endswith('.py'):
            filesystem_path = filesystem_path[:-3]
        if filesystem_path.startswith(self.built_in_scores_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.user_materials_directory_path):
            prefix_length = len(self.user_materials_directory_path) + 1
            remainder = filesystem_path[prefix_length:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(self.user_materials_package_path, remainder)
            else:
                result = self.user_materials_package_path
            return result
        elif filesystem_path.startswith(self.user_material_package_makers_directory_path):
            return '.'.join([
                self.user_material_package_makers_package_path,
                os.path.basename(filesystem_path)])
        elif filesystem_path.startswith(self.built_in_specifiers_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.built_in_material_package_makers_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.built_in_materials_directory_path):
            prefix_length = len(self.abjad_configuration.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.score_manager_tools_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_tools_directory_path)) + 1
        elif filesystem_path.startswith(self.user_scores_directory_path):
            prefix_length = len(self.user_scores_directory_path) + 1
        else:
            raise Exception('can not change to package path: {!r}'.format(filesystem_path))

        package_path = filesystem_path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')

        return package_path

    def list_score_directory_paths(self, built_in=False, user=False, head=None):
        '''List score directory paths.
    
        Example. List built-in score directory paths:

        ::

            >>> for x in configuration.list_score_directory_paths(built_in=True):
            ...     x
            '.../tools/scoremanagertools/built_in_scores/blue_example_score'
            '.../tools/scoremanagertools/built_in_scores/green_example_score'
            '.../tools/scoremanagertools/built_in_scores/red_example_score'

        Return list.
        '''
        result = []
        if built_in:
            for directory_entry in os.listdir(self.built_in_scores_directory_path):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.built_in_scores_package_path, directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.built_in_scores_directory_path, directory_entry)
                        result.append(filesystem_path)
        if user:
            for directory_entry in os.listdir(self.user_scores_directory_path):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.user_scores_package_path, directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.user_scores_directory_path, directory_entry)
                        result.append(filesystem_path)
        return result

    def packagesystem_path_exists(self, packagesystem_path):
        '''True when `packagesystem_path` exists. Otherwise false.

        Return boolean.
        '''
        assert os.path.sep not in packagesystem_path, repr(packagesystem_path)
        filesystem_path = self.packagesystem_path_to_filesystem_path(packagesystem_path)
        return os.path.exists(filesystem_path)

    def packagesystem_path_to_filesystem_path(self, package_path, is_module=False):
        '''Change `package_path` to directory path.
        
        Return string.
        '''

        if package_path is None:
            return
        assert isinstance(package_path, str), repr(package_path)
        package_path_parts = package_path.split('.')
        if package_path_parts[0] == 'scoremanagertools':
            directory_parts = [self.score_manager_tools_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[:3] == ['experimental', 'tools', 'scoremanagertools']:
            directory_parts = [self.score_manager_tools_directory_path] + \
                package_path_parts[3:]
        elif package_path_parts[0] == \
            self.built_in_materials_package_path:
            directory_parts = \
                [self.built_in_materials_directory_path] + \
                package_path_parts[1:]
        elif package_path_parts[0] == \
            self.built_in_specifiers_package_path:
            directory_parts = \
                [self.built_in_specifiers_directory_path] + \
                package_path_parts[1:]
        elif package_path.startswith(self.user_external_assets_package_path):
            prefix_length = len(self.user_external_assets_package_path)
            trimmed_package_path = package_path[prefix_length:]     
            directory_parts = []
            directory_parts.append(self.user_external_assets_directory_path)
            directory_parts.extend(trimmed_package_path.split('.'))
        else:
            directory_parts = [self.user_scores_directory_path] + package_path_parts[:]
        directory_path = os.path.join(*directory_parts)

        if is_module:
            directory_path += '.py'

        return directory_path
