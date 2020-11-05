import collections
import importlib
import os
import pathlib
import subprocess
import tempfile
import time
import traceback
import types
import typing

import six
import uqbar.apis

from . import storage


class Configuration:
    """
    Configuration.

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

    __documentation_section__ = "System configuration"

    __slots__ = ("_cached_configuration_directory", "_settings")

    _configuration_directory_name = ".abjad"

    _configuration_file_name = "abjad.cfg"

    # for caching
    _lilypond_version_string: typing.Optional[str] = None

    ### INITIALIZER ###

    def __init__(self):
        self._cached_configuration_directory = None
        if not os.path.exists(str(self.configuration_directory)):
            try:
                os.makedirs(str(self.configuration_directory))
            except (IOError, OSError):
                traceback.print_exc()
        old_contents = ""
        if self.configuration_file_path.exists():
            try:
                old_contents = self.configuration_file_path.read_text()
            except AttributeError:
                with self.configuration_file_path.open(mode="r") as f:
                    old_contents = f.read()
        configuration = self._configuration_from_string(old_contents)
        configuration = self._validate_configuration(configuration)
        new_contents = self._configuration_to_string(configuration)
        if not self._compare_configurations(old_contents, new_contents):
            try:
                with open(str(self.configuration_file_path), "w") as file_pointer:
                    file_pointer.write(new_contents)
            except (IOError, OSError):
                traceback.print_exc()
        self._settings = configuration
        self._make_missing_directories()

    ### SPECIAL METHODS ###

    def __delitem__(self, i) -> None:
        """
        Deletes item ``i`` from configuration.
        """
        del self._settings[i]

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.
        """
        return self._settings.__getitem__(argument)

    def __iter__(self) -> typing.Generator:
        """
        Iterates configuration settings.
        """
        for key in self._settings:
            yield key

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return storage.StorageFormatManager(self).get_repr_format()

    def __setitem__(self, i, argument) -> None:
        """
        Sets configuration item ``i`` to ``argument``.
        """
        self._settings[i] = argument

    ### PRIVATE METHODS ###

    def _compare_configurations(self, old, new):
        old = "\n".join(old.splitlines()[3:])
        new = "\n".join(new.splitlines()[3:])
        return old == new

    def _configuration_from_string(self, string):
        if "[main]" not in string:
            string = "[main]\n" + string
        config_parser = six.moves.configparser.ConfigParser()
        try:
            if six.PY3:
                config_parser.read_string(string)
                configuration = dict(config_parser["main"].items())
            else:
                string_io = six.moves.StringIO(string)
                config_parser.readfp(string_io)
                configuration = dict(config_parser.items("main"))
        except six.moves.configparser.ParsingError:
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
                result.append(f"# {line}")
            else:
                result.append("")
        for key, value in known_items:
            result.append("")
            if key in option_definitions:
                for line in option_definitions[key]["comment"]:
                    if line:
                        result.append(f"# {line}")
                    else:
                        result.append("")
            if value not in ("", None):
                result.append(f"{key!s} = {value!s}")
            else:
                result.append(f"{key!s} =")
        if unknown_items:
            result.append("")
            result.append("# User-specified keys:")
            for key, value in unknown_items:
                result.append("")
                if value not in ("", None):
                    result.append(f"{key!s} = {value!s}")
                else:
                    result.append(f"{key!s} =")
        string = "\n".join(result)
        return string

    def _get_config_specification(self):
        specs = self._get_option_specification()
        return [f"{key} = {value}" for key, value in sorted(specs.items())]

    def _get_current_time(self):
        return time.strftime("%d %B %Y %H:%M:%S")

    def _get_initial_comment(self):
        current_time = self._get_current_time()
        return [
            f"Abjad configuration file created on {current_time}.",
            "This file is interpreted by Python's ConfigParser ",
            "and follows ini syntax.",
        ]

    def _get_option_comments(self):
        options = self._get_option_definitions()
        comments = [(key, options[key]["comment"]) for key in options]
        return dict(comments)

    def _get_option_definitions(self):
        options = {
            "abjad_output_directory": {
                "comment": [
                    "Set to the directory where all Abjad-generated files",
                    "(such as PDFs and LilyPond files) should be saved.",
                    "Defaults to $HOME/.abjad/output/",
                ],
                "default": os.path.join(str(self.configuration_directory), "output"),
                "validator": str,
            },
            "composer_email": {
                "comment": ["Your email."],
                "default": "first.last@domain.com",
                "validator": str,
            },
            "composer_full_name": {
                "comment": ["Your full name."],
                "default": "Full Name",
                "validator": str,
            },
            "composer_github_username": {
                "comment": ["Your GitHub username."],
                "default": "username",
                "validator": str,
            },
            "composer_last_name": {
                "comment": ["Your last name."],
                "default": "Name",
                "validator": str,
            },
            "composer_scores_directory": {
                "comment": ["Your scores directory."],
                "default": str(self.home_directory / "scores"),
                "validator": str,
            },
            "composer_uppercase_name": {
                "comment": ["Your full name in uppercase for score covers."],
                "default": "FULL NAME",
                "validator": str,
            },
            "composer_website": {
                "comment": ["Your website."],
                "default": "www.composername.com",
                "validator": str,
            },
            "lilypond_path": {
                "comment": [
                    "Lilypond executable path. Set to override dynamic lookup."
                ],
                "default": "lilypond",
                "validator": str,
            },
            "midi_player": {
                "comment": [
                    "MIDI player to open MIDI files.",
                    "When unset your OS should know how to open MIDI files.",
                ],
                "default": None,
                "validator": str,
            },
            "pdf_viewer": {
                "comment": [
                    "PDF viewer to open PDF files.",
                    "When unset your OS should know how to open PDFs.",
                ],
                "default": None,
                "validator": str,
            },
            "text_editor": {
                "comment": [
                    "Text editor to edit text files.",
                    "When unset your OS should know how to open text files.",
                ],
                "default": None,
                "validator": str,
            },
        }
        return options

    def _get_option_specification(self):
        options = self._get_option_definitions()
        specs = [(key, options[key]["spec"]) for key in options]
        return dict(specs)

    def _make_missing_directories(self):
        if not os.path.exists(self.abjad_output_directory):
            try:
                os.makedirs(self.abjad_output_directory)
            except (IOError, OSError):
                traceback.print_exc()

    def _validate_configuration(self, configuration):
        option_definitions = self._get_option_definitions()
        for key in option_definitions:
            if key not in configuration:
                configuration[key] = option_definitions[key]["default"]
            validator = option_definitions[key]["validator"]
            if isinstance(validator, type):
                if not isinstance(configuration[key], validator):
                    configuration[key] = option_definitions[key]["default"]
            else:
                if not validator(configuration[key]):
                    configuration[key] = option_definitions[key]["default"]
        for key in configuration:
            if configuration[key] in ("", "None"):
                configuration[key] = None
        return configuration

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_directory(self) -> pathlib.Path:
        """
        Gets Abjad directory.
        """
        return pathlib.Path(__file__).parent.parent

    @property
    def abjad_output_directory(self) -> pathlib.Path:
        """
        Gets Abjad output directory.
        """
        if "abjad_output_directory" in self._settings:
            return pathlib.Path(self._settings["abjad_output_directory"])
        return self.configuration_directory / "output"

    @property
    def boilerplate_directory(self) -> pathlib.Path:
        """
        Gets Abjad boilerplate directory.
        """
        return self.abjad_directory.parent / "boilerplate"

    @property
    def composer_email(self) -> str:
        """
        Gets composer email.
        """
        return self._settings["composer_email"]

    @property
    def composer_full_name(self) -> str:
        """
        Gets composer full name.
        """
        return self._settings["composer_full_name"]

    @property
    def composer_github_username(self) -> str:
        """
        Gets GitHub username.
        """
        return self._settings["composer_github_username"]

    @property
    def composer_last_name(self) -> str:
        """
        Gets composer last name.
        """
        return self._settings["composer_last_name"]

    @property
    def composer_scores_directory(self) -> pathlib.Path:
        """
        Gets composer scores directory.
        """
        if "composer_scores_directory" in self._settings:
            return pathlib.Path(self._settings["composer_scores_directory"])
        return self.home_directory / "Scores"

    @property
    def composer_uppercase_name(self) -> str:
        """
        Gets composer uppercase name.
        """
        return self._settings["composer_uppercase_name"]

    @property
    def composer_website(self) -> str:
        """
        Gets composer website.
        """
        return self._settings["composer_website"]

    @property
    def configuration_directory(self) -> pathlib.Path:
        """
        Gets configuration directory.

        ..  container:: example

            >>> configuration = abjad.Configuration()
            >>> configuration.configuration_directory
            PosixPath('...')

        Defaults to $HOME/{directory_name}.

        Returns $TEMP/{directory_name} if $HOME is read-only or $HOME/{directory_name}
        is read-only.

        Also caches the initial result to reduce filesystem interaction.
        """
        if self._cached_configuration_directory is None:
            directory_name = self._configuration_directory_name
            home_directory = str(self.home_directory)
            flags = os.W_OK | os.X_OK
            if os.access(home_directory, flags):
                path = self.home_directory / directory_name
                if not path.exists() or (path.exists() and os.access(str(path), flags)):
                    self._cached_configuration_directory = path
                    return self._cached_configuration_directory
            path = pathlib.Path(tempfile.gettempdir()) / directory_name
            self._cached_configuration_directory = path
        return self._cached_configuration_directory

    @property
    def configuration_file_path(self) -> pathlib.Path:
        """
        Gets configuration file path.

        ..  container:: example

            >>> configuration = abjad.Configuration()
            >>> configuration.configuration_file_path
            PosixPath('...')

        """
        return self.configuration_directory / self._configuration_file_name

    @property
    def home_directory(self) -> pathlib.Path:
        """
        Gets home directory.

        ..  container:: example

            >>> configuration = abjad.Configuration()
            >>> configuration.home_directory
            PosixPath('...')

        """
        path = (
            os.environ.get("HOME")
            or os.environ.get("HOMEPATH")
            or os.environ.get("APPDATA")
            or tempfile.gettempdir()
        )
        return pathlib.Path(path).absolute()

    @property
    def lilypond_log_file_path(self) -> pathlib.Path:
        """
        Gets LilyPond log file path.
        """
        return self.abjad_output_directory / "lily.log"

    ### PUBLIC METHODS ###

    def get(self, *arguments, **keywords):
        """
        Gets a key.
        """
        return self._settings.get(*arguments, **keywords)

    def get_lilypond_version_string(self) -> str:
        """
        Gets LilyPond version string.

        ..  container:: example

            >>> configuration = abjad.Configuration()
            >>> configuration.get_lilypond_version_string() # doctest: +SKIP
            '2.19.84'

        """
        if self._lilypond_version_string is not None:
            return self._lilypond_version_string
        command = ["lilypond", "--version"]
        proc = subprocess.run(command, stdout=subprocess.PIPE)
        assert proc.stdout is not None
        lilypond_version_string = proc.stdout.decode().split()[2]
        Configuration._lilypond_version_string = lilypond_version_string
        return lilypond_version_string


### FUNCTIONS ###


def list_all_classes(modules="abjad", ignored_classes=None):
    """
    Lists all public classes defined in ``path``.

    ..  container:: example

        >>> all_classes = abjad.list_all_classes(modules="abjad")

    """
    all_classes = set()
    for module in yield_all_modules(modules):
        name = module.__name__.split(".")[-1]
        if name.startswith("_"):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, type):
            all_classes.add(obj)
    if ignored_classes:
        ignored_classes = set(ignored_classes)
        all_classes.difference_update(ignored_classes)
    return list(sorted(all_classes, key=lambda x: (x.__module__, x.__name__)))


def list_all_functions(modules="abjad"):
    """
    Lists all public functions defined in ``modules``.

    ..  container:: example

        >>> all_functions = abjad.list_all_functions(modules="abjad")

    """
    all_functions = set()
    for module in yield_all_modules(modules):
        name = module.__name__.split(".")[-1]
        if name.startswith("_"):
            continue
        if not hasattr(module, name):
            continue
        obj = getattr(module, name)
        if isinstance(obj, types.FunctionType):
            all_functions.add(obj)
    return list(sorted(all_functions, key=lambda x: (x.__module__, x.__name__)))


configuration = Configuration()


def yield_all_modules(paths=None):
    """
    Yields all modules encountered in ``path``.

    Returns generator.
    """
    _paths = []
    if not paths:
        _paths = configuration.abjad_directory
    elif isinstance(paths, str):
        module = importlib.import_module(paths)
        _paths.extend(module.__path__)
    elif isinstance(paths, types.ModuleType):
        _paths.extend(paths.__path__)
    elif isinstance(paths, collections.abc.Iterable):
        for path in paths:
            if isinstance(path, types.ModuleType):
                _paths.extend(path.__path__)
            elif isinstance(path, str):
                module = importlib.import_module(path)
                _paths.extend(module.__path__)
            else:
                raise ValueError(module)
    for path in _paths:
        for source_path in uqbar.apis.collect_source_paths([path]):
            package_path = uqbar.apis.source_path_to_package_path(source_path)
            yield importlib.import_module(package_path)
