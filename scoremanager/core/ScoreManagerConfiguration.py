# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class ScoreManagerConfiguration(AbjadConfiguration):
    r'''Score manager configuration.

    ..  container:: example

        ::

            >>> score_manager = scoremanager.core.ScoreManager(is_test=True)
            >>> configuration = score_manager._configuration
            >>> configuration
            ScoreManagerConfiguration()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cache_file_path',
        )

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
                    ),
            },
            'composer_full_name': {
                'comment': [
                    '',
                    'Set to full name of composer.',
                ],
                'spec': "string(default='Full Name')",
            },
            'composer_last_name': {
                'comment': [
                    '',
                    'Set to last name of composer.',
                ],
                'spec': "string(default='Name')",
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
            self.user_library_material_packages_directory_path,
            self.user_library_makers_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                file_path = os.path.join(directory_path, '__init__.py')
                with file(file_path, 'w') as file_pointer:
                    file_pointer.write('')
        directory_paths = (
            self.user_score_packages_directory_path,
            self.user_library_stylesheets_directory_path,
            self.transcripts_directory_path,
            )
        for directory_path in directory_paths:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

    def _path_to_score_path(self, path):
        if path.startswith(self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path)
        elif path.startswith(self.example_score_packages_directory_path):
            prefix_length = len(self.example_score_packages_directory_path)
        else:
            return
        path_prefix = path[:prefix_length]
        path_suffix = path[prefix_length+1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        return score_path

    def _path_to_storehouse_annotation(self, path):
        import scoremanager
        score_path = self._path_to_score_path(path)
        if score_path:
            session = scoremanager.core.Session
            manager = scoremanager.managers.ScorePackageManager(
                path=score_path,
                session=session,
                )
            title = manager._get_title()
            return title
        elif path.startswith(self.user_library_directory_path):
            return self.composer_last_name
        elif path.startswith(self.abjad_root_directory_path):
            return 'Abjad'
        else:
            message = 'path in unknown storehouse: {!r}.'
            message = message.format(path)
            raise ValueError(path)

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_makers_directory_path(self):
        r'''Gets Abjad makers directory path.

        ..  container:: example

            ::

                >>> configuration.abjad_makers_directory_path
                '.../scoremanager/makers'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory_path,
            'makers',
            )
        return path

    @property
    def abjad_material_packages_directory_path(self):
        r'''Gets Abjad material packages directory path.

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
        r'''Gets Abjad score package names.

        ..  container:: example

            ::

                >>> for x in configuration.abjad_score_package_names:
                ...     x
                'blue_example_score'
                'etude_example_score'
                'red_example_score'

        Returns tuple of strings.
        '''
        return (
            'blue_example_score',
            'etude_example_score',
            'red_example_score',
            )

    @property
    def example_score_packages_directory_path(self):
        r'''Gets Abjad score packages directory path.

        ..  container:: example

            ::

                >>> configuration.example_score_packages_directory_path
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
        r'''Gets Abjad stylesheets directory path.

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
    def composer_full_name(self):
        r'''Gets composer full name.

        ..  container:: example

            ::

                >>> configuration.composer_full_name
                '...'

        Aliases `composer` setting in score manager configuration
        file.

        Returns string.
        '''
        return self._settings['composer_full_name']

    @property
    def composer_last_name(self):
        r'''Gets composer last name.

        ..  container:: example

            ::

                >>> configuration.composer_last_name
                '...'

        Aliases `composer` setting in score manager configuration
        file.

        Returns string.
        '''
        return self._settings['composer_last_name']

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
    def user_library_makers_directory_path(self):
        r'''Gets user library makers path.

        ..  container:: example

            ::

                >>> configuration.user_library_makers_directory_path
                '.../makers'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'makers',
            )
        return path

    @property
    def user_library_material_packages_directory_path(self):
        r'''Gets user library material packages directory path.

        ..  container:: example

            ::

                >>> configuration.user_library_material_packages_directory_path
                '.../materials'

        Returns string.
        '''
        path = os.path.join(
            self.user_library_directory_path,
            'materials',
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
        ):
        r'''Lists score directory paths.

        ..  container:: example

            Lists Abjad score directory paths:

            ::

                >>> for x in configuration.list_score_directory_paths(
                ...     abjad=True,
                ...     ):
                ...     x
                '.../scoremanager/scores/blue_example_score'
                '.../scoremanager/scores/etude_example_score'
                '.../scoremanager/scores/red_example_score'

        Returns list.
        '''
        result = []
        if abjad:
            scores_directory_path = self.example_score_packages_directory_path
            directory_entries = sorted(os.listdir(scores_directory_path))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    directory_path = os.path.join(
                        scores_directory_path,
                        directory_entry,
                        )
                    package_path = self.path_to_package_path(
                        directory_path,
                        )
                    path = os.path.join(
                        self.example_score_packages_directory_path,
                        directory_entry,
                        )
                    result.append(path)
        if user:
            scores_directory_path = self.user_score_packages_directory_path
            directory_entries = sorted(os.listdir(scores_directory_path))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    package_path = directory_entry
                    path = os.path.join(
                        self.user_score_packages_directory_path,
                        directory_entry,
                        )
                    result.append(path)
        return result

    def path_to_package_path(self, path):
        r'''Changes `path` to package path.

        Returns string.
        '''
        if path is None:
            return
        assert isinstance(path, str), repr(path)
        path = os.path.normpath(path)
        if path.endswith('.py'):
            path = path[:-3]
        if path.startswith(
            self.example_score_packages_directory_path):
            prefix_length = len(self.example_score_packages_directory_path) + 1
        elif path.startswith(
            self.user_library_material_packages_directory_path):
            prefix_length = \
                len(self.user_library_material_packages_directory_path) + 1
            remainder = path[prefix_length:]
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
        elif path.startswith(
            self.abjad_material_packages_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        elif path.startswith(self.score_manager_directory_path):
            prefix_length = \
                len(os.path.dirname(self.score_manager_directory_path)) + 1
        elif path.startswith(
            self.user_score_packages_directory_path):
            prefix_length = len(self.user_score_packages_directory_path) + 1
        elif path.startswith(
            self.user_library_stylesheets_directory_path):
            prefix_length = \
                len(os.path.dirname(
                self.user_library_stylesheets_directory_path)) + 1
        elif path.startswith(self.abjad_stylesheets_directory_path):
            prefix_length = len(self.abjad_root_directory_path) + 1
        else:
            message = 'can not change path to package path: {!r}.'
            raise Exception(message.format(path))
        package_path = path[prefix_length:]
        package_path = package_path.replace(os.path.sep, '.')
        return package_path