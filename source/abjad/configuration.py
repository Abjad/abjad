"""
Configuration.
"""

import configparser
import os
import pathlib
import subprocess
import tempfile
import time
import traceback
import typing


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

    """

    __slots__ = ("_cached_abjad_configuration_directory", "_settings")

    _lilypond_version_string: typing.ClassVar[str] = ""

    # TODO: move start-up logic somewhere else?
    def __init__(self):
        self._cached_abjad_configuration_directory = None
        if not os.path.exists(str(self.abjad_configuration_directory())):
            try:
                os.makedirs(str(self.abjad_configuration_directory()))
            except (IOError, OSError):
                traceback.print_exc()
        old_contents = ""
        if self.abjad_configuration_file_path().exists():
            try:
                old_contents = self.abjad_configuration_file_path().read_text()
            except AttributeError:
                with self.abjad_configuration_file_path().open(mode="r") as f:
                    old_contents = f.read()
        configuration = self._configuration_from_string(old_contents)
        configuration = self._validate_configuration(configuration)
        new_contents = self._configuration_to_string(configuration)
        if not self._compare_configurations(old_contents, new_contents):
            try:
                with open(
                    str(self.abjad_configuration_file_path()), "w"
                ) as file_pointer:
                    print(new_contents, file=file_pointer)
            except (IOError, OSError):
                traceback.print_exc()
        self._settings = configuration
        self._make_missing_directories()

    def __eq__(self, argument):
        if isinstance(argument, type(self)):
            return self._settings == argument._settings
        return False

    def __getitem__(self, argument) -> typing.Any:
        return self._settings.__getitem__(argument)

    def _compare_configurations(self, old, new):
        old = "\n".join(old.splitlines()[3:])
        new = "\n".join(new.splitlines()[3:])
        return old == new

    def _configuration_from_string(self, string):
        if "[main]" not in string:
            string = "[main]\n" + string
        config_parser = configparser.ConfigParser()
        try:
            config_parser.read_string(string)
            configuration = dict(config_parser["main"].items())
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

    @staticmethod
    def _get_home_directory() -> pathlib.Path:
        path = (
            os.environ.get("HOME")
            or os.environ.get("HOMEPATH")
            or os.environ.get("APPDATA")
            or tempfile.gettempdir()
        )
        return pathlib.Path(path).absolute()

    def _get_initial_comment(self):
        current_time = time.strftime("%d %B %Y %H:%M:%S")
        return [
            f"Abjad configuration file created on {current_time}.",
            "This file is interpreted by Python's ConfigParser ",
            "and follows ini syntax.",
        ]

    def _get_option_definitions(self):
        options = {
            "abjad_output_directory": {
                "comment": [
                    "Set to the directory where all Abjad-generated files",
                    "(such as PDFs and LilyPond files) should be saved.",
                    "Defaults to $HOME/.abjad/output/",
                ],
                "default": os.path.join(
                    str(self.abjad_configuration_directory()), "output"
                ),
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

    def _make_missing_directories(self):
        if not os.path.exists(self.abjad_output_directory()):
            try:
                os.makedirs(self.abjad_output_directory())
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

    def abjad_configuration_file_path(self) -> pathlib.Path:
        """
        Gets Abjad configuration file path.
        """
        return self.abjad_configuration_directory() / "abjad.cfg"

    def abjad_configuration_directory(self) -> pathlib.Path:
        """
        Gets Abjad configuration directory.
        """
        if self._cached_abjad_configuration_directory is None:
            directory_name = ".abjad"
            home_directory = str(self._get_home_directory())
            flags = os.W_OK | os.X_OK
            if os.access(home_directory, flags):
                path = self._get_home_directory() / directory_name
                if not path.exists() or (path.exists() and os.access(str(path), flags)):
                    self._cached_abjad_configuration_directory = path
                    return self._cached_abjad_configuration_directory
            path = pathlib.Path(tempfile.gettempdir()) / directory_name
            self._cached_abjad_configuration_directory = path
        return self._cached_abjad_configuration_directory

    def abjad_install_directory(self) -> pathlib.Path:
        """
        Gets Abjad install directory.
        """
        return pathlib.Path(__file__).parent.parent

    def abjad_output_directory(self) -> pathlib.Path:
        """
        Gets Abjad output directory.
        """
        if "abjad_output_directory" in self._settings:
            return pathlib.Path(self._settings["abjad_output_directory"])
        return self.abjad_configuration_directory() / "output"

    def lilypond_log_file_path(self) -> pathlib.Path:
        """
        Gets LilyPond log file path.
        """
        return self.abjad_output_directory() / "lilypond.log"

    def lilypond_version_string(self) -> str:
        """
        Gets LilyPond version string.
        """
        if self._lilypond_version_string != "":
            return self._lilypond_version_string
        command = ["lilypond", "--version"]
        proc = subprocess.run(command, stdout=subprocess.PIPE)
        assert proc.stdout is not None
        lilypond_version_string = proc.stdout.decode().split()[2]
        Configuration._lilypond_version_string = lilypond_version_string
        return lilypond_version_string
