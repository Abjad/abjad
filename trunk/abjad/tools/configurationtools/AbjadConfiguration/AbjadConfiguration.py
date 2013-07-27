import os
import subprocess
import types
from abjad.tools.configurationtools.Configuration import Configuration


class AbjadConfiguration(Configuration):
    '''Abjad configuration object:

    ::

        >>> ABJCONFIG = configurationtools.AbjadConfiguration()
        >>> ABJCONFIG['accidental_spelling']
        'mixed'

    `AbjadConfiguration` creates the `$home/.abjad/` directory 
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
            '-*- coding: utf-8 -*-',
            '',
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
                    'Defaults to $home/.abjad/output/'
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

    @staticmethod
    def get_abjad_revision_string():
        '''.. versionadded:: 2.0

        Get Abjad revision string:

        ::

            >>> configurationtools.AbjadConfiguration.get_abjad_revision_string() # doctest: +SKIP
            '11266'

        Return string.
        '''
        from abjad import abjad_configuration
        command = 'svnversion {}'.format(abjad_configuration.abjad_directory_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.stdout.readlines()[0].strip().strip('M')

    @classmethod
    def get_abjad_startup_string(cls):
        return 'Abjad {} (r{})'.format(
            cls.get_abjad_version_string(),
            cls.get_abjad_revision_string(),
            )

    @staticmethod
    def get_abjad_version_string():
        '''.. versionadded:: 2.0

        Get Abjad version string:

        ::

            >>> configurationtools.AbjadConfiguration.get_abjad_version_string()
            '2.13'

        Return string.
        '''
        import abjad
        return abjad.__version__

    @classmethod
    def get_lilypond_minimum_version_string(cls):
        '''Get the x.x.0 version of LilyPond:

        ::

            >>> configurationtools.AbjadConfiguration.get_lilypond_minimum_version_string()
            '2.17.0'

        This is useful for documentation purposes, where all developers are
        using the development version of LilyPond, but not necessarily the exact
        same version.

        Return string.
        '''
        version = cls.get_lilypond_version_string()
        parts = version.split('.')[0:2]
        parts.append('0')
        return '.'.join(parts)

    @staticmethod
    def get_lilypond_version_string():
        '''.. versionadded:: 2.0

        Get LilyPond version string:

        ::

            >>> configurationtools.AbjadConfiguration.get_lilypond_version_string() # doctest: +SKIP
            '2.13.61'

        Return string.
        '''
        from abjad import abjad_configuration
        if subprocess.mswindows and not 'LilyPond' in os.environ.get('PATH'):
            command = r'dir "C:\Program Files\*.exe" /s /b | find "lilypond.exe"'
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            lilypond = proc.stdout.readline()
            lilypond = lilypond.strip('\r').strip('\n').strip()
            if lilypond == '':
                raise SystemError('Cannot find LilyPond under Windows.')
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
        '''.. versionadded:: 2.0

        Get Python version string:

        ::

            >>> configurationtools.AbjadConfiguration.get_python_version_string() # doctest: +SKIP
            '2.6.1'

        Return string.
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
        r'''.. versionadded:: 2.9

        Get system tab width:

        ::

            >>> configurationtools.AbjadConfiguration.get_tab_width()
            4

        The value is used by various functions that generate or test code in the system.

        Return nonnegative integer.
        '''
        return 4

    @staticmethod
    def get_text_editor():
        '''Get OS-appropriate text editor.
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
        '''List Abjad environment variables.

        Return tuple of zero or more environment variable / setting pairs.

        Abjad environment variables are defined in
        ``abjad/tools/configurationtools/AbjadConfiguration/AbjadConfiguration.py``.
        '''
        from abjad import abjad_configuration
        result = []
        for key in dir(abjad_configuration):
            if key.isupper() and not key.startswith('_'):
                result.append((key, getattr(abjad_configuration, key)))
        return tuple(result)

    @staticmethod
    def list_package_dependency_versions():
        r'''List package dependency versions:

        ::

            >>> configurationtools.AbjadConfiguration.list_package_dependency_versions() # doctest: +SKIP
            {'sphinx': '1.1.2', 'py.test': '2.1.2'}

        Return dictionary.
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
        dependencies['py.test'] = None
        try:
            import py.test
            dependencies['py.test'] = py.test.__version__
        except ImportError:
            pass
        dependencies['sphinx'] = None
        try:
            import sphinx
            dependencies['sphinx'] = sphinx.__version__
        except ImportError:
            pass
        return dependencies
        
    ### PUBLIC PROPERTIES ###

    @property
    def abjad_configuration_directory_path(self):
        return os.path.join(self.home_directory_path, '.abjad')

    @property
    def abjad_configuration_file_path(self):
        return self.configuration_file_path

    @property
    def abjad_directory_path(self):
        module_parts = self.__module__.split('.')
        filepath_parts = os.path.abspath(__file__).rpartition('.py')
        filepath_parts = filepath_parts[0].split(os.path.sep)
        for part in reversed(module_parts):
            if part == 'abjad':
                break
            filepath_parts.pop()
        return os.path.sep.join(filepath_parts)

    @property
    def abjad_experimental_directory_path(self):
        return os.path.abspath(os.path.join(
            self.abjad_directory_path, '..', '..', 'experimental'))

    @property
    def abjad_output_directory_path(self):
        return self._settings['abjad_output']

    @property
    def abjad_root_directory_path(self):
        return os.path.abspath(os.path.join(
            self.abjad_directory_path, '..', '..'))

    @property
    def configuration_directory_path(self):
        return self.abjad_configuration_directory_path

    @property
    def configuration_file_name(self):
        return 'abjad.cfg'

