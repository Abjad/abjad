# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(AbjadConfiguration):
    r'''Score manager configuration.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager()
            >>> configuration = score_manager._configuration
            >>> configuration
            ScoreManagerConfiguration()

    '''

    ### INITIALIZER ###

    def __init__(self):
        AbjadConfiguration.__init__(self)
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
            'score_manager_library': {
                'comment': [
                    '',
                    'Set to the directory where you'
                    ' house your score manager library.',
                    'Defaults to $HOME/score_manager_library/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path,
                        'score_manager_library',
                        )
                    ),
            },
            'scores_directory': {
                'comment': [
                    '',
                    'Set to the directory where you house your scores.',
                    'Defaults to $HOME/scores/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory_path, 
                        'scores',
                        )
                    )
            },
        }
        return options

    @property
    def _user_library_directory_name(self):
        directory_path = self.user_library_directory_path
        directory_name = os.path.split(directory_path)[-1]
        return directory_name

    ### PRIVATE METHODS ###

    def _make_missing_directories(self):
        directory_paths = (
            self.user_library_directory_path,
            self.user_library_editors_directory_path,
            self.user_library_material_managers_directory_path,
            self.user_library_material_packages_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                file_path = os.path.join(directory_path, '__init__.py')
                file(file_path, 'w').write('')
        directory_paths = (
            self.user_score_packages_directory_path,
            self.user_library_stylesheets_directory_path,
            self.transcripts_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_editors_directory_path(self):
        r'''Gets abjad editors directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_editors_directory_path
                '.../scoremanager/editors'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'editors',
            )
        return path

    @property
    def abjad_material_managers_directory_path(self):
        r'''Gets abjad material managers directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_material_managers_directory_path
                '.../scoremanager/managers'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'managers',
            )
        return path

    @property
    def abjad_material_packages_directory_path(self):
        r'''Gets abjad material packages directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_material_packages_directory_path
                '.../scoremanager/materials'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'materials',
            )
        return path

    @property
    def abjad_score_package_names(self):
        r'''Gets abjad score package names.

        ..  container:: example

            ::

                >>> for x in configuration.abjad_score_package_names:
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
    def abjad_score_packages_directory_path(self):
        r'''Gets abjad score packages directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_score_packages_directory_path
                '.../scoremanager/scores'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'scores',
            )
        return path

    @property
    def abjad_stylesheets_directory_path(self):
        r'''Gets abjad stylesheets directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_stylesheets_directory_path
                '.../abjad/stylesheets'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_directory_path,
            'stylesheets',
            )
        return path

    @property
    def boilerplate_directory_path(self):
        r'''Gets boilerplate directory path.

        ..  container:: example

            >>> configuration.boilerplate_directory_path
            '.../scoremanager/boilerplate'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'boilerplate',
            )
        return path

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

    @property
    def user_library_directory_path(self):
        r'''Gets user library directory path.

        ..  container:: example

            ::

                >>> configuration.user_library_directory_path
                '...'

        Aliases `score_manager_library` setting in score manager configuration
        file.

        Returns string.
        '''
        path = self._settings['score_manager_library']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    @property
    def user_library_editors_directory_path(self):
        r'''Gets user library editors path.

        ..  container:: example

            ::

                >>> configuration.user_library_editors_directory_path
                '.../editors'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'editors',
            )
        return path

    @property
    def user_library_material_managers_directory_path(self):
        r'''Gets user library material managers directory path.

        ..  container:: example

            ::

                >>> configuration.user_library_material_managers_directory_path
                '.../material_managers'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'material_managers',
            )
        return path

    @property
    def user_library_material_packages_directory_path(self):
        r'''Gets user library material packages directory path.

        ..  container:: example

            ::

                >>> configuration.user_library_material_packages_directory_path
                '.../material_packages'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'material_packages',
            )
        return path

    @property
    def user_library_stylesheets_directory_path(self):
        r'''Gets user library stylesheets directory path.

        ..  container:: example

            ::

                >>> configuration.user_library_stylesheets_directory_path
                '.../stylesheets'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'stylesheets',
            )
        return path

    @property
    def user_score_packages_directory_path(self):
        r'''Gets user score packages directory path.

        ..  container:: example

            ::

                >>> configuration.user_score_packages_directory_path
                '...'

        Aliases `scores_directory` setting in score manager configuration file.

        Returns string.
        '''
        path = self._settings['scores_directory']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    ### PUBLIC METHODS ###

    def list_score_directory_paths(
        self, 
        abjad=False, 
        user=False, 
        head=None,
        ):
        r'''Lists score directory paths.

        ..  container:: example

            Lists abjad score directory paths:

            ::

                >>> for x in configuration.list_score_directory_paths(
                ...     abjad=True):
                ...     x
                '.../scoremanager/scores/blue_example_score'
                '.../scoremanager/scores/green_example_score'
                '.../scoremanager/scores/red_example_score'

        Returns list.
        '''
        result = []
        if abjad:
            scores_directory_path = self.abjad_score_packages_directory_path
            directory_entries = sorted(os.listdir(scores_directory_path))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    directory_path = os.path.join(
                        scores_directory_path,
                        directory_entry,
                        )
                    package_path = self.path_to_package(
                        directory_path,
                        )
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.abjad_score_packages_directory_path,
                            directory_entry,
                            )
                        result.append(filesystem_path)
        if user:
            scores_directory_path = self.user_score_packages_directory_path
            directory_entries = sorted(os.listdir(scores_directory_path))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    package_path = directory_entry
                    if head is None or package_path.startswith(head):
                        filesystem_path = os.path.join(
                            self.user_score_packages_directory_path,
                            directory_entry,
                            )
                        result.append(filesystem_path)
        return result

    def package_exists(self, package_path):
        r'''Is true whens `package_path` exists. Otherwise false.

        ..  container:: example

            ::

                >>> package_path = 'scoremanager.materials'
                >>> configuration.package_exists(package_path)
                True

        Returns boolean.
        '''
        assert os.path.sep not in package_path
        filesystem_path = self.package_to_path(package_path)
        return os.path.exists(filesystem_path)

    def package_to_path(
        self, 
        package_path, 
        is_module=False,
        ):
        r'''Changes `package_path` to filesystem path.

        Appends ``.py`` when `is_module` is true.

        Returns string.
        '''
        if package_path is None:
            return
        assert isinstance(package_path, str), repr(package_path)
        package_path_parts = package_path.split('.')
        if package_path_parts[0] == 'scoremanager':
            directory_parts = [self.score_manager_directory_path]
            directory_parts += package_path_parts[1:]
        elif package_path_parts[0] == 'scoremanager.materials':
            directory_parts = [self.abjad_material_packages_filesystem_path]
            directory_parts += package_path_parts[1:]
        elif package_path.startswith(self._user_library_directory_name):
            prefix_length = len(self._user_library_directory_name)
            trimmed_package_path = package_path[prefix_length:]
            directory_parts = []
            directory_parts.append(self.user_library_directory_path)
            directory_parts.extend(trimmed_package_path.split('.'))
        elif package_path_parts[0] in self.abjad_score_package_names:
            directory_parts = []
            directory_parts.append(self.abjad_score_packages_directory_path)
            directory_parts.extend(package_path_parts)
        elif package_path_parts[-1] in self.abjad_score_package_names:
            directory_parts = []
            directory_parts.append(self.abjad_score_packages_directory_path)
            directory_parts.append(package_path_parts[-1])
        else:
            directory_parts = [self.user_score_packages_directory_path]
            directory_parts += package_path_parts[:]
        filesystem_path = os.path.join(*directory_parts)
        filesystem_path = os.path.normpath(filesystem_path)
        if is_module:
            filesystem_path += '.py'
        return filesystem_path

    def path_to_package(self, filesystem_path):
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
            self.abjad_score_packages_directory_path):
            prefix_length = len(self.abjad_score_packages_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_library_material_packages_directory_path):
            prefix_length = \
                len(self.user_library_material_packages_directory_path) + 1
            remainder = filesystem_path[prefix_length:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(
                    self._user_library_directory_name, 
                    'material_packages',
                    remainder,
                    )
            else:
                result = '.'.join([
                    self._user_library_directory_name,
                    'material_packages',
                    ])
            return result
        elif filesystem_path.startswith(
            self.user_library_material_managers_directory_path):
            return '.'.join([
                self._user_library_directory_name,
                'material_packages',
                os.path.basename(filesystem_path),
                ])
        elif filesystem_path.startswith(
            self.abjad_material_managers_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(
            self.abjad_material_packages_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif filesystem_path.startswith(self.score_manager_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_directory_path)) + 1
        elif filesystem_path.startswith(
            self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path) + 1
        elif filesystem_path.startswith(
            self.user_library_stylesheets_directory_path):
            prefix_length = \
                len(os.path.dirname(
                self.user_library_stylesheets_directory_path)) + 1
        elif filesystem_path.startswith(self.abjad_stylesheets_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        else:
            message = 'can not change filesystem path'
            message += ' to packagesystem path: {!r}.'
            raise Exception(message.format(filesystem_path))
        package_path = filesystem_path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')
        return package_path
