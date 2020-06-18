import cProfile
import datetime
import io
import os
import pathlib
import pstats
import subprocess
import sys
import traceback
import typing

from ..formatting import StorageFormatManager
from .Configuration import Configuration

configuration = Configuration()


class IOManager(object):
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
        # special import necessary to satisfy parameterized pytests;
        # would like to remove this;
        # don't understand abjad/tests/test_IOManager_open_file.py
        from abjad import configuration

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
