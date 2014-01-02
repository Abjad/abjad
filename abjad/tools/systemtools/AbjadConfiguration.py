# -*- encoding: utf-8 -*-
import os
import subprocess
import types
from abjad.tools.systemtools.Configuration import Configuration


class AbjadConfiguration(Configuration):
    r'''Abjad configuration.

    ::

        >>> ABJCONFIG = systemtools.AbjadConfiguration()
        >>> ABJCONFIG['accidental_spelling']
        'mixed'

    ::

        >>> configuration = systemtools.AbjadConfiguration()

    `AbjadConfiguration` creates the `$HOME/.abjad/` directory
    on instantiation.

    `AbjadConfiguration` then attempts to read an `abjad.cfg` file in
    that directory and parse the file as a `ConfigObj` configuration.
    `AbjadConfiguration` generates a default configuration if no file
    is found.

    `AbjadConfiguration` validates the `ConfigObj` instance
    and replaces key-value pairs which fail validation with default values.
    `AbjadConfiguration` then writes the configuration back to disk.

    The Abjad output directory is created the from `abjad_output` key
    if it does not already exist.

    `AbjadConfiguration` supports the mutable mapping interface
    and can be subscripted as a dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        # verify the PDF output directory
        if not os.path.exists(self.abjad_output_directory_path):
            os.mkdir(self.abjad_output_directory_path)

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            'Abjad configuration file created by Abjad on {}.'.format(
                self._current_time),
            'File is interpreted by ConfigObj and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            # TODO: change name to 'abjad_output_directory_path'
            'abjad_output': {
                'comment': [
                    '',
                    'Set to the directory where all Abjad-generated files',
                    '(such as PDFs and LilyPond files) should be saved.',
                    'Defaults to $HOME/.abjad/output/'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.abjad_configuration_directory_path, 'output'))
            },
            'accidental_spelling': {
                'comment': [
                    '',
                    'Default accidental spelling (mixed|sharps|flats).',
                ],
                'spec': "option('mixed', 'sharps', 'flats', default='mixed')"
            },
            'lilypond_includes': {
                'comment': [
                    '',
                    'Comma-separated list of LilyPond files that ',
                    'Abjad will "\include" in all generated *.ly files',
                ],
                'spec': 'list(min=0, default=list())'
            },
            'lilypond_language': {
                'comment': [
                    '',
                    'Language to use in all generated LilyPond files.'
                ],
                'spec': "string(default='english')"
            },
            'lilypond_path': {
                'comment': [
                    '',
                    'Lilypond executable path. Set to override dynamic lookup.'
                ],
                'spec': "string(default='lilypond')"
            },
            'midi_player': {
                'comment': [
                    '',
                    'MIDI player to open MIDI files.',
                    'When unset your OS should know how to open MIDI files.',
                ],
                'spec': "string(default='')"
            },
            'pdf_viewer': {
                'comment': [
                    '',
                    'PDF viewer to open PDF files.',
                    'When unset your OS should know how to open PDFs.',
                ],
                'spec': "string(default='')"
            },
            'text_editor': {
                'comment': [
                    '',
                    'Text editor to edit text files.',
                    'When unset your OS should know how to open text files.'
                ],
                'spec': "string(default='')"
            },

        }
        return options

    ### PUBLIC METHODS ###

    @classmethod
    def get_abjad_startup_string(cls):
        r'''Gets Abjad startup string.

        ::

            >>> abjad_configuration.get_abjad_startup_string()
            'Abjad 2.15 (development)'

        Returns string.
        '''
        result = 'Abjad {} ({})'
        result = result.format(
            cls.get_abjad_version_string(),
            'development',
            )
        return result

    @staticmethod
    def get_abjad_version_string():
        '''Gets Abjad version string.

        ::

            >>> abjad_configuration.get_abjad_version_string()
            '2.15'

        Returns string.
        '''
        import abjad
        return abjad.__version__

    @classmethod
    def get_lilypond_minimum_version_string(cls):
        r'''Gets LilyPond minimum version string.

        ::

            >>> abjad_configuration.get_lilypond_minimum_version_string() # doctest: +SKIP
            '2.17.0'

        This is useful for documentation purposes, where all developers are
        using the development version of LilyPond, but not necessarily
        the exact same version.

        Returns string.
        '''
        version = cls.get_lilypond_version_string()
        parts = version.split('.')[0:2]
        parts.append('0')
        return '.'.join(parts)

    @staticmethod
    def get_lilypond_version_string():
        '''Gets LilyPond version string:

        ::

            >>> abjad_configuration.get_lilypond_version_string() # doctest: +SKIP
            '2.17.28'

        Returns string.
        '''
        from abjad import abjad_configuration
        if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
            command = r'dir "C:\Program Files\*.exe" /s /b | find "lilypond.exe"'
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            lilypond = proc.stdout.readline()
            lilypond = lilypond.strip('\r').strip('\n').strip()
            if lilypond == '':
                message = 'can not find LilyPond under Windows.'
                raise SystemError(message)
        else:
            lilypond = abjad_configuration['lilypond_path']
            if not lilypond:
                lilypond = 'lilypond'
        command = lilypond + ' --version'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lilypond_version_string = proc.stdout.readline()
        lilypond_version_string = lilypond_version_string.split(' ')[-1]
        lilypond_version_string = lilypond_version_string.strip()
        return lilypond_version_string

    @staticmethod
    def get_python_version_string():
        '''Gets Python version string.

        ::

            >>> abjad_configuration.get_python_version_string() # doctest: +SKIP
            '2.7.5'

        Returns string.
        '''
        # python prints to stderr on startup (instead of stdout)
        command = 'python --version'
        proc = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
        python_version_string = proc.stderr.readline()
        # massage output string
        python_version_string = python_version_string.split(' ')[-1]
        python_version_string = python_version_string.strip()
        # return trimmed string
        return python_version_string

    @staticmethod
    def get_tab_width():
        r'''Gets tab width.

        ::

            >>> abjad_configuration.get_tab_width()
            4

        The value is used by various functions that generate or
        test code in the system.

        Returns nonnegative integer.
        '''
        return 4

    @staticmethod
    def get_text_editor():
        r'''Get text editor.

        ::

            >>> abjad_configuration.get_text_editor() # doctest: +SKIP
            'vim'

        Returns string.
        '''
        from abjad import abjad_configuration
        text_editor = abjad_configuration['text_editor']
        if text_editor is not None:
            return text_editor
        elif os.name == 'posix':
            return 'vim'
        else:
            return 'edit'

    @staticmethod
    def list_abjad_environment_variables():
        r'''Lists Abjad environment variables.

        ::

            >>> for x in abjad_configuration.list_abjad_environment_variables():
            ...     x


        Abjad environment variables are defined in
        ``abjad/tools/abjad_configuration/AbjadConfiguration.py``.

        Returns tuple of zero or more environment variable / setting pairs.
        '''
        from abjad import abjad_configuration
        result = []
        for key in dir(abjad_configuration):
            if key.isupper() and not key.startswith('_'):
                result.append((key, getattr(abjad_configuration, key)))
        return tuple(result)

    @staticmethod
    def list_package_dependency_versions():
        r'''Lists package dependency versions.

        ::

            >>> abjad_configuration.list_package_dependency_versions() # doctest: +SKIP
            {'sphinx': '1.1.2', 'pytest': '2.1.2'}

        Returns dictionary.
        '''
        dependencies = {}
        dependencies['configobj'] = None
        try:
            import configobj
            dependencies['configobj'] = configobj.__version__
        except ImportError:
            pass
        dependencies['ply'] = None
        try:
            from ply import lex
            dependencies['ply'] = lex.__version__
        except ImportError:
            pass
        dependencies['pytest'] = None
        try:
            import pytest
            dependencies['pytest'] = pytest.__version__
        except ImportError:
            pass
        dependencies['sphinx'] = None
        try:
            import sphinx
            dependencies['sphinx'] = sphinx.__version__
        except ImportError:
            pass
        return dependencies

    @staticmethod
    def set_default_accidental_spelling(spelling='mixed'):
        '''Set default accidental spelling to sharps:

        ::

            >>> abjad_configuration.set_default_accidental_spelling('sharps')

        ::

            >>> [Note(13, (1, 4)), Note(15, (1, 4))]
            [Note("cs''4"), Note("ds''4")]

        Set default accidental spelling to flats:

        ::

            >>> abjad_configuration.set_default_accidental_spelling('flats')

        ::

            >>> [Note(13, (1, 4)), Note(15, (1, 4))]
            [Note("df''4"), Note("ef''4")]

        Set default accidental spelling to mixed:

        ::

            >>> abjad_configuration.set_default_accidental_spelling()

        ::

            >>> [Note(13, (1, 4)), Note(15, (1, 4))]
            [Note("cs''4"), Note("ef''4")]

        Mixed is system default.

        Mixed test case must appear last here for doc tests to check correctly.

        Returns none.
        '''
        from abjad import abjad_configuration
        if spelling not in ('mixed', 'sharps', 'flats'):
            raise ValueError
        abjad_configuration['accidental_spelling'] = spelling

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_configuration_directory_path(self):
        r'''Abjad configuration directory path.

        Returns string.
        '''
        return os.path.join(self.home_directory_path, '.abjad')

    @property
    def abjad_configuration_file_path(self):
        r'''Abjad configuration file path.

        Returns string.
        '''
        return self.configuration_file_path

    @property
    def abjad_directory_path(self):
        r'''Abjad directory path.

        Returns string.
        '''
        module_parts = self.__module__.split('.')
        file_path_parts = os.path.abspath(__file__).rpartition('.py')
        file_path_parts = file_path_parts[0].split(os.path.sep)
        for part in reversed(module_parts):
            if part == 'abjad':
                break
            file_path_parts.pop()
        return os.path.sep.join(file_path_parts)

    @property
    def abjad_experimental_directory_path(self):
        r'''Abjad experimental directory path.

        Returns string.
        '''
        return os.path.abspath(os.path.join(
            self.abjad_root_directory_path,
            'experimental',
            ))

    @property
    def abjad_output_directory_path(self):
        r'''Abjad output directory path.

        Returns string.
        '''
        return self._settings['abjad_output']

    @property
    def abjad_root_directory_path(self):
        r'''Abjad root directory path.

        Returns string.
        '''
        return os.path.abspath(os.path.join(
            self.abjad_directory_path,
            '..',
            ))

    @property
    def configuration_directory_path(self):
        r'''Configuration directory path.

        Returns string.
        '''
        return self.abjad_configuration_directory_path

    @property
    def configuration_file_name(self):
        r'''Configuration file name.

        Returns string.
        '''
        return 'abjad.cfg'
