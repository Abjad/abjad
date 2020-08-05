import cProfile
import datetime
import difflib
import hashlib
import io
import os
import pathlib
import pstats
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
import typing

import uqbar

import abjad

from .configuration import Configuration
from .contextmanagers import Timer
from .formatx import LilyPondFormatManager, StorageFormatManager
from .illustrators import illustrate
from .lilypondfile import Block
from .parentage import Parentage
from .score import Container, Leaf, Tuplet

configuration = Configuration()


class AbjadGrapher(uqbar.graphs.Grapher):
    """
    Abjad grapher.
    """

    ### INTIALIZER ###

    def __init__(self, graphable, format_="pdf", layout="dot"):
        uqbar.graphs.Grapher.__init__(self, graphable, format_=format_, layout=layout)

    ### PUBLIC METHODS ###

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(configuration["abjad_output_directory"])

    def open_output_path(self, output_path):
        IOManager.open_file(str(output_path))


class LilyPondIO:
    """
    LilyPond IO.
    """

    ### INITIALIZER ###

    def __init__(
        self,
        illustrable,
        *,
        flags=None,
        output_directory=None,
        render_prefix=None,
        should_copy_stylesheets=False,
        should_open=True,
        should_persist_log=True,
        string=None,
        **keywords,
    ):
        self.flags = flags or []
        self.illustrable = illustrable
        self.keywords = keywords
        self.output_directory = output_directory
        self.render_prefix = render_prefix
        self.should_copy_stylesheets = bool(should_copy_stylesheets)
        self.should_open = bool(should_open)
        self.should_persist_log = bool(should_persist_log)
        self.string = string

    ### SPECIAL METHODS ###

    def __call__(self):
        with Timer() as format_timer:
            string = self.string or self.get_string()
        format_time = format_timer.elapsed_time
        render_prefix = self.render_prefix or self.get_render_prefix(string)
        render_directory = self.get_render_directory()
        input_path = (render_directory / render_prefix).with_suffix(".ly")
        self.persist_string(string, input_path)
        lilypond_path = self.get_lilypond_path()
        if self.should_copy_stylesheets:
            self.copy_stylesheets(render_directory)
        render_command = self.get_render_command(input_path, lilypond_path)
        with Timer() as render_timer:
            log, success = self.run_command(render_command)
        render_time = render_timer.elapsed_time
        if self.should_persist_log:
            self.persist_log(log, input_path.with_suffix(".log"))
        output_directory = pathlib.Path(
            self.output_directory or self.get_output_directory()
        )
        output_paths = self.migrate_assets(
            render_prefix, render_directory, output_directory
        )
        openable_paths = []
        for output_path in self.get_openable_paths(output_paths):
            openable_paths.append(output_path)
            if self.should_open:
                self.open_output_path(output_path)
        return openable_paths, format_time, render_time, success, log

    ### PUBLIC METHODS ###

    def copy_stylesheets(self, render_directory):
        for directory in self.get_stylesheets_directories():
            for path in directory.glob("*.*ly"):
                shutil.copy(path, render_directory)

    def get_lilypond_path(self):
        lilypond_path = configuration.get("lilypond_path")
        if not lilypond_path:
            lilypond_paths = IOManager.find_executable("lilypond")
            if lilypond_paths:
                lilypond_path = lilypond_paths[0]
            else:
                lilypond_path = "lilypond"
        return lilypond_path

    def get_openable_paths(self, output_paths) -> typing.Generator:
        for path in output_paths:
            if path.suffix in (".pdf", ".mid", ".midi", ".svg", ".png"):
                yield path

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(configuration["abjad_output_directory"])

    def get_render_command(self, input_path, lilypond_path) -> str:
        parts = [
            str(lilypond_path),
            *self.flags,
            "-dno-point-and-click",
            "-o",
            str(input_path.with_suffix("")),
            str(input_path),
        ]
        return " ".join(parts)

    def get_render_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def get_render_prefix(self, string) -> str:
        timestamp = re.sub(r"[^\w]", "-", datetime.datetime.now().isoformat())
        checksum = hashlib.sha1(string.encode()).hexdigest()[:7]
        return f"{timestamp}-{checksum}"

    def get_string(self) -> str:
        if hasattr(self.illustrable, "__illustrate__"):
            lilypond_file = self.illustrable.__illustrate__(**self.keywords)
        else:
            lilypond_file = illustrate(self.illustrable, **self.keywords)
        return lilypond_file._get_lilypond_format()

    def get_stylesheets_directories(self) -> typing.List[pathlib.Path]:
        directories = []
        path = getattr(abjad, "__path__")
        abjad_path = pathlib.Path(path[0])
        directory = abjad_path / ".." / "docs" / "source" / "_stylesheets"
        directories.append(directory)
        if "sphinx_stylesheets_directory" in configuration:
            string = configuration["sphinx_stylesheets_directory"]
            directory = pathlib.Path(string)
            directories.append(directory)
        return directories

    def migrate_assets(
        self, render_prefix, render_directory, output_directory
    ) -> typing.Sequence[pathlib.Path]:
        migrated_assets = []
        for old_path in render_directory.iterdir():
            if not old_path.name.startswith(render_prefix):
                continue
            new_path = output_directory / old_path.name
            shutil.copy(old_path, new_path)
            migrated_assets.append(new_path)
        return migrated_assets

    def open_output_path(self, output_path):
        IOManager.open_file(str(output_path))

    def persist_log(self, string, input_path):
        input_path.write_text(string)

    def persist_string(self, string, input_path):
        input_path.write_text(string)

    def run_command(self, command):
        completed_process = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        text = completed_process.stdout.decode("utf-8")
        success = completed_process.returncode == 0
        return text, success


class Illustrator(LilyPondIO):
    """
    Illustrator.
    """

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> typing.Generator:
        for path in output_paths:
            if path.suffix == ".pdf":
                yield path


class IOManager:
    """
    IO manager.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Managers"

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _ensure_directory_existence(directory):
        if not directory:
            directory = "."
        if not os.path.isdir(directory):
            lines = []
            line = f"Attention: {directory!r} does not exist on your system."
            lines.append(line)
            lines.append("Abjad will now create it to store all output files.")
            lines.append("Press any key to continue.")
            message = "\n".join(lines)
            input(message)
            os.makedirs(directory)

    @staticmethod
    def _read_from_pipe(pipe):
        lines = []
        string = pipe.read()
        for line in string.splitlines():
            line = line.decode(errors="ignore")
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def _warn_when_output_directory_almost_full(last_number):
        abjad_output_directory = configuration["abjad_output_directory"]
        max_number = 10000
        lines = []
        lines.append("")
        lines.append("WARNING: Abjad output directory almost full!")
        line = f"Abjad output directory contains {last_number} files "
        line += f"and only {max_number} are allowed."
        lines.append(line)
        line = f"Please empty {abjad_output_directory} soon!"
        lines.append(line)
        lines.append("")
        for line in lines:
            print(line.center(80))

    ### PUBLIC METHODS ###

    @staticmethod
    def count_function_calls(
        argument: str,
        *,
        global_context: dict = None,
        local_context: dict = None,
        fixed_point: bool = True,
    ) -> int:
        """
        Counts function calls required to execute ``argument``.
        """

        def extract_count(profile_output) -> int:
            return int(profile_output.splitlines()[2].split()[0])

        if fixed_point:
            # profile at least twice to ensure consist results from profiler;
            # not sure why but profiler eventually levels off to consistent
            # output
            last_result, current_result = -1, 0
            while current_result != last_result:
                last_result = current_result
                string = IOManager.profile(
                    argument,
                    print_to_terminal=False,
                    global_context=global_context,
                    local_context=local_context,
                )
                assert isinstance(string, str)
                current_result = extract_count(string)
            return current_result
        result = IOManager.profile(
            argument,
            print_to_terminal=False,
            global_context=global_context,
            local_context=local_context,
        )
        assert isinstance(result, str)
        count = extract_count(result)
        return count

    @staticmethod
    def execute_file(
        path: str = None, *, attribute_names: typing.Tuple[str] = None
    ) -> typing.Optional[typing.Tuple[str]]:
        """
        Executes file ``path``.

        Returns ``attribute_names`` from file.
        """
        assert path is not None
        assert isinstance(attribute_names, tuple)
        path_ = pathlib.Path(path)
        if not path_.is_file():
            return None
        file_contents_string = path_.read_text()
        try:
            result = IOManager.execute_string(
                file_contents_string, attribute_names=attribute_names
            )
        except Exception:
            message = f"Exception raised in {path_}."
            # use print instead of display
            # to force to terminal even when called in silent context
            print(message)
            traceback.print_exc()
        return result

    @staticmethod
    def execute_string(
        string: str,
        *,
        attribute_names: typing.Tuple[str] = None,
        local_namespace: dict = None,
    ):
        """
        Executes ``string``.

        ..  container:: example

            >>> string = 'foo = 23'
            >>> attribute_names = ('foo', 'bar')
            >>> abjad.IOManager.execute_string(
            ...     string,
            ...     attribute_names=attribute_names,
            ...     )
            (23, None)

        Returns ``attribute_names`` from executed string.
        """
        assert isinstance(string, str)
        assert isinstance(attribute_names, tuple)
        if local_namespace is None:
            local_namespace = {}
        assert isinstance(local_namespace, dict)
        local_namespace = {}
        try:
            exec(string, local_namespace, local_namespace)
        except SyntaxError:
            return
        result = []
        for name in attribute_names:
            if name in local_namespace:
                result.append(local_namespace[name])
            else:
                result.append(None)
        return tuple(result)

    @staticmethod
    def find_executable(
        name: str, *, flags: int = os.X_OK
    ) -> typing.List[pathlib.Path]:
        """
        Finds executable ``name``.

        Similar to Unix ``which`` command.

        Returns list of zero or more full paths to ``name``.
        """
        result = []
        extensions = [x for x in os.environ.get("PATHEXT", "").split(os.pathsep) if x]
        PATH = os.environ.get("PATH", None)
        if PATH is None:
            return []
        for path_ in os.environ.get("PATH", "").split(os.pathsep):
            path = pathlib.Path(path_) / name
            if os.access(path, flags):
                result.append(path)
            for extension in extensions:
                path_extension = path / extension
                if os.access(path_extension, flags):
                    result.append(path_extension)
        return result

    @staticmethod
    def make_subprocess(command: str) -> subprocess.Popen:
        """
        Makes Popen instance.

        ..  container:: example

            >>> command = 'echo "hellow world"'
            >>> abjad.IOManager.make_subprocess(command)
            <subprocess.Popen object at 0x...>

        Defined equal to:

            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                )

        Redirects stderr to stdout.
        """
        return subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )

    @staticmethod
    def open_file(
        file_path: str,
        *,
        application: str = None,
        line_number: int = None,
        test: bool = None,
    ):
        """
        Opens ``file_path``.

        Uses ``application`` when ``application`` is not none.

        Uses Abjad configuration file ``text_editor`` when
        ``application`` is none.

        Takes best guess at operating system-specific file opener when both
        ``application`` and Abjad configuration file ``text_editor`` are none.

        Respects ``line_number`` when ``file_path`` can be opened with text
        editor.
        """
        if sys.platform.lower().startswith("win"):
            startfile = getattr(os, "startfile", None)
            assert startfile is not None
            startfile(file_path)
            return
        viewer = None
        if sys.platform.lower().startswith("linux"):
            viewer = application or "xdg-open"
        elif file_path.endswith(".pdf"):
            viewer = application or configuration["pdf_viewer"]
        elif file_path.endswith((".log", ".py", ".rst", ".txt")):
            viewer = application or configuration["text_editor"]
        elif file_path.endswith((".mid", ".midi")):
            viewer = application or configuration["midi_player"]
        viewer = viewer or "open"
        if line_number:
            command = f"{viewer} +{line_number} {file_path}"
        else:
            command = f"{viewer} {file_path}"
        if not test:
            IOManager.spawn_subprocess(command)

    @staticmethod
    def open_last_log() -> None:
        """
        Opens LilyPond log file in operating system-specific text editor.
        """
        text_editor = configuration.get("text_editor")
        file_path = configuration.lilypond_log_file_path
        IOManager.open_file(str(file_path), application=text_editor)

    @staticmethod
    def profile(
        argument: str,
        *,
        global_context: dict = None,
        line_count: int = 12,
        local_context: dict = None,
        print_callers: bool = False,
        print_callees: bool = False,
        print_to_terminal: bool = True,
        sort_by: str = "cumulative",
        strip_dirs: bool = True,
    ) -> typing.Optional[str]:
        """
        Profiles ``argument``.

        ..  container:: example

            ::

                >>> argument = 'abjad.Staff("c8 c8 c8 c8 c8 c8 c8 c8")'
                >>> abjad.IOManager.profile(
                ...     argument,
                ...     global_context=globals(),
                ...     ) # doctest: +SKIP
                Tue Apr  5 20:32:40 2011    _tmp_abj_profile

                        2852 function calls (2829 primitive calls) in 0.006 CPU seconds

                Ordered by: cumulative time
                List reduced from 118 to 12 due to restriction <12>

                ncalls  tottime  percall  cumtime  percall filename:lineno(function)
                        1    0.000    0.000    0.006    0.006 <string>:1(<module>)
                        1    0.001    0.001    0.003    0.003 make_notes.py:12(make_not
                        1    0.000    0.000    0.003    0.003 Staff.py:21(__init__)
                        1    0.000    0.000    0.003    0.003 Context.py:11(__init__)
                        1    0.000    0.000    0.003    0.003 Container.py:23(__init__)
                        1    0.000    0.000    0.003    0.003 Container.py:271(_initial
                        2    0.000    0.000    0.002    0.001 all_are_logical_voice_con
                    52    0.001    0.000    0.002    0.000 component_to_logical_voic
                        1    0.000    0.000    0.002    0.002 _construct_unprolated_not
                        8    0.000    0.000    0.002    0.000 make_tied_note.py:5(make_
                        8    0.000    0.000    0.002    0.000 make_tied_leaf.py:5(make_

        Wraps the built-in Python ``cProfile`` module.

        Set ``argument`` to any string of Abjad input.

        Set ``sort_by`` to ``'cumulative'``, ``'time'`` or ``'calls'``.

        Set ``line_count`` to any nonnegative integer.

        Set ``strip_dirs`` to true to strip directory names from output lines.

        See the `Python docs <http://docs.python.org/library/profile.html>`_
        for more information on the Python profilers.

        Returns none when ``print_to_terminal`` is false.

        Returns string when ``print_to_terminal`` is true.
        """
        now_string = datetime.datetime.today().strftime("%a %b %d %H:%M:%S %Y")
        profile = cProfile.Profile()
        local_context = local_context or locals()
        if global_context is None:
            profile = profile.run(argument)
        else:
            profile = profile.runctx(argument, global_context, local_context)
        stats_stream = io.StringIO()
        stats = pstats.Stats(profile, stream=stats_stream)
        if sort_by == "cum":
            sort_by = "cumulative"
        if strip_dirs:
            stats.strip_dirs().sort_stats(sort_by).print_stats(line_count)
        else:
            stats.sort_stats(sort_by).print_stats(line_count)
        if print_callers:
            stats.sort_stats(sort_by).print_callers(line_count)
        if print_callees:
            stats.sort_stats(sort_by).print_callees(line_count)
        result = now_string + "\n\n" + stats_stream.getvalue()
        stats_stream.close()
        if print_to_terminal:
            print(result)
            return None
        return result

    @staticmethod
    def run_command(command: str) -> typing.List[str]:
        """
        Runs command in subprocess.

        Returns list of strings read from subprocess stdout.
        """
        process = IOManager.make_subprocess(command)
        lines = IOManager._read_from_pipe(process.stdout)
        lines = lines.splitlines()
        return lines

    @staticmethod
    def run_lilypond(
        ly_path: str, *, flags: str = None, lilypond_log_file_path: pathlib.Path = None,
    ) -> bool:
        """
        Runs LilyPond on ``ly_path``.

        Writes redirected output of Unix ``date`` to top line of LilyPond log
        file.

        Then appends redirected output of LilyPond output to the LilyPond log
        file.
        """
        ly_path = str(ly_path)
        lilypond_path_ = configuration.get("lilypond_path")
        if lilypond_path_ is not None:
            assert isinstance(lilypond_path_, str), repr(lilypond_path_)
        if not lilypond_path_:
            lilypond_paths = IOManager.find_executable("lilypond")
            if lilypond_paths:
                lilypond_path_ = str(lilypond_paths[0])
            else:
                lilypond_path_ = "lilypond"
        lilypond_base, extension = os.path.splitext(ly_path)
        flags = flags or ""
        date = datetime.datetime.now().strftime("%c")
        if lilypond_log_file_path is None:
            log_file_path = configuration.lilypond_log_file_path
        else:
            log_file_path = lilypond_log_file_path
        command = "{} {} -dno-point-and-click -o {} {}".format(
            lilypond_path_, flags, lilypond_base, ly_path
        )
        process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        subprocess_output, _ = process.communicate()
        subprocess_output_string = subprocess_output.decode(errors="ignore")
        exit_code = process.returncode
        with open(log_file_path, "w") as file_pointer:
            file_pointer.write(date + "\n")
            file_pointer.write(subprocess_output_string)
        postscript_path = ly_path.replace(".ly", ".ps")
        try:
            os.remove(postscript_path)
        except OSError:
            pass
        # TODO: maybe just 'return exit_code'?
        if exit_code:
            return False
        return True

    @staticmethod
    def spawn_subprocess(command: str) -> int:
        """
        Spawns subprocess and runs ``command``.

        The function is basically a reimplementation of the
        deprecated ``os.system()`` using Python's ``subprocess`` module.

        Redirects stderr to stdout.
        """
        return subprocess.call(command, shell=True)


class PersistenceManager:
    """
    Persistence manager.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.persist(staff)
        PersistenceManager(client=Staff("c'4 e'4 d'4 f'4"))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_client",)

    _png_page_pattern = re.compile(r".+page(\d+)\.png")

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        """
        Client of persistence manager.

        Returns component or selection.
        """
        return self._client

    ### PUBLIC METHODS ###

    def as_ly(
        self, ly_file_path, *, illustrate_function=None, strict=None, **keywords,
    ):
        """
        Persists client as LilyPond file.

        Returns output path and elapsed formatting time when LilyPond output is
        written.
        """
        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if illustrate_function is not None:
            lilypond_file = illustrate_function(**keywords)
        elif hasattr(self._client, "__illustrate__"):
            lilypond_file = self._client.__illustrate__(**keywords)
        else:
            lilypond_file = illustrate(self._client, **keywords)
        assert ly_file_path is not None, repr(ly_file_path)
        ly_file_path = str(ly_file_path)
        ly_file_path = os.path.expanduser(ly_file_path)
        assert ly_file_path.endswith(".ly"), ly_file_path
        timer = Timer()
        with timer:
            string = lilypond_file._get_lilypond_format()
            if isinstance(strict, int):
                string = LilyPondFormatManager.align_tags(string, strict)
        abjad_formatting_time = timer.elapsed_time
        directory = os.path.dirname(ly_file_path)
        IOManager._ensure_directory_existence(directory)
        with open(ly_file_path, "w") as file_pointer:
            file_pointer.write(string)
        return ly_file_path, abjad_formatting_time

    def as_midi(self, midi_file_path, *, remove_ly=False, **keywords):
        """
        Persists client as MIDI file.

        Returns 4-tuple of output MIDI path, Abjad formatting time, LilyPond
        rendering time and success boolean.
        """
        if hasattr(self._client, "score_block"):
            lilypond_file = self._client
        else:
            lilypond_file = illustrate(self._client, **keywords)
        assert hasattr(lilypond_file, "score_block")
        if midi_file_path is not None:
            midi_file_path = os.path.expanduser(midi_file_path)
            without_extension = os.path.splitext(midi_file_path)[0]
            ly_file_path = f"{without_extension}.ly"
        else:
            ly_file_path = None
        result = type(self)(lilypond_file).as_ly(ly_file_path, **keywords)
        ly_file_path, abjad_formatting_time = result
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        if os.name == "nt":
            extension = "mid"
        else:
            extension = "midi"
        path = os.path.splitext(ly_file_path)[0]
        midi_file_path = f"{path}.{extension}"
        return (
            midi_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_pdf(
        self,
        pdf_file_path,
        *,
        illustrate_function=None,
        remove_ly=False,
        strict=None,
        **keywords,
    ):
        """
        Persists client as PDF.

        Returns output path, elapsed formatting time and elapsed rendering
        time when PDF output is written.
        """
        if strict is not None:
            assert isinstance(strict, int), repr(strict)
        if pdf_file_path is not None:
            pdf_file_path = str(pdf_file_path)
            pdf_file_path = os.path.expanduser(pdf_file_path)
            without_extension = os.path.splitext(pdf_file_path)[0]
            ly_file_path = f"{without_extension}.ly"
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path,
            illustrate_function=illustrate_function,
            strict=strict,
            **keywords,
        )
        ly_file_path, abjad_formatting_time = result
        without_extension = os.path.splitext(ly_file_path)[0]
        pdf_file_path = f"{without_extension}.pdf"
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(ly_file_path)
        lilypond_rendering_time = timer.elapsed_time
        if remove_ly:
            os.remove(ly_file_path)
        return (
            pdf_file_path,
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )

    def as_png(
        self,
        png_file_path,
        *,
        flags="--png",
        illustrate_function=None,
        preview=False,
        remove_ly=False,
        resolution=False,
        **keywords,
    ):
        """
        Persists client as PNG.

        Autogenerates file path when ``png_file_path`` is none.

        Returns output path(s), elapsed formatting time and elapsed rendering
        time.
        """
        if png_file_path is not None:
            png_file_path = os.path.expanduser(png_file_path)
            without_extension = os.path.splitext(png_file_path)[0]
            ly_file_path = f"{without_extension}.ly"
        else:
            ly_file_path = None
        result = self.as_ly(
            ly_file_path, illustrate_function=illustrate_function, **keywords
        )
        ly_file_path, abjad_formatting_time = result
        original_directory = os.path.split(ly_file_path)[0]
        original_ly_file_path = ly_file_path
        temporary_directory = tempfile.mkdtemp()
        temporary_ly_file_path = os.path.join(
            temporary_directory, os.path.split(ly_file_path)[1]
        )
        shutil.copy(original_ly_file_path, temporary_ly_file_path)
        # render lilypond flags
        if preview:
            flags = "-dpreview"
        if resolution and isinstance(resolution, int):
            flags += f" -dresolution={resolution}"
        timer = Timer()
        with timer:
            success = IOManager.run_lilypond(temporary_ly_file_path, flags=flags)
        lilypond_rendering_time = timer.elapsed_time
        png_file_paths = []
        for file_name in os.listdir(temporary_directory):
            if not file_name.endswith(".png"):
                continue
            source_png_file_path = os.path.join(temporary_directory, file_name)
            target_png_file_path = os.path.join(original_directory, file_name)
            shutil.move(source_png_file_path, target_png_file_path)
            png_file_paths.append(target_png_file_path)
        shutil.rmtree(temporary_directory)
        if remove_ly:
            os.remove(ly_file_path)
        if 1 < len(png_file_paths):
            png_file_paths.sort(
                key=lambda x: int(self._png_page_pattern.match(x).groups()[0])
            )
        return (
            tuple(png_file_paths),
            abjad_formatting_time,
            lilypond_rendering_time,
            success,
        )


class Player(LilyPondIO):
    """
    Player.
    """

    ### PUBLIC METHODS ###

    def get_openable_paths(self, output_paths) -> typing.Generator:
        for path in output_paths:
            if path.suffix in (".mid", ".midi"):
                yield path

    def get_string(self) -> str:
        lilypond_file = illustrate(self.illustrable, **self.keywords)
        assert hasattr(lilypond_file, "score_block")
        block = Block(name="midi")
        lilypond_file.score_block.items.append(block)
        return lilypond_file._get_lilypond_format()


class TestManager:
    """
    Manages test logic.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Managers"

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _compare_backup(path):
        if isinstance(path, str):
            paths = [path]
        elif isinstance(path, pathlib.Path):
            paths = [str(path)]
        elif isinstance(path, (tuple, list)):
            paths = [str(_) for _ in path]
        else:
            raise TypeError(path)
        for path in paths:
            backup_path = path + ".backup"
            if not TestManager.compare_files(path, backup_path):
                return False
        return True

    @staticmethod
    def _compare_lys(path_1, path_2):
        """
        Compares LilyPond file ``path_1`` to LilyPond file ``path_2``.

        Performs line-by-line comparison.

        Discards blank lines.

        Discards any LilyPond version statements.

        Discards any lines beginning with ``%``.

        Returns true or false.
        """
        file_1_lines = TestManager._normalize_ly(path_1)
        file_2_lines = TestManager._normalize_ly(path_2)
        return file_1_lines == file_2_lines

    @staticmethod
    def _compare_text_files(path_1, path_2):
        """
        Compares text file ``path_1`` to text file ``path_2``.

        Performs line-by-line comparison.

        Discards blank lines.

        Trims whitespace from the end of each line.

        Returns true or false.
        """
        file_1_lines, file_2_lines = [], []
        with open(path_1, "r") as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == "":
                    continue
                file_1_lines.append(line)
        with open(path_2, "r") as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == "":
                    continue
                file_2_lines.append(line)
        return file_1_lines == file_2_lines

    @staticmethod
    def _normalize_ly(path):
        lines = []
        with open(path, "r") as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == "":
                    continue
                if line.startswith(r"\version"):
                    continue
                elif line.startswith("%"):
                    continue
                lines.append(line)
        return lines

    ### PUBLIC METHODS ###

    @staticmethod
    def compare(string_1, string_2):
        """
        Compares ``string_1`` to ``string_2``.

        Massage newlines.

        Returns true or false.
        """
        assert isinstance(string_1, str), repr(str)
        split_lines = string_2.split("\n")
        if not split_lines[0] or split_lines[0].isspace():
            split_lines.pop(0)
        if not split_lines[-1] or split_lines[-1].isspace():
            split_lines.pop(-1)
        indent_width = 0
        if split_lines:
            for indent_width, character in enumerate(split_lines[0]):
                if character != " ":
                    break
        massaged_lines = []
        for split_line in split_lines:
            massaged_line = split_line[indent_width:]
            massaged_lines.append(massaged_line)
        massaged_string = "\n".join(massaged_lines)
        return string_1.replace("\t", "    ") == massaged_string

    @staticmethod
    def compare_files(path_1, path_2):
        """
        Compares file ``path_1`` to file ``path_2``.

        For all file types::

        * Performs line-by-line comparison
        * Discards blank lines

        For LilyPond files, additionally::

        * Discards any LilyPond version statements
        * Discards any lines beginning with ``%``

        Returns true when files compare the same and false when files compare
        differently.
        """
        path_1 = str(path_1)
        path_2 = str(path_2)
        if os.path.exists(path_1) and not os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and not os.path.exists(path_2):
            return True
        if path_1.endswith(".backup"):
            path_1 = path_1.strip(".backup")
        if path_2.endswith(".backup"):
            path_2 = path_2.strip(".backup")
        base_1, extension_1 = os.path.splitext(path_1)
        base_2, extension_2 = os.path.splitext(path_2)
        assert extension_1 == extension_2
        if extension_1 == ".ly":
            return TestManager._compare_lys(path_1, path_2)
        else:
            return TestManager._compare_text_files(path_1, path_2)

    @staticmethod
    def diff(object_a, object_b, title=None):
        """
        Gets diff of ``object_a`` and ``object_b`` formats.

        >>> one = abjad.Flute()
        >>> string_1 = abjad.storage(one)

        >>> two = abjad.BassFlute()
        >>> string_2 = abjad.storage(two)

        >>> diff = abjad.TestManager.diff(string_1, string_2, 'Diff:')
        >>> print(diff)
        Diff:
        - abjad.Flute(
        + abjad.BassFlute(
        ?       ++++
        -     name='flute',
        +     name='bass flute',
        ?           +++++
        -     short_name='fl.',
        +     short_name='bass fl.',
        ?                 +++++
              markup=abjad.Markup(
        -         contents=['Flute'],
        ?                    ^
        +         contents=['Bass flute'],
        ?                    ^^^^^^
                  ),
              short_markup=abjad.Markup(
        -         contents=['Fl.'],
        ?                    ^
        +         contents=['Bass fl.'],
        ?                    ^^^^^^
                  ),
              allowable_clefs=('treble',),
              context='Staff',
        -     middle_c_sounding_pitch=abjad.NamedPitch("c'"),
        ?                                              ^  -
        +     middle_c_sounding_pitch=abjad.NamedPitch('c'),
        ?                                              ^
        -     pitch_range=abjad.PitchRange('[C4, D7]'),
        ?                                     ^  ^^
        +     pitch_range=abjad.PitchRange('[C3, C6]'),
        ?                                     ^  ^^
        -     primary=True,
              )

        Returns string.
        """
        assert isinstance(object_a, str), repr(object_a)
        assert isinstance(object_b, str), repr(object_b)
        a_format = object_a
        b_format = object_b
        a_format = a_format.splitlines(True)
        b_format = b_format.splitlines(True)
        diff = "".join(difflib.ndiff(a_format, b_format))
        if title is not None:
            diff = title + "\n" + diff
        return diff


### PRIVATE FUCTIONS ###


def _as_graphviz_node(component):
    score_index = Parentage(component).score_index()
    score_index = "_".join(str(_) for _ in score_index)
    class_name = type(component).__name__
    if score_index:
        name = f"{class_name}_{score_index}"
    else:
        name = class_name
    node = uqbar.graphs.Node(name=name, attributes={"margin": 0.05, "style": "rounded"})
    table = uqbar.graphs.Table(attributes={"border": 2, "cellpadding": 5})
    node.append(table)

    if isinstance(component, Container):
        node[0].append(
            uqbar.graphs.TableRow(
                [
                    uqbar.graphs.TableCell(
                        type(component).__name__, attributes={"border": 0}
                    )
                ]
            )
        )

    if isinstance(component, Tuplet):
        node[0].extend(
            [
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            label=type(component).__name__, attributes={"border": 0}
                        )
                    ]
                ),
                uqbar.graphs.HRule(),
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            label=f"* {component.multiplier!s}",
                            attributes={"border": 0},
                        )
                    ]
                ),
            ]
        )

    if isinstance(component, Leaf):
        lilypond_format = component._get_compact_representation()
        lilypond_format = lilypond_format.replace("<", "&lt;")
        lilypond_format = lilypond_format.replace(">", "&gt;")
        node[0].extend(
            [
                uqbar.graphs.TableRow(
                    [
                        uqbar.graphs.TableCell(
                            type(component).__name__, attributes={"border": 0}
                        )
                    ]
                ),
                uqbar.graphs.HRule(),
                uqbar.graphs.TableRow(
                    [uqbar.graphs.TableCell(lilypond_format, attributes={"border": 0})]
                ),
            ]
        )

    return node


def _graph_container(container):
    assert isinstance(container, Container), repr(container)

    def recurse(component, leaf_cluster):
        component_node = _as_graphviz_node(component)
        node_mapping[component] = component_node
        node_order = [component_node.name]
        if isinstance(component, Container):
            graph.append(component_node)
            this_leaf_cluster = uqbar.graphs.Graph(
                name=component_node.name, attributes={"color": "grey75", "penwidth": 2},
            )
            all_are_leaves = True
            pending_node_order = []
            for child in component:
                if not isinstance(child, Leaf):
                    all_are_leaves = False
                child_node, child_node_order = recurse(child, this_leaf_cluster)
                pending_node_order.extend(child_node_order)
                edge = uqbar.graphs.Edge()
                edge.attach(component_node, child_node)
            if all_are_leaves:
                pending_node_order.reverse()
            node_order.extend(pending_node_order)
            if len(this_leaf_cluster):
                leaf_cluster.append(this_leaf_cluster)
        else:
            leaf_cluster.append(component_node)
        return component_node, node_order

    node_order = []
    node_mapping = {}
    graph = uqbar.graphs.Graph(
        name="G",
        attributes={"style": "rounded"},
        edge_attributes={},
        node_attributes={"fontname": "Arial", "shape": "none"},
    )
    leaf_cluster = uqbar.graphs.Graph(name="leaves")
    component_node, node_order = recurse(container, leaf_cluster)
    if len(leaf_cluster) == 1:
        graph.append(leaf_cluster[0])
    elif len(leaf_cluster):
        graph.append(leaf_cluster)
    graph._node_order = node_order
    return graph


### FUNCTIONS ###


def graph(
    graphable, format_="pdf", layout="dot", return_timing=False, **keywords,
):
    r"""
    Graphs ``argument``.

    ..  container:: example

        Graphs staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.graph(staff) # doctest: +SKIP

        ..  docs::

            >>> print(format(staff.__graph__(), "graphviz"))
            digraph G {
                graph [style=rounded];
                node [fontname=Arial,
                    shape=none];
                Staff_0 [label=<
                    <TABLE BORDER="2" CELLPADDING="5">
                        <TR>
                            <TD BORDER="0">Staff</TD>
                        </TR>
                    </TABLE>>,
                    margin=0.05,
                    style=rounded];
                subgraph Staff {
                    graph [color=grey75,
                        penwidth=2];
                    Note_0 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">c'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_1 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">d'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_2 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">e'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                    Note_3 [label=<
                        <TABLE BORDER="2" CELLPADDING="5">
                            <TR>
                                <TD BORDER="0">Note</TD>
                            </TR>
                            <HR/>
                            <TR>
                                <TD BORDER="0">f'4</TD>
                            </TR>
                        </TABLE>>,
                        margin=0.05,
                        style=rounded];
                }
                Staff_0 -> Note_0;
                Staff_0 -> Note_1;
                Staff_0 -> Note_2;
                Staff_0 -> Note_3;
            }

    ..  container:: example

        Graphs rhythm tree:

        >>> rtm_syntax = '(3 ((2 (2 1)) 2))'
        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> rhythm_tree = parser(rtm_syntax)[0]
        >>> abjad.graph(rhythm_tree) # doctest: +SKIP

        ..  docs::

            >>> print(format(rhythm_tree.__graph__(), 'graphviz'))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="3",
                    shape=triangle];
                node_1 [label="2",
                    shape=triangle];
                node_2 [label="2",
                    shape=box];
                node_3 [label="1",
                    shape=box];
                node_4 [label="2",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_4;
                node_1 -> node_2;
                node_1 -> node_3;
            }

    Opens image in default image viewer.
    """
    grapher = AbjadGrapher(graphable, format_=format_, layout=layout, **keywords)
    result = grapher()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def play(illustrable, return_timing=False, **keywords):
    """
    Plays ``argument``.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.play(note) # doctest: +SKIP

    Makes MIDI file.

    Appends ``.mid`` filename extension under Windows.

    Appends ``.midi`` filename extension under other operating systems.

    Opens MIDI file.
    """
    player = Player(illustrable, **keywords)
    result = player()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def persist(client):
    """
    Makes persistence manager.
    """
    return PersistenceManager(client)


def show(illustrable, return_timing=False, **keywords):
    r"""
    Shows ``argument``.

    ..  container:: example

        Shows note:

        >>> note = abjad.Note("c'4")
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4

    ..  container:: example

        Shows staff:

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
            }

    Makes LilyPond input files and output PDF.

    Writes LilyPond input file and output PDF to Abjad output directory.

    Opens output PDF.

    Returns none when ``return_timing`` is false.

    Returns pair of ``abjad_formatting_time`` and ``lilypond_rendering_time``
    when ``return_timing`` is true.
    """
    illustrator = Illustrator(illustrable, **keywords)
    result = illustrator()
    if not result:
        return
    _, format_time, render_time, success, log = result
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time
