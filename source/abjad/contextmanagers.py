import collections
import filecmp
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

from . import _updatelib
from . import configuration as _configuration
from . import iterate as _iterate
from . import string as _string

configuration = _configuration.Configuration()


class ContextManager:
    """
    An abstract context manager class.
    """

    __slots__ = ()
    _is_abstract = True

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"<{type(self).__name__}()>"


class FilesystemState(ContextManager):
    """
    Filesystem state context manager.
    """

    __documentation_section__ = "Context managers"

    __slots__ = ("_keep", "_remove")

    def __init__(self, keep=None, remove=None):
        keep = keep or []
        assert isinstance(keep, collections.abc.Iterable), repr(keep)
        keep = tuple([str(_) for _ in keep])
        self._keep = keep
        remove = remove or []
        assert isinstance(remove, collections.abc.Iterable), repr(remove)
        remove = tuple([str(_) for _ in remove])
        self._remove = remove

    def __enter__(self) -> "FilesystemState":
        """
        Backs up filesystem assets.
        """
        for path in self.remove:
            assert not os.path.exists(path), repr(path)
        for path in self.keep:
            assert os.path.exists(path), repr(path)
            assert os.path.isfile(path) or os.path.isdir(path), repr(path)
        for path in self.keep:
            backup_path = path + ".backup"
            if os.path.isfile(path):
                shutil.copyfile(path, backup_path)
                assert filecmp.cmp(path, backup_path), repr(path)
            elif os.path.isdir(path):
                shutil.copytree(path, backup_path)
            else:
                raise TypeError(f"neither file nor directory: {path}.")
        return self

    def __exit__(self, exg_type, exc_value, trackeback) -> None:
        """
        Restores filesytem assets and removes backups; also removes paths in remove list.
        """
        backup_paths = (_ + ".backup" for _ in self.keep)
        for path in backup_paths:
            assert os.path.exists(path), repr(path)
        for path in self.keep:
            backup_path = path + ".backup"
            assert os.path.exists(backup_path), repr(backup_path)
            if os.path.isfile(backup_path):
                shutil.copyfile(backup_path, path)
                filecmp.cmp(path, backup_path)
                os.remove(backup_path)
            elif os.path.isdir(backup_path):
                if os.path.exists(path):
                    shutil.rmtree(path)
                shutil.copytree(backup_path, path)
                shutil.rmtree(backup_path)
            else:
                raise TypeError(f"neither file nor directory: {path}.")
        for path in self.remove:
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    raise TypeError(f"neither file nor directory: {path}.")
        for path in self.keep:
            assert os.path.exists(path), repr(path)
        for path in backup_paths:
            assert not os.path.exists(path), repr(path)

    @property
    def keep(self):
        """
        Gets asset paths to restore on exit.

        Returns tuple.
        """
        return self._keep

    @property
    def remove(self):
        """
        Gets paths to remove on exit.

        Returns tuple.
        """
        return self._remove


class ForbidUpdate(ContextManager):
    r"""
    A context manager for forbidding score updates.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 ~ d'2 e'4")
        >>> with abjad.ForbidUpdate(component=staff):
        ...     for note in staff[:]:
        ...         pitch_1 = note.written_pitch
        ...         pitch_2 = pitch_1 + abjad.NamedInterval('M3')
        ...         pitches = [pitch_1, pitch_2]
        ...         chord = abjad.Chord(pitches, note.written_duration)
        ...         abjad.mutate.replace(note, chord)
        ...

        >>> abjad.wf.wellformed(staff)
        True

        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                <c' e'>8
                <d' fs'>8
                <d' fs'>2
                <e' gs'>4
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = ("_component", "_update_on_enter", "_update_on_exit")

    ### INITIALIZER ###

    def __init__(self, component=None, update_on_enter=True, update_on_exit=None):
        if component is not None:
            assert hasattr(component, "_timespan"), repr(component)
        self._component = component
        if update_on_enter is not None:
            update_on_enter = bool(update_on_enter)
        self._update_on_enter = update_on_enter
        if update_on_exit is not None:
            update_on_exit = bool(update_on_exit)
        self._update_on_exit = update_on_exit

    ### SPECIAL METHODS ###

    def __enter__(self) -> "ForbidUpdate":
        r"""
        Enters context manager.

        ..  container:: example

            REGRESSION. Indicators need to be updated after swap; context
            manager updates indicators before forbidding further updates:

            >>> staff = abjad.Staff(r"\times 1/1 { c'4 d' }")
            >>> abjad.attach(abjad.Clef("alto"), staff[0][0])
            >>> container = abjad.Container()
            >>> abjad.mutate.swap(staff[0], container)
            >>> with abjad.ForbidUpdate(staff):
            ...     for note in staff[0]:
            ...         print(note)
            ...         print(abjad.get.effective(note, abjad.Clef))
            ...
            Note("c'4")
            Clef(name='alto', hide=False)
            Note("d'4")
            Clef(name='alto', hide=False)

        """
        if self.component is not None:
            for component_ in _iterate.components(self.component):
                _updatelib._update_now(
                    component_, indicators=True, offsets=True, offsets_in_seconds=True
                )
            self.component._is_forbidden_to_update = True
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager.
        """
        if self.component is not None:
            self.component._is_forbidden_to_update = False
            if self.update_on_exit:
                for component_ in _iterate.components(self.component):
                    _updatelib._update_now(
                        component_,
                        indicators=True,
                        offsets=True,
                        offsets_in_seconds=True,
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def component(self):
        """
        Gets component.

        Set to component or none.

        Returns component or none.
        """
        return self._component

    @property
    def update_on_enter(self) -> bool | None:
        """
        Is true when context manager should update offsets on enter.

        Set to true, false or none.
        """
        return self._update_on_enter

    @property
    def update_on_exit(self) -> bool | None:
        """
        Is true when context manager should update offsets on exit.

        Set to true, false or none.
        """
        return self._update_on_exit


class NullContextManager(ContextManager):
    """
    A context manager that does nothing.
    """

    __documentation_section__ = "Context managers"

    __slots__ = ()

    def __init__(self):
        pass

    def __enter__(self) -> None:
        """
        Enters context manager and does nothing.
        """
        pass

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager and does nothing.
        """
        pass


class ProgressIndicator(ContextManager):
    """
    A context manager for printing progress indications.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = ("_is_warning", "_message", "_progress", "_total", "_verbose")

    RED = "\033[91m"
    END = "\033[0m"

    ### INITIALIZER ###

    def __init__(self, message="", total=None, verbose=True, is_warning=None):
        self._message = message
        self._progress = 0
        self._total = total
        self._verbose = bool(verbose)
        self._is_warning = bool(is_warning)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "ProgressIndicator":
        """
        Enters progress indicator.
        """
        self._print()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits progress indicator.
        """
        if self.verbose:
            print()

    def __repr__(self) -> str:
        """
        Gets interpreter representation of context manager.

        ..  container:: example

            >>> context_manager = abjad.ProgressIndicator()
            >>> context_manager
            <ProgressIndicator()>

        """
        return f"<{type(self).__name__}()>"

    ### PRIVATE METHODS ###

    def _print(self):
        if not self.verbose:
            return
        message = self.message or "Progress"
        if self.total is not None:
            message = f"{message}: {self.progress} / {self.total}"
        else:
            message = f"{message}: {self.progress}"
        if self.is_warning and self.progress:
            message = self.RED + message + self.END
        print(message, end="")

    ### PUBLIC METHODS ###

    def advance(self):
        """
        Advances the progress indicator's progress count.  Overwrites
        the current terminal line with the progress indicators message and new
        count.
        """
        self._progress += 1
        if self.verbose:
            sys.stdout.flush()
            print("\r", end="")
        self._print()

    ### PUBLIC PROPERTIES ###

    @property
    def is_warning(self) -> bool:
        """
        Is true if progress indicator prints in red when its progress goes above zero.
        """
        return self._is_warning

    @property
    def message(self) -> str:
        """
        Gets message of progress indicator.
        """
        return self._message

    @property
    def progress(self) -> int:
        """
        Gets progress.
        """
        return self._progress

    @property
    def total(self) -> int | None:
        """
        Gets total count.
        """
        return self._total

    @property
    def verbose(self) -> bool:
        """
        Is true if progress indicator prints status.
        """
        return self._verbose


class RedirectedStreams(ContextManager):
    """
    A context manager for capturing stdout and stderr output.

    ..  container:: example

        >>> abjad.RedirectedStreams()
        <RedirectedStreams()>

        >>> from io import StringIO
        >>> string_io = StringIO()
        >>> with abjad.RedirectedStreams(stdout=string_io):
        ...     print("hello, world!")
        ...
        >>> result = string_io.getvalue()
        >>> string_io.close()
        >>> print(result)
        hello, world!
        <BLANKLINE>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = ("_stdout", "_stderr", "_old_stderr", "_old_stdout")

    ### INITIALIZER ###

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    ### SPECIAL METHODS ###

    def __enter__(self) -> "RedirectedStreams":
        """
        Enters redirected streams context manager.
        """
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits redirected streams context manager.
        """
        try:
            self._stdout.flush()
            self._stderr.flush()
        except Exception:
            pass
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def __repr__(self) -> str:
        """
        Gets interpreter representation of context manager.

        ..  container:: example

            >>> context_manager = abjad.RedirectedStreams()
            >>> context_manager
            <RedirectedStreams()>

        """
        return super().__repr__()

    @property
    def stderr(self):
        """
        Gets stderr of context manager.
        """
        return self._stderr

    @property
    def stdout(self):
        """
        Gets stdout of context manager.
        """
        return self._stdout


class TemporaryDirectory(ContextManager):
    """
    A temporary directory context manager.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = ("_parent_directory", "_temporary_directory")

    ### INITIALIZER ###

    def __init__(self, parent_directory=None):
        self._parent_directory = parent_directory
        self._temporary_directory = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        """
        Enters context manager.

        Creates and returns path to a temporary directory.
        """
        self._temporary_directory = tempfile.mkdtemp(dir=self.parent_directory)
        return self._temporary_directory

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager.

        Deletes previously created temporary directory.
        """
        shutil.rmtree(self._temporary_directory)

    ### PUBLIC PROPERTIES ###

    @property
    def parent_directory(self) -> str:
        """
        Gets parent directory.
        """
        return self._parent_directory

    @property
    def temporary_directory(self) -> str:
        """
        Gets temporary directory.
        """
        return self._temporary_directory


class TemporaryDirectoryChange(ContextManager):
    """
    A context manager for temporarily changing the current working directory.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = ("_directory", "_original_directory", "_verbose")

    ### INITIALIZER ###

    def __init__(self, directory=None, verbose=None):
        if directory is None:
            pass
        elif isinstance(directory, pathlib.Path):
            directory = str(directory)
        elif os.path.isdir(directory):
            pass
        elif os.path.isfile(directory):
            directory = os.path.dirname(directory)
        self._directory = directory
        self._original_directory = None
        if verbose is not None:
            verbose = bool(verbose)
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "TemporaryDirectoryChange":
        """
        Enters context manager and changes to ``directory``.
        """
        self._original_directory = os.getcwd()
        if self._directory is not None:
            os.chdir(self.directory)
            if self.verbose:
                message = f"Changing directory to {self.directory} ..."
                print(message)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager and returns to original working directory.
        """
        if self._directory is not None:
            os.chdir(self._original_directory)
            if self.verbose:
                message = f"Returning to {self.original_directory} ..."
                print(message)
        self._original_directory = None

    def __repr__(self) -> str:
        """
        Gets interpreter representation of context manager.
        """
        return f"<{type(self).__name__}()>"

    ### PUBLIC PROPERTIES ###

    @property
    def directory(self) -> str:
        """
        Gets temporary directory of context manager.
        """
        return self._directory

    @property
    def original_directory(self) -> str:
        """
        Gets original directory of context manager.
        """
        return self._original_directory

    @property
    def verbose(self) -> bool:
        """
        Is true if context manager prints verbose messages on entrance and exit.
        """
        return self._verbose


class Timer(ContextManager):
    """
    A timing context manager.

    ..  container:: example

        >>> timer = abjad.Timer()
        >>> with timer:
        ...     for _ in range(1000000):
        ...         x = 1 + 1
        ...
        >>> timer.elapsed_time # doctest: +SKIP
        0.092742919921875

        The timer can also be accessed from within the ``with`` block:

        >>> with abjad.Timer() as timer: # doctest: +SKIP
        ...     for _ in range(5):
        ...         for _ in range(1000000):
        ...             x = 1 + 1
        ...         print(timer.elapsed_time)
        ...
        0.101150989532
        0.203935861588
        0.304930925369
        0.4057970047
        0.50649189949

    Timers can be reused between ``with`` blocks. They will reset their clock
    on entering any ``with`` block.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Context managers"

    __slots__ = (
        "_enter_message",
        "_exit_message",
        "_print_continuously_from_background",
        "_process",
        "_start_time",
        "_stop_time",
        "_timer_process",
        "_verbose",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        exit_message=None,
        enter_message=None,
        print_continuously_from_background=False,
        verbose=True,
    ):
        if enter_message is not None:
            enter_message = str(enter_message)
        self._enter_message = enter_message
        if exit_message is not None:
            exit_message = str(exit_message)
        self._exit_message = exit_message
        self._print_continuously_from_background = print_continuously_from_background
        self._process = None
        self._timer_process = None
        self._start_time = None
        self._stop_time = None
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self) -> "Timer":
        """
        Enters context manager.
        """
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        if self.print_continuously_from_background:
            path = configuration.abjad_directory.parent / "scripts" / "timer.py"
            interval = str(int(self.print_continuously_from_background))
            process = subprocess.Popen([path, interval], shell=False)
            self._process = process
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exit context manager.
        """
        self._stop_time = time.time()
        if self._process is not None:
            self._process.kill()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self) -> float | None:
        """
        Elapsed time.
        """
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self) -> str:
        """
        Timer enter message.
        """
        return self._enter_message

    @property
    def exit_message(self) -> str:
        """
        Timer exit message.
        """
        return self._exit_message

    @property
    def print_continuously_from_background(self) -> bool:
        """
        Is true when timer should print continuously from background.
        """
        return self._print_continuously_from_background

    @property
    def start_time(self):
        """
        Start time of timer.

        Returns time.
        """
        return self._start_time

    @property
    def stop_time(self):
        """
        Stop time of timer.

        Returns time.
        """
        return self._stop_time

    @property
    def total_time_message(self) -> str:
        """
        Gets total time message.

        Truncated to the nearest second.
        """
        assert self.elapsed_time is not None
        identifier = _string.pluralize("second", int(self.elapsed_time))
        message = f"total time {int(self.elapsed_time)} {identifier} ..."
        return message

    @property
    def verbose(self) -> bool:
        """
        Is true if timer should print messages.
        """
        return self._verbose
