# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import traceback
from abjad.tools.systemtools.Configuration import Configuration


class AbjadConfiguration(Configuration):
    r'''Abjad configuration.

    ..  container:: example

        ::

            >>> abjad_configuration = systemtools.AbjadConfiguration()

        ::

            >>> abjad_configuration['accidental_spelling']
            'mixed'

    `AbjadConfiguration` creates the `$HOME/.abjad/` directory
    on instantiation.

    `AbjadConfiguration` then attempts to read an `abjad.cfg` file in
    that directory and parse the file as a `ConfigParser` configuration.

    `AbjadConfiguration` generates a default configuration if no file
    is found.

    `AbjadConfiguration` validates the `ConfigParser` instance
    and replaces key-value pairs which fail validation with default values.

    If the validated configuration differs from the original on disk,
    `AbjadConfiguration` writes the validated configuration back to disk.

    The Abjad output directory is created the from
    `abjad_output_directory` key if it does not already exist.

    `AbjadConfiguration` supports the mutable mapping interface
    and can be subscripted as a dictionary.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'System configuration'

    _lilypond_version_string = None  # For caching.

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.abjad_output_directory):
            try:
                os.makedirs(self.abjad_output_directory)
            except (IOError, OSError):
                traceback.print_exc()

    ### PRIVATE METHODS ###

    def _get_option_definitions(self):
        options = {
            'abjad_output_directory': {
                'comment': [
                    'Set to the directory where all Abjad-generated files',
                    '(such as PDFs and LilyPond files) should be saved.',
                    'Defaults to $HOME/.abjad/output/'
                    ],
                'default': os.path.join(
                    self.configuration_directory_path,
                    'output',
                    ),
                'validator': str,
                },
            'accidental_spelling': {
                'comment': [
                    'Default accidental spelling (mixed|sharps|flats).',
                    ],
                'default': 'mixed',
                'validator': lambda x: x in ('mixed', 'sharps', 'flats'),
                },
            'lilypond_path': {
                'comment': [
                    'Lilypond executable path. Set to override dynamic lookup.'
                    ],
                'default': 'lilypond',
                'validator': str,
                },
            'midi_player': {
                'comment': [
                    'MIDI player to open MIDI files.',
                    'When unset your OS should know how to open MIDI files.',
                    ],
                'default': None,
                'validator': str,
                },
            'pdf_viewer': {
                'comment': [
                    'PDF viewer to open PDF files.',
                    'When unset your OS should know how to open PDFs.',
                    ],
                'default': None,
                'validator': str,
                },
            'text_editor': {
                'comment': [
                    'Text editor to edit text files.',
                    'When unset your OS should know how to open text files.'
                    ],
                'default': None,
                'validator': str,
                },
            }
        return options

    ### PUBLIC METHODS ###

    @classmethod
    def get_abjad_startup_string(class_):
        r'''Gets Abjad startup string.

        ..  container:: example

            ::

                >>> abjad_configuration.get_abjad_startup_string()
                'Abjad 2.19 (development)'

        Returns string.
        '''
        result = 'Abjad {} ({})'
        result = result.format(
            class_.get_abjad_version_string(),
            'development',
            )
        return result

    @staticmethod
    def get_abjad_version_string():
        '''Gets Abjad version string.

        ..  container:: example

            ::

                >>> abjad_configuration.get_abjad_version_string()
                '2.19'

        Returns string.
        '''
        import abjad
        return abjad.__version__

    @classmethod
    def get_lilypond_minimum_version_string(class_):
        r'''Gets LilyPond minimum version string.

        ..  container:: example

            ::

                >>> abjad_configuration.get_lilypond_minimum_version_string() # doctest: +SKIP
                '2.17.0'

        Returns string.
        '''
        version = class_.get_lilypond_version_string()
        parts = version.split('.')[0:2]
        parts.append('0')
        return '.'.join(parts)

    @staticmethod
    def get_lilypond_version_string():
        '''Gets LilyPond version string.

        ..  container:: example

            ::

                >>> abjad_configuration.get_lilypond_version_string() # doctest: +SKIP
                '2.19.1'

        Returns string.
        '''
        from abjad import abjad_configuration
        from abjad.tools import systemtools
        if AbjadConfiguration._lilypond_version_string is not None:
            return AbjadConfiguration._lilypond_version_string
        lilypond = abjad_configuration.get('lilypond_path')
        if not lilypond:
            lilypond = systemtools.IOManager.find_executable('lilypond')
            if lilypond:
                lilypond = lilypond[0]
            else:
                lilypond = 'lilypond'
        command = lilypond + ' --version'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        if sys.version_info[0] == 2:
            lilypond_version_string = proc.stdout.readline()
        else:
            import locale
            encoding = locale.getdefaultlocale()[1]
            if encoding is None:
                encoding = 'utf-8'
            lilypond_version_string = proc.stdout.readline().decode(encoding)
        lilypond_version_string = lilypond_version_string.split(' ')[-1]
        lilypond_version_string = lilypond_version_string.strip()
        AbjadConfiguration._lilypond_version_string = lilypond_version_string
        return lilypond_version_string

    @staticmethod
    def get_python_version_string():
        '''Gets Python version string.

        ..  container:: example

            ::

                >>> abjad_configuration.get_python_version_string() # doctest: +SKIP
                '2.7.5'

        Returns string.
        '''
        return '.'.join(str(_) for _ in sys.version_info[:3])

    @staticmethod
    def get_tab_width():
        r'''Gets tab width.

        ..  container:: example

            ::

                >>> abjad_configuration.get_tab_width()
                4

        Used by code generation functions.

        Returns nonnegative integer.
        '''
        return 4

    @staticmethod
    def get_text_editor():
        r'''Gets text editor.

        ..  container:: example

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
    def list_package_dependency_versions():
        r'''Lists package dependency versions.

        ..  container:: example

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
        except (AttributeError, ImportError):
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
        '''Sets default accidental spelling.

        ..  container:: example

            Sets default accidental spelling to sharps:

            ::

                >>> abjad_configuration.set_default_accidental_spelling('sharps')

            ::

                >>> [Note(13, (1, 4)), Note(15, (1, 4))]
                [Note("cs''4"), Note("ds''4")]

        ..  container:: example

            Sets default accidental spelling to flats:

            ::

                >>> abjad_configuration.set_default_accidental_spelling('flats')

            ::

                >>> [Note(13, (1, 4)), Note(15, (1, 4))]
                [Note("df''4"), Note("ef''4")]

        ..  container:: example

            Sets default accidental spelling to mixed:

            ::

                >>> abjad_configuration.set_default_accidental_spelling()

            ::

                >>> [Note(13, (1, 4)), Note(15, (1, 4))]
                [Note("cs''4"), Note("ef''4")]

        Defaults to ``'mixed'``.

        Mixed test case must appear last here for doc tests to check correctly.

        Returns none.
        '''
        from abjad import abjad_configuration
        if spelling not in ('mixed', 'sharps', 'flats'):
            raise ValueError
        abjad_configuration['accidental_spelling'] = spelling

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        current_time = self._current_time
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Abjad configuration file created on {}.'.format(current_time),
            "This file is interpreted by Python's ConfigParser ",
            'and follows ini syntax.',
            ]

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_boilerplate_directory(self):
        r'''Gest Abjad boilerplate directory.

        Return string.
        '''
        relative_path = os.path.join(
            self.abjad_directory,
            'boilerplate',
            )
        return os.path.abspath(relative_path)

    @property
    def abjad_directory(self):
        r'''Gets Abjad directory.

        Returns string.
        '''
        import abjad
        return abjad.__path__[0]

    @property
    def abjad_experimental_directory(self):
        r'''Gets Abjad experimental directory.

        Returns string.
        '''
        relative_path = os.path.join(
            self.abjad_root_directory,
            'experimental',
            )
        return os.path.abspath(relative_path)

    @property
    def abjad_output_directory(self):
        r'''Gets Abjad output directory.

        Returns string.
        '''
        if 'abjad_output_directory' in self._settings:
            return self._settings['abjad_output_directory']
        return os.path.join(
            self.configuration_directory_path,
            'output'
            )

    @property
    def abjad_root_directory(self):
        r'''Gets Abjad root directory.

        Returns string.
        '''
        relative_path = os.path.join(
            self.abjad_directory,
            '..',
            )
        return os.path.abspath(relative_path)

    @property
    def configuration_directory_name(self):
        r'''Gets configuration directory name.

        Returns string.
        '''
        return '.abjad'

    @property
    def configuration_file_name(self):
        r'''Gets configuration file name.

        Returns string.
        '''
        return 'abjad.cfg'

    @property
    def lilypond_log_file_path(self):
        r'''Gets LilyPond log file path.

        Returns string.
        '''
        return os.path.join(self.abjad_output_directory, 'lily.log')
