# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(AbjadConfiguration):
    r'''Score manager configuration.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> configuration = score_manager.configuration
            >>> configuration
            ScoreManagerConfiguration()

    '''

    ### INITIALIZER ###

    def __init__(self):
        AbjadConfiguration.__init__(self)

        # built-in asset library package paths

        self.built_in_editors_package_path = '.'.join([
            self.score_manager_package_path,
            'editors',
            ])
        self.built_in_material_package_managers_package_path = '.'.join([
            self.score_manager_package_path,
            'materialpackagemanagers',
            ])
        self.built_in_material_packages_package_path = '.'.join([
            self.score_manager_package_path,
            'materialpackages',
            ])

        # user asset library directory paths

        self.user_asset_library_directory_path = \
            os.path.normpath(os.path.expanduser(
            self._settings['user_asset_library_directory_path']
            ))
        self.user_asset_library_editors_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'editors',
            )
        self.user_asset_library_material_package_managers_directory_path = \
            os.path.join(
            self.user_asset_library_directory_path,
            'material_package_managers',
            )
        self.user_asset_library_material_packages_directory_path = \
            os.path.join(
            self.user_asset_library_directory_path,
            'material_packages',
            )
        self.user_asset_library_specifiers_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'specifiers',
            )
        self.user_asset_library_stylesheets_directory_path = os.path.join(
            self.user_asset_library_directory_path,
            'stylesheets',
            )

        # user asset library package paths

        self.user_asset_library_package_path = 'score_manager_asset_library'
        self.user_asset_library_editors_package_path = '.'.join([
            self.user_asset_library_package_path,
            'editors',
            ])
        self.user_asset_library_material_package_managers_package_path = \
            '.'.join([
            self.user_asset_library_package_path,
            'material_package_managers',
            ])
        self.user_asset_library_material_packages_package_path = '.'.join([
            self.user_asset_library_package_path,
            'material_packages',
            ])
        self.user_asset_library_specifiers_package_path = '.'.join([
            self.user_asset_library_package_path,
            'specifiers',
            ])

        # built-in score packages

        self.built_in_score_packages_directory_path = os.path.join(
            self.score_manager_directory_path,
            'scorepackages',
            )
        self.built_in_score_packages_package_path = '.'.join([
            self.score_manager_package_path,
            'scorepackages',
            ])

        # user score packages

        self.user_score_packages_directory_path = \
            os.path.normpath(os.path.expanduser(
            self._settings['user_score_packages_directory_path']
            ))
        self.user_score_packages_package_path = ''

        self._make_missing_packages()
        self._make_missing_directories()

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Score manager tools configuration file created on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj'
            ' and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            'user_asset_library_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you'
                    ' house your user-specific assets.',
                    'Defaults to $HOME/score_manager_asset_library/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path,
                        'score_manager_asset_library',
                        )
                    ),
            },
            'user_score_packages_directory_path': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores.',
                    'Defaults to $HOME/score_packages/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path, 
                        'score_packages',
                        )
                    )
            },
        }
        return options

    ### PRIVATE METHODS ###

    def _make_missing_directories(self):
        directory_paths = (
            self.user_score_packages_directory_path,
            self.user_asset_library_stylesheets_directory_path,
            self.transcripts_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

    def _make_missing_packages(self):
        directory_paths = (
            self.user_asset_library_directory_path,
            self.user_asset_library_editors_directory_path,
            self.user_asset_library_material_package_managers_directory_path,
            self.user_asset_library_material_packages_directory_path,
            self.user_asset_library_specifiers_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                file_path = os.path.join(directory_path, '__init__.py')
                file(file_path, 'w').write('')

    ### PUBLIC PROPERTIES ###

    @property
    def built_in_editors_directory_path(self):
        r'''Gets built-in editors directory path.

        ..  container:: example

            ::

                >>> configuration.built_in_editors_directory_path
                '.../scoremanager/editors'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'editors',
            )
        return path

    @property
    def built_in_material_package_managers_directory_path(self):
        r'''Gets built-in material package managers directory path.

        ..  container:: example

            ::

                >>> configuration.built_in_material_package_managers_directory_path
                '.../scoremanager/materialpackagemanagers'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'materialpackagemanagers',
            )
        return path

    @property
    def built_in_material_packages_directory_path(self):
        r'''Gets built-in material packages directory path.

        ..  container:: example

            ::

                >>> configuration.built_in_material_packages_directory_path
                '.../scoremanager/materialpackages'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'materialpackages',
            )
        return path

    @property
    def built_in_stylesheets_directory_path(self):
        r'''Gets built-in stylesheets directory path.

        ..  container:: example

            ::

                >>> configuration.built_in_stylesheets_directory_path
                '.../abjad/stylesheets'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_directory_path,
            'stylesheets',
            )
        return path

    @property
    def built_in_score_package_names(self):
        r'''Gets built-in score package names.

        ..  container:: example

            ::

                >>> for x in configuration.built_in_score_package_names:
                ...     x
                'blue_example_score'
                'green_example_score'
                'red_example_score'

        Returns tuple of strings.
        '''
        return (
            'blue_example_score',
            'green_example_score',
            'red_example_score',
            )

    @property
    def cache_file_path(self):
        r'''Gets cache file path.

        ..  container:: example

            ::

                >>> configuration.cache_file_path
                '.../.score_manager/cache.py'

        Returns string.
        '''
        file_path = self._cache_file_path = os.path.join(
            self.configuration_directory_path, 
            'cache.py',
            )
        return file_path

    @property
    def configuration_directory_path(self):
        r'''Gets configuration directory path.

        ..  container:: example

            ::

                >>> configuration.configuration_directory_path
                '.../.score_manager'

        Defaults to path of hidden ``.score_manager`` directory.

        Returns string.
        '''
        return os.path.join(self.home_directory_path, '.score_manager')

    @property
    def configuration_file_name(self):
        r'''Gets configuration file name.

        ..  container:: example

            ::

                >>> configuration.configuration_file_name
                'score_manager.cfg'

        Returns string.
        '''
        return 'score_manager.cfg'

    @property
    def configuration_file_path(self):
        r'''Gets configuration file path.

        ..  container:: example

            ::

                >>> configuration.configuration_file_path
                '.../.score_manager/score_manager.cfg'

        Returns string.
        '''
        superclass = super(ScoreManagerConfiguration, self)
        return superclass.configuration_file_path

    @property
    def handler_tools_directory_path(self):
        r'''Gets handler tools directory path.

        ..  container:: example

            ::

                >>> configuration.handler_tools_directory_path
                '.../experimental/tools/handlertools'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_experimental_directory_path,
            'tools',
            'handlertools',
            )
        return path
        
    @property
    def home_directory_path(self):
        r'''Gets home directory path.

        ..  container:: example

            ::

                >>> configuration.home_directory_path
                '...'

        Returns string.
        '''
        superclass = super(ScoreManagerConfiguration, self)
        return superclass.home_directory_path

    @property
    def score_manager_package_path(self):
        r'''Gets score manager package path.

        ..  container:: example

            ::

                >>> configuration.score_manager_package_path
                'scoremanager'

        Returns string.
        '''
        return 'scoremanager'

    @property
    def transcripts_directory_path(self):
        r'''Gets score manager transcripts directory path.

        ..  container:: example

            ::

                >>> configuration.transcripts_directory_path
                '.../.score_manager/transcripts'

        Returns string.
        '''
        path = os.path.join(
            self.configuration_directory_path,
            'transcripts',
            )
        return path

    ### PUBLIC METHODS ###

    def filesystem_path_to_packagesystem_path(self, filesystem_path):
        r'''Changes `filesystem_path` to package path.

        Returns string.
        '''
        if filesystem_path is None:
            return
        assert isinstance(filesystem_path, str), repr(filesystem_path)
        filesystem_path = os.path.normpath(filesystem_path)
        if filesystem_path.endswith('.py'):
            filesystem_path = filesystem_path[:-3]
        if filesystem_path.startswith(
            self.built_in_score_packages_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_asset_library_material_packages_directory_path):
            prefix_length = \
                len(self.user_asset_library_material_packages_directory_path) + 1
            remainder = filesystem_path[prefix_length:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(
                    self.user_asset_library_material_packages_package_path, 
                    remainder)
            else:
                result = self.user_asset_library_material_packages_package_path
            return result
        elif filesystem_path.startswith(
            self.user_asset_library_material_package_managers_directory_path):
            return '.'.join([
                self.user_asset_library_material_package_managers_package_path,
                os.path.basename(filesystem_path)])
        elif filesystem_path.startswith(
            self.built_in_material_package_managers_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.built_in_material_packages_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.score_manager_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_directory_path)) + 1
        elif filesystem_path.startswith(
            self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_asset_library_stylesheets_directory_path):
            prefix_length = \
                len(os.path.dirname(
                self.user_asset_library_stylesheets_directory_path)) + 1
        elif filesystem_path.startswith(self.abjad_stylesheets_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        else:
            message = 'can not change filesystem path'
            message += ' to packagesystem path: {!r}.'
            raise Exception(message.format(filesystem_path))
        packagesystem_path = filesystem_path[prefix_length:]
        packagesystem_path = packagesystem_path.replace(os.path.sep, '.')
        return packagesystem_path

    def list_score_directory_paths(
        self, 
        built_in=False, 
        user=False, 
        head=None,
        ):
        r'''Lists score directory paths.

        Example. List built-in score directory paths:

        ::

            >>> for x in configuration.list_score_directory_paths(
            ...     built_in=True):
            ...     x
            '.../scoremanager/scorepackages/blue_example_score'
            '.../scoremanager/scorepackages/green_example_score'
            '.../scoremanager/scorepackages/red_example_score'

        Returns list.
        '''
        result = []
        if built_in:
            for directory_entry in \
                sorted(os.listdir(
                    self.built_in_score_packages_directory_path)):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.built_in_score_packages_package_path,
                        directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.built_in_score_packages_directory_path,
                            directory_entry)
                        result.append(filesystem_path)
        if user:
            for directory_entry in \
                sorted(os.listdir(self.user_score_packages_directory_path)):
                if directory_entry[0].isalpha():
                    package_path = '.'.join([
                        self.user_score_packages_package_path,
                        directory_entry])
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.user_score_packages_directory_path,
                            directory_entry)
                        result.append(filesystem_path)
        return result

    def packagesystem_path_exists(self, packagesystem_path):
        r'''Is true whens `packagesystem_path` exists. Otherwise false.

        ::

            >>> packagesystem_path = 'scoremanager.materialpackages'
            >>> configuration.packagesystem_path_exists(packagesystem_path)
            True

        Returns boolean.
        '''
        assert os.path.sep not in packagesystem_path
        filesystem_path = \
            self.packagesystem_path_to_filesystem_path(packagesystem_path)
        return os.path.exists(filesystem_path)

    def packagesystem_path_to_filesystem_path(
        self, 
        packagesystem_path, 
        is_module=False,
        ):
        r'''Changes `packagesystem_path` to filesystem path.

        Returns string.
        '''
        if packagesystem_path is None:
            return
        assert isinstance(packagesystem_path, str), repr(packagesystem_path)
        packagesystem_path_parts = packagesystem_path.split('.')
        if packagesystem_path_parts[0] == 'scoremanager':
            directory_parts = [self.score_manager_directory_path] + \
                packagesystem_path_parts[1:]
        elif packagesystem_path_parts[:3] == \
            ['experimental', 'tools', 'scoremanager']:
            directory_parts = [self.score_manager_directory_path] + \
                packagesystem_path_parts[3:]
        elif packagesystem_path_parts[0] == \
            self.built_in_material_packages_package_path:
            directory_parts = \
                [self.built_in_material_packages_filesystem_path] + \
                packagesystem_path_parts[1:]
        elif packagesystem_path.startswith(
            self.user_asset_library_package_path):
            prefix_length = len(self.user_asset_library_package_path)
            trimmed_packagesystem_path = packagesystem_path[prefix_length:]
            directory_parts = []
            directory_parts.append(self.user_asset_library_directory_path)
            directory_parts.extend(trimmed_packagesystem_path.split('.'))
        elif packagesystem_path_parts[-1] in self.built_in_score_package_names:
            directory_parts = []
            directory_parts.append(self.built_in_score_packages_directory_path)
            directory_parts.append(packagesystem_path_parts[-1])
        else:
            directory_parts = \
                [self.user_score_packages_directory_path] + \
                packagesystem_path_parts[:]
        filesystem_path = os.path.join(*directory_parts)
        filesystem_path = os.path.normpath(filesystem_path)
        if is_module:
            filesystem_path += '.py'
        return filesystem_path
