import collections
import configparser
import importlib
import os
import pathlib
import subprocess
import tempfile
import time
import traceback
import types
import typing

import uqbar.apis


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
    _lilypond_version_string: typing.ClassVar[str | None] = None

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
                    print(new_contents, file=file_pointer)
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

    def __eq__(self, argument):
        """
        Returns true when ``argument`` is configuratioin with same settings.
        """
        if isinstance(argument, type(self)):
            return self._settings == argument._settings
        return False

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.
        """
        return self._settings.__getitem__(argument)

    def __iter__(self) -> typing.Iterator[str]:
        """
        Iterates configuration settings.
        """
        for key in self._settings:
            yield key

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


def list_all_classes(modules="abjad", ignored_classes=None):
    """
    Lists all public classes defined in ``path``.

    ..  container:: example

        >>> for class_ in abjad.list_all_classes(modules="abjad"): class_
        <class 'abjad.bind.Wrapper'>
        <class 'abjad.configuration.Configuration'>
        <class 'abjad.contextmanagers.ContextManager'>
        <class 'abjad.contextmanagers.FilesystemState'>
        <class 'abjad.contextmanagers.ForbidUpdate'>
        <class 'abjad.contextmanagers.NullContextManager'>
        <class 'abjad.contextmanagers.ProgressIndicator'>
        <class 'abjad.contextmanagers.RedirectedStreams'>
        <class 'abjad.contextmanagers.TemporaryDirectory'>
        <class 'abjad.contextmanagers.TemporaryDirectoryChange'>
        <class 'abjad.contextmanagers.Timer'>
        <class 'abjad.contributions.ContributionsBySite'>
        <class 'abjad.cyclictuple.CyclicTuple'>
        <class 'abjad.duration.Duration'>
        <class 'abjad.duration.Offset'>
        <class 'abjad.exceptions.AssignabilityError'>
        <class 'abjad.exceptions.ImpreciseMetronomeMarkError'>
        <class 'abjad.exceptions.LilyPondParserError'>
        <class 'abjad.exceptions.MissingContextError'>
        <class 'abjad.exceptions.MissingMetronomeMarkError'>
        <class 'abjad.exceptions.ParentageError'>
        <class 'abjad.exceptions.PersistentIndicatorError'>
        <class 'abjad.exceptions.SchemeParserFinishedError'>
        <class 'abjad.exceptions.UnboundedTimeIntervalError'>
        <class 'abjad.exceptions.WellformednessError'>
        <class 'abjad.get.Lineage'>
        <class 'abjad.indicators.Arpeggio'>
        <class 'abjad.indicators.Articulation'>
        <class 'abjad.indicators.BarLine'>
        <class 'abjad.indicators.BeamCount'>
        <class 'abjad.indicators.BendAfter'>
        <class 'abjad.indicators.BreathMark'>
        <class 'abjad.indicators.Clef'>
        <class 'abjad.indicators.ColorFingering'>
        <class 'abjad.indicators.Dynamic'>
        <class 'abjad.indicators.Fermata'>
        <class 'abjad.indicators.Glissando'>
        <class 'abjad.indicators.InstrumentName'>
        <class 'abjad.indicators.KeyCluster'>
        <class 'abjad.indicators.KeySignature'>
        <class 'abjad.indicators.LaissezVibrer'>
        <class 'abjad.indicators.LilyPondLiteral'>
        <class 'abjad.indicators.Markup'>
        <class 'abjad.indicators.MetronomeMark'>
        <class 'abjad.indicators.Mode'>
        <class 'abjad.indicators.Ottava'>
        <class 'abjad.indicators.RehearsalMark'>
        <class 'abjad.indicators.Repeat'>
        <class 'abjad.indicators.RepeatTie'>
        <class 'abjad.indicators.ShortInstrumentName'>
        <class 'abjad.indicators.StaffChange'>
        <class 'abjad.indicators.StartBeam'>
        <class 'abjad.indicators.StartGroup'>
        <class 'abjad.indicators.StartHairpin'>
        <class 'abjad.indicators.StartPhrasingSlur'>
        <class 'abjad.indicators.StartPianoPedal'>
        <class 'abjad.indicators.StartSlur'>
        <class 'abjad.indicators.StartTextSpan'>
        <class 'abjad.indicators.StartTrillSpan'>
        <class 'abjad.indicators.StemTremolo'>
        <class 'abjad.indicators.StopBeam'>
        <class 'abjad.indicators.StopGroup'>
        <class 'abjad.indicators.StopHairpin'>
        <class 'abjad.indicators.StopPhrasingSlur'>
        <class 'abjad.indicators.StopPianoPedal'>
        <class 'abjad.indicators.StopSlur'>
        <class 'abjad.indicators.StopTextSpan'>
        <class 'abjad.indicators.StopTrillSpan'>
        <class 'abjad.indicators.TextMark'>
        <class 'abjad.indicators.Tie'>
        <class 'abjad.indicators.TimeSignature'>
        <class 'abjad.indicators.VoiceNumber'>
        <class 'abjad.instruments.Accordion'>
        <class 'abjad.instruments.AltoFlute'>
        <class 'abjad.instruments.AltoSaxophone'>
        <class 'abjad.instruments.AltoTrombone'>
        <class 'abjad.instruments.AltoVoice'>
        <class 'abjad.instruments.BaritoneSaxophone'>
        <class 'abjad.instruments.BaritoneVoice'>
        <class 'abjad.instruments.BassClarinet'>
        <class 'abjad.instruments.BassFlute'>
        <class 'abjad.instruments.BassSaxophone'>
        <class 'abjad.instruments.BassTrombone'>
        <class 'abjad.instruments.BassVoice'>
        <class 'abjad.instruments.Bassoon'>
        <class 'abjad.instruments.Cello'>
        <class 'abjad.instruments.ClarinetInA'>
        <class 'abjad.instruments.ClarinetInBFlat'>
        <class 'abjad.instruments.ClarinetInEFlat'>
        <class 'abjad.instruments.Contrabass'>
        <class 'abjad.instruments.ContrabassClarinet'>
        <class 'abjad.instruments.ContrabassFlute'>
        <class 'abjad.instruments.ContrabassSaxophone'>
        <class 'abjad.instruments.Contrabassoon'>
        <class 'abjad.instruments.EnglishHorn'>
        <class 'abjad.instruments.Flute'>
        <class 'abjad.instruments.FrenchHorn'>
        <class 'abjad.instruments.Glockenspiel'>
        <class 'abjad.instruments.Guitar'>
        <class 'abjad.instruments.Harp'>
        <class 'abjad.instruments.Harpsichord'>
        <class 'abjad.instruments.Instrument'>
        <class 'abjad.instruments.Marimba'>
        <class 'abjad.instruments.MezzoSopranoVoice'>
        <class 'abjad.instruments.Oboe'>
        <class 'abjad.instruments.Percussion'>
        <class 'abjad.instruments.Piano'>
        <class 'abjad.instruments.Piccolo'>
        <class 'abjad.instruments.SopraninoSaxophone'>
        <class 'abjad.instruments.SopranoSaxophone'>
        <class 'abjad.instruments.SopranoVoice'>
        <class 'abjad.instruments.StringNumber'>
        <class 'abjad.instruments.TenorSaxophone'>
        <class 'abjad.instruments.TenorTrombone'>
        <class 'abjad.instruments.TenorVoice'>
        <class 'abjad.instruments.Trumpet'>
        <class 'abjad.instruments.Tuba'>
        <class 'abjad.instruments.Tuning'>
        <class 'abjad.instruments.Vibraphone'>
        <class 'abjad.instruments.Viola'>
        <class 'abjad.instruments.Violin'>
        <class 'abjad.instruments.Xylophone'>
        <class 'abjad.label.ColorMap'>
        <class 'abjad.lilypondfile.Block'>
        <class 'abjad.lilypondfile.LilyPondFile'>
        <class 'abjad.lyproxy.LilyPondContext'>
        <class 'abjad.lyproxy.LilyPondEngraver'>
        <class 'abjad.lyproxy.LilyPondGrob'>
        <class 'abjad.lyproxy.LilyPondGrobInterface'>
        <class 'abjad.math.Infinity'>
        <class 'abjad.math.NegativeInfinity'>
        <class 'abjad.meter.Meter'>
        <class 'abjad.meter.MetricAccentKernel'>
        <class 'abjad.metricmodulation.MetricModulation'>
        <class 'abjad.obgc.OnBeatGraceContainer'>
        <class 'abjad.overrides.Interface'>
        <class 'abjad.overrides.LilyPondOverride'>
        <class 'abjad.overrides.LilyPondSetting'>
        <class 'abjad.overrides.OverrideInterface'>
        <class 'abjad.overrides.SettingInterface'>
        <class 'abjad.parentage.Parentage'>
        <class 'abjad.parsers.base.Parser'>
        <class 'abjad.pattern.Pattern'>
        <class 'abjad.pattern.PatternTuple'>
        <class 'abjad.pcollections.PitchClassSegment'>
        <class 'abjad.pcollections.PitchClassSet'>
        <class 'abjad.pcollections.PitchRange'>
        <class 'abjad.pcollections.PitchSegment'>
        <class 'abjad.pcollections.PitchSet'>
        <class 'abjad.pcollections.TwelveToneRow'>
        <class 'abjad.pitch.Accidental'>
        <class 'abjad.pitch.Interval'>
        <class 'abjad.pitch.IntervalClass'>
        <class 'abjad.pitch.NamedInterval'>
        <class 'abjad.pitch.NamedIntervalClass'>
        <class 'abjad.pitch.NamedInversionEquivalentIntervalClass'>
        <class 'abjad.pitch.NamedPitch'>
        <class 'abjad.pitch.NamedPitchClass'>
        <class 'abjad.pitch.NumberedInterval'>
        <class 'abjad.pitch.NumberedIntervalClass'>
        <class 'abjad.pitch.NumberedInversionEquivalentIntervalClass'>
        <class 'abjad.pitch.NumberedPitch'>
        <class 'abjad.pitch.NumberedPitchClass'>
        <class 'abjad.pitch.Octave'>
        <class 'abjad.pitch.Pitch'>
        <class 'abjad.pitch.PitchClass'>
        <class 'abjad.pitch.StaffPosition'>
        <class 'abjad.rhythmtrees.RhythmTreeContainer'>
        <class 'abjad.rhythmtrees.RhythmTreeLeaf'>
        <class 'abjad.rhythmtrees.RhythmTreeNode'>
        <class 'abjad.rhythmtrees.RhythmTreeParser'>
        <class 'abjad.score.AfterGraceContainer'>
        <class 'abjad.score.BeforeGraceContainer'>
        <class 'abjad.score.Chord'>
        <class 'abjad.score.Cluster'>
        <class 'abjad.score.Component'>
        <class 'abjad.score.Container'>
        <class 'abjad.score.Context'>
        <class 'abjad.score.DrumNoteHead'>
        <class 'abjad.score.IndependentAfterGraceContainer'>
        <class 'abjad.score.Leaf'>
        <class 'abjad.score.MultimeasureRest'>
        <class 'abjad.score.Note'>
        <class 'abjad.score.NoteHead'>
        <class 'abjad.score.NoteHeadList'>
        <class 'abjad.score.Rest'>
        <class 'abjad.score.Score'>
        <class 'abjad.score.Skip'>
        <class 'abjad.score.Staff'>
        <class 'abjad.score.StaffGroup'>
        <class 'abjad.score.TremoloContainer'>
        <class 'abjad.score.Tuplet'>
        <class 'abjad.score.Voice'>
        <class 'abjad.select.LogicalTie'>
        <class 'abjad.setclass.SetClass'>
        <class 'abjad.tag.Tag'>
        <class 'abjad.timespan.OffsetCounter'>
        <class 'abjad.timespan.Timespan'>
        <class 'abjad.timespan.TimespanList'>
        <class 'abjad.tweaks.Bundle'>
        <class 'abjad.tweaks.Tweak'>
        <class 'abjad.verticalmoment.VerticalMoment'>

    """
    all_classes = set()
    for module in yield_all_modules(modules):
        if "parser" in module.__name__:
            continue
        name = module.__name__.split(".")[-1]
        for name in dir(module):
            item = getattr(module, name)
            if isinstance(item, type):
                if "sphinx" in repr(item):
                    continue
                if item.__name__.startswith("_"):
                    continue
                if "abjad.io" in str(item):
                    continue
                if "abjad" in repr(item):
                    all_classes.add(item)
    if ignored_classes:
        ignored_classes = set(ignored_classes)
        all_classes.difference_update(ignored_classes)
    return list(sorted(all_classes, key=lambda _: (_.__module__, _.__name__)))


def list_all_functions(modules="abjad"):
    """
    Lists all public functions defined in ``modules``.

    ..  container:: example

        >>> functions = abjad.list_all_functions(modules="abjad")
        >>> names = [_.__name__ for _ in functions]
        >>> # for name in sorted(names): name

    """
    all_functions = set()
    for module in yield_all_modules(modules):
        name = module.__name__.split(".")[-1]
        if name.startswith("_"):
            continue
        if "sphinx" in repr(module):
            continue
        for name in sorted(dir(module)):
            item = getattr(module, name)
            if isinstance(item, types.FunctionType):
                if item.__name__.startswith("_"):
                    continue
                if "abjad" not in repr(item.__module__):
                    continue
                all_functions.add(item)
    return list(sorted(all_functions, key=lambda _: (_.__module__, _.__name__)))


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
