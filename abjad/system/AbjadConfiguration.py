import importlib
import os
import subprocess
import sys
import traceback
from abjad.system.Configuration import Configuration


class AbjadConfiguration(Configuration):
    """
    Abjad configuration.

    ..  container:: example

        >>> abjad_configuration = abjad.AbjadConfiguration()

    ..  container:: example

        Behavior at instantiation:

        * Looks for ``$HOME/.abjad/``.

        * Creates ``$HOME/.abjad/`` if directory does not exist.

        * Looks for ``$HOME/.abjad/abjad.cfg``.

        * Creates ``$HOME/.abjad/abjad.cfg`` if file does not exist.

        * Parses ``$HOME/.abjad/abjad.cfg``.

        * Provides default key-value pairs for pairs which fail validation.

        * Writes configuration changes to disk.

        * Creates Abjad output directory if directory does not exist.

    Supports mutable mapping dictionary interface.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'System configuration'

    __slots__ = (
        '_composer_library_tools',
        )

    _configuration_directory_name = '.abjad'

    _configuration_file_name = 'abjad.cfg'

    # for caching
    _lilypond_version_string = None

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        if not os.path.exists(self.abjad_output_directory):
            try:
                os.makedirs(self.abjad_output_directory)
            except (IOError, OSError):
                traceback.print_exc()
        self._composer_library_tools = None

    ### PRIVATE METHODS ###

    def _get_initial_comment(self):
        current_time = self._get_current_time()
        return [
            'Abjad configuration file created on {}.'.format(current_time),
            "This file is interpreted by Python's ConfigParser ",
            'and follows ini syntax.',
            ]

    def _get_option_definitions(self):
        options = {
            'abjad_output_directory': {
                'comment': [
                    'Set to the directory where all Abjad-generated files',
                    '(such as PDFs and LilyPond files) should be saved.',
                    'Defaults to $HOME/.abjad/output/'
                    ],
                'default': os.path.join(
                    str(self.configuration_directory),
                    'output',
                    ),
                'validator': str,
                },
            'composer_email': {
                'comment': ['Your email.'],
                'default': 'first.last@domain.com',
                'validator': str,
                },
            'composer_full_name': {
                'comment': ['Your full name.'],
                'default': 'Full Name',
                'validator': str,
                },
            'composer_github_username': {
                'comment': ['Your GitHub username.'],
                'default': 'username',
                'validator': str,
                },
            'composer_last_name': {
                'comment': ['Your last name.'],
                'default': 'Name',
                'validator': str,
                },
            'composer_library': {
                'comment': ['Your library.'],
                'default': 'my_library',
                'validator': str,
                },
            'composer_scores_directory': {
                'comment': ['Your scores directory.'],
                'default': str(self.home_directory / 'scores'),
                'validator': str,
                },
            'composer_uppercase_name': {
                'comment': ['Your full name in uppercase for score covers.'],
                'default': 'FULL NAME',
                'validator': str,
                },
            'composer_website': {
                'comment': ['Your website.'],
                'default': 'www.composername.com',
                'validator': str,
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

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_directory(self):
        """
        Gets Abjad directory.

        Returns string.
        """
        import abjad
        return abjad.__path__[0]

    @property
    def abjad_output_directory(self):
        """
        Gets Abjad output directory.

        Returns string.
        """
        if 'abjad_output_directory' in self._settings:
            return self._settings['abjad_output_directory']
        return os.path.join(
            self.configuration_directory,
            'output'
            )

    @property
    def abjad_root_directory(self):
        """
        Gets Abjad root directory.

        Returns string.
        """
        relative_path = os.path.join(
            self.abjad_directory,
            '..',
            )
        return os.path.abspath(relative_path)

    @property
    def boilerplate_directory(self):
        """
        Gets Abjad boilerplate directory.

        Return string.
        """
        relative_path = os.path.join(
            self.abjad_directory,
            'boilerplate',
            )
        return os.path.abspath(relative_path)

    @property
    def composer_email(self):
        """
        Gets composer email.

        Returns string.
        """
        return self._settings['composer_email']

    @property
    def composer_full_name(self):
        """
        Gets composer full name.

        Returns string.
        """
        return self._settings['composer_full_name']

    @property
    def composer_github_username(self):
        """
        Gets GitHub username.

        Returns string.
        """
        return self._settings['composer_github_username']

    @property
    def composer_last_name(self):
        """
        Gets composer last name.

        Returns string.
        """
        return self._settings['composer_last_name']

    @property
    def composer_library(self):
        """
        Gets composer library package name.

        Returns string.
        """
        return self._settings['composer_library']

    @property
    def composer_library_tools(self):
        """
        Gets composer library tools directory.

        Returns string.
        """
        if self._composer_library_tools is None:
            name = self.composer_library
            if not name:
                return
            try:
                path = importlib.import_module(name)
            except ImportError:
                path = None
            if not path:
                return
            #path = os.path.join(path.__path__[0], 'tools')
            path = path.__path__[0]
            self._composer_library_tools = path
        return self._composer_library_tools

    @property
    def composer_scores_directory(self):
        """
        Gets composer scores directory.

        Returns string.
        """
        if 'composer_scores_directory' in self._settings:
            return self._settings['composer_scores_directory']
        return os.path.join(self.home_directory, 'scores')

    @property
    def composer_uppercase_name(self):
        """
        Gets composer uppercase name.

        ..  container:: example

            >>> configuration.composer_uppercase_name # doctest: +SKIP
            'TREVOR BAČA'

        Returns string.
        """
        return self._settings['composer_uppercase_name']

    @property
    def composer_website(self):
        """
        Gets composer website.

        ..  container:: example

            >>> configuration.composer_website  # doctest: +SKIP
            'www.trevobaca.com'

        Returns string.
        """
        return self._settings['composer_website']

    @property
    def lilypond_log_file_path(self):
        """
        Gets LilyPond log file path.

        Returns string.
        """
        return os.path.join(self.abjad_output_directory, 'lily.log')

    ### PUBLIC METHODS ###

    @classmethod
    def get_abjad_startup_string(class_):
        """
        Gets Abjad startup string.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_abjad_startup_string()
            'Abjad 3.0.0 (development)'

        Returns string.
        """
        result = 'Abjad {} ({})'
        result = result.format(
            class_.get_abjad_version_string(),
            'development',
            )
        return result

    @staticmethod
    def get_abjad_version_string():
        """
        Gets Abjad version string.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_abjad_version_string()
            '3.0.0'

        Returns string.
        """
        import abjad
        return abjad.__version__

    @classmethod
    def get_lilypond_minimum_version_string(class_):
        """
        Gets LilyPond minimum version string.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_lilypond_minimum_version_string() # doctest: +SKIP
            '2.19.0'

        Returns string.
        """
        version = class_.get_lilypond_version_string()
        parts = version.split('.')[0:2]
        parts.append('0')
        return '.'.join(parts)

    @staticmethod
    def get_lilypond_version_string():
        """
        Gets LilyPond version string.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_lilypond_version_string() # doctest: +SKIP
            '2.19.82'

        Returns string.
        """
        from abjad import abjad_configuration
        from abjad import system
        if AbjadConfiguration._lilypond_version_string is not None:
            return AbjadConfiguration._lilypond_version_string
        lilypond = abjad_configuration.get('lilypond_path')
        if not lilypond:
            lilypond = system.IOManager.find_executable('lilypond')
            if lilypond:
                lilypond = lilypond[0]
            else:
                lilypond = 'lilypond'
        command = lilypond + ' --version'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lilypond_version_string = proc.stdout.readline().decode()
        lilypond_version_string = lilypond_version_string.split(' ')[-1]
        lilypond_version_string = lilypond_version_string.strip()
        AbjadConfiguration._lilypond_version_string = lilypond_version_string
        return lilypond_version_string

    @staticmethod
    def get_python_version_string():
        """
        Gets Python version string.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_python_version_string() # doctest: +SKIP
            '3.6.4'

        Returns string.
        """
        return '.'.join(str(_) for _ in sys.version_info[:3])

    @staticmethod
    def get_tab_width():
        """
        Gets tab width.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_tab_width()
            4

        Used by code generation functions.

        Returns nonnegative integer.
        """
        return 4

    @staticmethod
    def get_text_editor():
        """
        Gets text editor.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.get_text_editor() # doctest: +SKIP
            'vi'

        Returns string.
        """
        from abjad import abjad_configuration
        text_editor = abjad_configuration['text_editor']
        if text_editor is not None:
            return text_editor
        elif os.name == 'posix':
            return 'vi'
        else:
            return 'edit'

    @staticmethod
    def list_package_dependency_versions():
        """
        Lists package dependency versions.

        ..  container:: example

            >>> abjad_configuration = abjad.AbjadConfiguration()
            >>> abjad_configuration.list_package_dependency_versions() # doctest: +SKIP
            {'sphinx': '1.1.2', 'pytest': '2.1.2'}

        Returns dictionary.
        """
        dependencies = {}
        dependencies['configobj'] = None
        try:
            import configobj  # type: ignore
            dependencies['configobj'] = configobj.__version__
        except (AttributeError, ImportError):
            pass
        dependencies['ply'] = None
        try:
            from ply import lex  # type: ignore
            dependencies['ply'] = lex.__version__
        except ImportError:
            pass
        dependencies['pytest'] = None
        try:
            import pytest  # type: ignore
            dependencies['pytest'] = pytest.__version__
        except ImportError:
            pass
        dependencies['sphinx'] = None
        try:
            import sphinx  # type: ignore
            dependencies['sphinx'] = sphinx.__version__
        except ImportError:
            pass
        return dependencies
