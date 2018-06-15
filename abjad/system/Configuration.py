import abc
import os
import pathlib
import six
import tempfile
import time
import traceback
from abjad.system.AbjadObject import AbjadObject
from six.moves import StringIO
from six.moves import configparser


class Configuration(AbjadObject):
    """
    Configuration.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'System configuration'

    __slots__ = (
        '_cached_configuration_directory',
        '_settings',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._cached_configuration_directory = None
        if not os.path.exists(str(self.configuration_directory)):
            try:
                os.makedirs(str(self.configuration_directory))
            except (IOError, OSError):
                traceback.print_exc()
        old_contents = ''
        if self.configuration_file_path.exists():
            try:
                old_contents = self.configuration_file_path.read_text()
            except AttributeError:
                with self.configuration_file_path.open(mode='r') as f:
                    old_contents = f.read()
        configuration = self._configuration_from_string(old_contents)
        configuration = self._validate_configuration(configuration)
        new_contents = self._configuration_to_string(configuration)
        if not self._compare_configurations(old_contents, new_contents):
            try:
                #self.configuration_file_path.write_text(new_contents)
                with open(str(self.configuration_file_path), 'w') as file_pointer:
                    file_pointer.write(new_contents)
            except (IOError, OSError):
                traceback.print_exc()
        self._settings = configuration

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        """
        Deletes item ``i`` from configuration.

        Returns none.
        """
        del(self._settings[i])

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        Returns item or slice.
        """
        return self._settings.__getitem__(argument)

    def __iter__(self):
        """
        Iterates configuration settings.

        Returns generator.
        """
        for key in self._settings:
            yield key

    def __len__(self):
        """
        Gets the number of settings in configuration.

        Returns nonnegative integer.
        """
        return len(self._settings)

    def __setitem__(self, i, argument):
        """
        Sets configuration item ``i`` to ``argument``.

        Returns none.
        """
        self._settings[i] = argument

    ### PRIVATE METHODS ###

    def _compare_configurations(self, old, new):
        old = '\n'.join(old.splitlines()[3:])
        new = '\n'.join(new.splitlines()[3:])
        return old == new

    def _configuration_from_string(self, string):
        if '[main]' not in string:
            string = '[main]\n' + string
        config_parser = configparser.ConfigParser()
        try:
            if six.PY3:
                config_parser.read_string(string)
                configuration = dict(config_parser['main'].items())
            else:
                string_io = StringIO(string)
                config_parser.readfp(string_io)
                configuration = dict(config_parser.items('main'))
        except configparser.ParsingError:
            configuration = {}
        return configuration

    def _configuration_to_string(self, configuration):
        option_definitions = self._get_option_definitions()
        known_items, unknown_items = [], []
        for key, value in sorted(configuration.items()):
            if key in option_definitions:
                known_items.append((key, value))
            else:
                unknown_items.append((key, value))
        result = []
        for line in self._get_initial_comment():
            if line:
                result.append('# {}'.format(line))
            else:
                result.append('')
        for key, value in known_items:
            result.append('')
            if key in option_definitions:
                for line in option_definitions[key]['comment']:
                    if line:
                        result.append('# {}'.format(line))
                    else:
                        result.append('')
            if value not in ('', None):
                result.append('{!s} = {!s}'.format(key, value))
            else:
                result.append('{!s} ='.format(key))
        if unknown_items:
            result.append('')
            result.append('# User-specified keys:')
            for key, value in unknown_items:
                result.append('')
                if value not in ('', None):
                    result.append('{!s} = {!s}'.format(key, value))
                else:
                    result.append('{!s} ='.format(key))
        string = '\n'.join(result)
        return string

    def _get_config_specification(self):
        specs = self._get_option_specification()
        return ['{} = {}'.format(key, value)
            for key, value in sorted(specs.items())]

    def _get_current_time(self):
        return time.strftime("%d %B %Y %H:%M:%S")

    @abc.abstractmethod
    def _get_initial_comment(self):
        raise NotImplementedError

    def _get_option_comments(self):
        options = self._get_option_definitions()
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    @abc.abstractmethod
    def _get_option_definitions(self):
        raise NotImplementedError

    def _get_option_specification(self):
        options = self._get_option_definitions()
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)

    def _validate_configuration(self, configuration):
        option_definitions = self._get_option_definitions()
        for key in option_definitions:
            if key not in configuration:
                configuration[key] = option_definitions[key]['default']
            validator = option_definitions[key]['validator']
            if isinstance(validator, type):
                if not isinstance(configuration[key], validator):
                    configuration[key] = option_definitions[key]['default']
            else:
                if not validator(configuration[key]):
                    configuration[key] = option_definitions[key]['default']
        for key in configuration:
            if configuration[key] in ('', 'None'):
                configuration[key] = None
        return configuration

    ### PUBLIC PROPERTIES ###

    @property
    def configuration_directory(self):
        """
        Gets configuration directory.

        ..  container:: example

            >>> configuration = abjad.AbjadConfiguration()
            >>> configuration.configuration_directory
            PosixPath('...')

        Defaults to $HOME/{directory_name}.

        If $HOME is read-only or $HOME/{directory_name} is read-only, returns
        $TEMP/{directory_name}.

        Also caches the initial result to reduce filesystem interaction.

        Returns path object.
        """
        if self._cached_configuration_directory is None:
            directory_name = self._configuration_directory_name
            home_directory = str(self.home_directory)
            flags = os.W_OK | os.X_OK
            if os.access(home_directory, flags):
                path = self.home_directory / directory_name
                if not path.exists() or (
                    path.exists() and os.access(str(path), flags)):
                    self._cached_configuration_directory = path
                    return self._cached_configuration_directory
            temp_directory = self.temp_directory
            path = self.temp_directory / directory_name
            self._cached_configuration_directory = path
        return self._cached_configuration_directory

    @property
    def configuration_file_path(self):
        """
        Gets configuration file path.

        ..  container:: example

            >>> configuration = abjad.AbjadConfiguration()
            >>> configuration.configuration_file_path
            PosixPath('...')

        Returns path object.
        """
        return pathlib.Path(
            self.configuration_directory,
            self._configuration_file_name,
            )

    @property
    def home_directory(self):
        """
        Gets home directory.

        ..  container:: example

            >>> configuration = abjad.AbjadConfiguration()
            >>> configuration.home_directory
            PosixPath('...')

        Returns path object.
        """
        path = (
            os.environ.get('HOME') or
            os.environ.get('HOMEPATH') or
            os.environ.get('APPDATA') or
            tempfile.gettempdir()
            )
        return pathlib.Path(path).absolute()

    @property
    def temp_directory(self):
        """
        Gets temp directory.

        ..  container:: example

            >>> configuration = abjad.AbjadConfiguration()
            >>> configuration.temp_directory
            PosixPath('...')

        Returns path object.
        """
        return pathlib.Path(tempfile.gettempdir())

    ### PUBLIC METHODS ###

    def get(self, *arguments, **keywords):
        """
        Gets a key.
        """
        return self._settings.get(*arguments, **keywords)
