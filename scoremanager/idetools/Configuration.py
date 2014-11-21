# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.AbjadConfiguration import AbjadConfiguration


class Configuration(AbjadConfiguration):
    r'''Abjad IDE configuration.

    ..  container:: example

        ::

            >>> ide = scoremanager.idetools.AbjadIDE(is_test=True)
            >>> configuration = ide._configuration
            >>> configuration
            Configuration()

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
        current_time = self._current_time
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Abjad IDE configuration file created on {}.'.format(current_time),
            'This file is interpreted by ConfigObj and follows ini sytnax.',
        ]

    @property
    def _library_name(self):
        directory = self.library
        directory_name = os.path.split(directory)[-1]
        return directory_name

    ### PRIVATE METHODS ###

    def _get_option_definitions(self):
        #parent_options = AbjadConfiguration._get_option_definitions(self)
        options = {
            'composer_full_name': {
                'comment': [
                    '',
                    'Your full name.',
                ],
                'spec': "string(default='Full Name')",
            },
            'composer_last_name': {
                'comment': [
                    '',
                    'Your last name.',
                ],
                'spec': "string(default='Last Name')",
            },
            'composer_website': {
                'comment': [
                    '',
                    'Your website.',
                ],
                'spec': "string(default=None)",
            },
            'library': {
                'comment': [
                    '',
                    'The directory where you house score-external assets.',
                    'Defaults to $HOME/.abjad/library/.',
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.abjad_configuration_directory,
                        'library',
                        )
                    ),
            },
            'scores_directory': {
                'comment': [
                    '',
                    'The directory where you house your scores.',
                    'Defaults to $HOME/scores/.'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.home_directory,
                        'scores',
                        )
                    ),
            },
            'upper_case_composer_full_name': {
                'comment': [
                    '',
                    'Upper case version of your full name for score covers.',
                ],
                'spec': "string(default='Upper Case Full Name')",
            },
        }
        #parent_options.update(options)
        #return parent_options
        return options

    def _make_missing_directories(self):
        directories = (
            self.library,
            self.materials_library,
            self.makers_library,
            )
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                file_path = os.path.join(directory, '__init__.py')
                with open(file_path, 'w') as file_pointer:
                    file_pointer.write('')
        directories = (
            self.user_score_packages_directory,
            self.stylesheets_library,
            self.transcripts_directory,
            )
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def _path_to_score_path(self, path):
        if path.startswith(self.user_score_packages_directory):
            prefix = len(self.user_score_packages_directory)
        elif path.startswith(self.example_score_packages_directory):
            prefix = len(self.example_score_packages_directory)
        else:
            return
        path_prefix = path[:prefix]
        path_suffix = path[prefix+1:]
        score_name = path_suffix.split(os.path.sep)[0]
        score_path = os.path.join(path_prefix, score_name)
        return score_path

    def _path_to_storehouse(self, path):
        is_in_score = False
        if path.startswith(self.user_score_packages_directory):
            is_in_score = True
            prefix = len(self.user_score_packages_directory)
        elif path.startswith(self.example_score_packages_directory):
            is_in_score = True
            prefix = len(self.example_score_packages_directory)
        elif path.startswith(self.library):
            prefix = len(self.library)
        elif path.startswith(self.example_stylesheets_directory):
            return self.example_stylesheets_directory
        else:
            message = 'unidentifiable path: {!r}.'
            message = message.format(path)
            raise Exception(message)
        path_prefix = path[:prefix]
        remainder = path[prefix+1:]
        path_parts = remainder.split(os.path.sep)
        assert 1 <= len(path_parts)
        if is_in_score:
            path_parts = path_parts[:2]
        else:
            assert 1 <= len(path_parts)
            path_parts = path_parts[:1]
        storehouse_path = os.path.join(path_prefix, *path_parts)
        return storehouse_path

    def _path_to_storehouse_annotation(self, path):
        import scoremanager
        score_path = self._path_to_score_path(path)
        if score_path:
            session = scoremanager.idetools.Session
            manager = scoremanager.idetools.ScorePackageManager(
                path=score_path,
                session=session,
                )
            title = manager._get_title()
            return title
        elif path.startswith(self.library):
            return self.composer_last_name
        elif path.startswith(self.abjad_root_directory):
            return 'Abjad'
        else:
            message = 'path in unknown storehouse: {!r}.'
            message = message.format(path)
            raise ValueError(path)

    ### PUBLIC PROPERTIES ###

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
    def boilerplate_directory(self):
        r'''Gets boilerplate directory.

        ..  container:: example

            >>> configuration.boilerplate_directory
            '.../scoremanager/boilerplate'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory,
            'boilerplate',
            )
        return path

    @property
    def cache_file_path(self):
        r'''Gets cache file path.

        ..  container:: example

            ::

                >>> configuration.cache_file_path
                '.../.abjad/ide/cache.py'

        Returns string.
        '''
        file_path = self._cache_file_path = os.path.join(
            self.configuration_directory,
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
    def composer_website(self):
        r'''Gets composer website.

        ..  container:: example

            ::

                >>> configuration.composer_website  # doctest: +SKIP
                'My website address'

        Aliases `composer_website` setting in score manager configuration
        file.

        Returns string.
        '''
        return self._settings['composer_website']

    @property
    def configuration_directory(self):
        r'''Gets configuration directory.

        ..  container:: example

            ::

                >>> configuration.configuration_directory
                '.../.abjad/ide'

        Returns string.
        '''
        return os.path.join(self.abjad_configuration_directory, 'ide')

    @property
    def configuration_file_name(self):
        r'''Gets configuration file name.

        ..  container:: example

            ::

                >>> configuration.configuration_file_name
                'ide.cfg'

        Returns string.
        '''
        return 'ide.cfg'

    @property
    def configuration_file_path(self):
        r'''Gets configuration file path.

        ..  container:: example

            ::

                >>> configuration.configuration_file_path
                '.../.abjad/ide/ide.cfg'

        Returns string.
        '''
        return os.path.join(
            self.configuration_directory,
            self.configuration_file_name,
            )

    @property
    def example_score_packages_directory(self):
        r'''Gets Abjad score packages directory.

        ..  container:: example

            ::

                >>> configuration.example_score_packages_directory
                '.../scoremanager/scores'

        Returns string.
        '''
        path = os.path.join(
            self.score_manager_directory,
            'scores',
            )
        return path

    @property
    def example_stylesheets_directory(self):
        r'''Gets example stylesheets directory.

        ..  container:: example

            ::

                >>> configuration.example_stylesheets_directory
                '.../abjad/stylesheets'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_directory,
            'stylesheets',
            )
        return path

    @property
    def handler_tools_directory(self):
        r'''Gets handler tools directory.

        ..  container:: example

            ::

                >>> configuration.handler_tools_directory
                '.../tools/handlertools'

        Returns string.
        '''
        path = os.path.join(
            self.abjad_directory,
            'tools',
            'handlertools',
            )
        return path

    @property
    def home_directory(self):
        r'''Gets home directory.

        ..  container:: example

            ::

                >>> configuration.home_directory
                '...'

        Returns string.
        '''
        superclass = super(Configuration, self)
        return superclass.home_directory

    @property
    def library(self):
        r'''Gets library directory.

        ..  container:: example

            ::

                >>> configuration.library
                '...'

        Aliases `library` setting in score manager configuration
        file.

        Returns string.
        '''
        path = self._settings['library']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    @property
    def makers_library(self):
        r'''Gets makers library path.

        ..  container:: example

            ::

                >>> configuration.makers_library
                '.../makers'

        Returns string.
        '''
        path = os.path.join(
            self.library,
            'makers',
            )
        return path

    @property
    def materials_library(self):
        r'''Gets materials library path.

        ..  container:: example

            ::

                >>> configuration.materials_library
                '.../materials'

        Returns string.
        '''
        path = os.path.join(
            self.library,
            'materials',
            )
        return path

    @property
    def stylesheets_library(self):
        r'''Gets stylesheets library path.

        ..  container:: example

            ::

                >>> configuration.stylesheets_library
                '.../stylesheets'

        Returns string.
        '''
        path = os.path.join(
            self.library,
            'stylesheets',
            )
        return path

    @property
    def transcripts_directory(self):
        r'''Gets score manager transcripts directory.

        ..  container:: example

            ::

                >>> configuration.transcripts_directory
                '.../.abjad/ide/transcripts'

        Returns string.
        '''
        path = os.path.join(
            self.configuration_directory,
            'transcripts',
            )
        return path

    @property
    def unicode_directive(self):
        r'''Gets Unicode directive.

        ..  container:: example

            ::

                >>> configuration.unicode_directive
                '# -*- encoding: utf-8 -*-'

        Returns string.
        '''
        return '# -*- encoding: utf-8 -*-'

    @property
    def upper_case_composer_full_name(self):
        r'''Gets upper case composer full name.

        ..  container:: example

            ::

                >>> configuration.composer_full_name
                '...'

        Aliases `upper_case_composer_full_name` setting in score manager 
        configuration file.

        Returns string.
        '''
        return self._settings['upper_case_composer_full_name']

    @property
    def user_score_packages_directory(self):
        r'''Gets user score packages directory.

        ..  container:: example

            ::

                >>> configuration.user_score_packages_directory
                '...'

        Aliases `scores_directory` setting in score manager configuration file.

        Returns string.
        '''
        path = self._settings['scores_directory']
        path = os.path.expanduser(path)
        path = os.path.normpath(path)
        return path

    @property
    def wrangler_views_directory(self):
        r'''Gets wrangler views directory.

        ..  container::

            >>> configuration.wrangler_views_directory
            '.../views'

        Defined equal to views/ subdirectory of score manager directory.

        Returns string.
        '''
        return os.path.join(self.configuration_directory, 'views')

    @property
    def wrangler_views_metadata_file(self):
        r'''Gets wrangler views __metadata__.py file path.

        ..  container::

            >>> configuration.wrangler_views_metadata_file
            '.../ide/views/__metadata__.py'

        Defined equal to metadata file resident in the wrangler views
        directory.

        Returns string.
        '''
        return os.path.join(self.wrangler_views_directory, '__metadata__.py')

    ### PUBLIC METHODS ###

    def list_score_directories(
        self,
        abjad=False,
        user=False,
        ):
        r'''Lists score directories.

        ..  container:: example

            Lists Abjad score directories:

            ::

                >>> for x in configuration.list_score_directories(
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
            scores_directory = self.example_score_packages_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    directory = os.path.join(
                        scores_directory,
                        directory_entry,
                        )
                    path = os.path.join(
                        self.example_score_packages_directory,
                        directory_entry,
                        )
                    result.append(path)
        if user:
            scores_directory = self.user_score_packages_directory
            directory_entries = sorted(os.listdir(scores_directory))
            for directory_entry in directory_entries:
                if directory_entry[0].isalpha():
                    path = os.path.join(
                        self.user_score_packages_directory,
                        directory_entry,
                        )
                    result.append(path)
        return result

    def path_to_package(self, path):
        r'''Changes `path` to package.

        Returns string.
        '''
        if path is None:
            return
        assert isinstance(path, str), repr(path)
        path = os.path.normpath(path)
        if path.endswith('.py'):
            #path = path[:-3]
            path, extension = os.path.splitext(path)
        if path.startswith(self.example_score_packages_directory):
            prefix = len(self.example_score_packages_directory) + 1
        elif path.startswith(self.materials_library):
            prefix = len(self.materials_library) + 1
            remainder = path[prefix:]
            if remainder:
                remainder = remainder.replace(os.path.sep, '.')
                result = '{}.{}'.format(
                    self._library_name,
                    'material_packages',
                    remainder,
                    )
            else:
                result = '.'.join([
                    self._library_name,
                    'material_packages',
                    ])
            return result
        elif path.startswith(self.score_manager_directory):
            prefix = len(os.path.dirname(self.score_manager_directory)) + 1
        elif path.startswith(self.user_score_packages_directory):
            prefix = len(self.user_score_packages_directory) + 1
        elif path.startswith(self.stylesheets_library):
            prefix = len(
                os.path.dirname(self.stylesheets_library)) + 1
        elif path.startswith(self.example_stylesheets_directory):
            prefix = len(self.abjad_root_directory) + 1
        elif path.startswith(self.library):
            prefix = len(os.path.dirname(self.library)) + 1
        else:
            message = 'can not change path to package: {!r}.'
            raise Exception(message.format(path))
        package = path[prefix:]
        package = package.replace(os.path.sep, '.')
        return package