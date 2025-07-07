"""
Context managers.
"""

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
from . import score as _score
from . import string as _string

_Configuration = _configuration.Configuration()


class FilesystemState:
    """
    Filesystem state context manager.
    """

    __slots__ = ("_keep", "_remove")
    _is_abstract = True

    def __init__(
        self,
        *,
        keep: list[pathlib.Path] | None = None,
        remove: list[pathlib.Path] | None = None,
    ):
        keep = keep or []
        keep_tuple = tuple([str(_) for _ in keep])
        self._keep = keep_tuple
        remove = remove or []
        remove_tuple = tuple([str(_) for _ in remove])
        self._remove = remove_tuple

    def __enter__(self) -> "FilesystemState":
        """
        Backs up filesystem paths.
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
        Restores filesytem paths and removes backups; also removes paths in
        remove list.
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
    def keep(self) -> tuple[str, ...]:
        """
        Gets paths to restore on exit.
        """
        return self._keep

    @property
    def remove(self) -> tuple[str, ...]:
        """
        Gets paths to remove on exit.
        """
        return self._remove


class ForbidUpdate:
    """
    Forbid update context manager.
    """

    __slots__ = ("_component", "_update_on_exit")
    _is_abstract = True

    def __init__(self, component: _score.Component, *, update_on_exit: bool = False):
        assert isinstance(component, _score.Component), repr(component)
        self._component = component
        assert isinstance(update_on_exit, bool), repr(update_on_exit)
        self._update_on_exit = update_on_exit

    def __enter__(self) -> "ForbidUpdate":
        r"""
        Enters context manager.

        ..  container:: example

            REGRESSION. Indicators need to be updated after swap; context
            manager updates indicators before forbidding further updates:

            >>> staff = abjad.Staff(r"\tuplet 1/1 { c'4 d' }")
            >>> abjad.attach(abjad.Clef("alto"), staff[0][0])
            >>> container = abjad.Container()
            >>> abjad.mutate.swap(staff[0], container)
            >>> with abjad.contextmanagers.ForbidUpdate(staff):
            ...     for note in staff[0]:
            ...         print(note)
            ...         print(abjad.get.effective_indicator(note, abjad.Clef))
            ...
            Note("c'4")
            Clef(name='alto', hide=False)
            Note("d'4")
            Clef(name='alto', hide=False)

        """
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
        self.component._is_forbidden_to_update = False
        if self.update_on_exit is True:
            for component_ in _iterate.components(self.component):
                _updatelib._update_now(
                    component_,
                    indicators=True,
                    offsets=True,
                    offsets_in_seconds=True,
                )
        else:
            assert self.update_on_exit is False

    @property
    def component(self) -> _score.Component:
        """
        Gets component.
        """
        return self._component

    @property
    def update_on_exit(self) -> bool:
        """
        Is true when context manager updates offsets on exit.
        """
        return self._update_on_exit


class NullContextManager:
    """
    Null context manager.
    """

    __slots__ = ()
    _is_abstract = True

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


# TODO: typehint
class RedirectedStreams:
    """
    Redirected streams context manager.

    ..  container:: example

        Captures stdout and stderr output:

        >>> import io
        >>> string_io = io.StringIO()
        >>> with abjad.contextmanagers.RedirectedStreams(stdout=string_io):
        ...     print("hello, world!")
        ...
        >>> result = string_io.getvalue()
        >>> string_io.close()
        >>> print(result)
        hello, world!
        <BLANKLINE>

    """

    __slots__ = ("_stdout", "_stderr", "_old_stderr", "_old_stdout")
    _is_abstract = True

    def __init__(self, *, stdout=None, stderr=None):
        if stdout is None:
            self._stdout = sys.stdout
        else:
            self._stdout = stdout
        if stderr is None:
            self._stderr = sys.stderr
        else:
            self._stderr = stderr

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

    # TODO: typehint
    @property
    def stderr(self):
        """
        Gets stderr of context manager.
        """
        return self._stderr

    # TODO: typehint
    @property
    def stdout(self):
        """
        Gets stdout of context manager.
        """
        return self._stdout


# TODO: remove in favor of something in standard library?
class TemporaryDirectory:
    """
    Temporary directory context manager.
    """

    __slots__ = ("_parent_directory", "_temporary_directory")

    _is_abstract = True

    def __init__(self, parent_directory=None):
        self._parent_directory = parent_directory
        self._temporary_directory = None

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


class TemporaryDirectoryChange:
    """
    Temporary directory change context manager.
    """

    __slots__ = ("_directory", "_original_directory", "_verbose")

    _is_abstract = True

    def __init__(self, directory=None, *, verbose: bool = False):
        if directory is None:
            pass
        elif isinstance(directory, pathlib.Path):
            directory = str(directory)
        elif os.path.isdir(directory):
            pass
        elif os.path.isfile(directory):
            directory = os.path.dirname(directory)
        self._directory = directory
        self._original_directory: str | None = None
        assert isinstance(verbose, bool), repr(verbose)
        self._verbose = verbose

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
            assert self._original_directory is not None
            os.chdir(self._original_directory)
            if self.verbose:
                message = f"Returning to {self.original_directory} ..."
                print(message)
        self._original_directory = None

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
        assert self._original_directory is not None
        return self._original_directory

    @property
    def verbose(self) -> bool:
        """
        Is true if context manager prints verbose messages on entrance and exit.
        """
        return self._verbose


class Timer:
    """
    Timer context manager.

    ..  container:: example

        Prints elapsed time after timer finishes:

        >>> timer = abjad.contextmanagers.Timer()
        >>> with timer:
        ...     for _ in range(1000000):
        ...         x = 1 + 1
        ...
        >>> timer.elapsed_time # doctest: +SKIP
        0.092742919921875

    ..  container:: example

        Prints elapsed time while timer is running:

        >>> with abjad.contextmanagers.Timer() as timer: # doctest: +SKIP
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

        Timers can be reused between with-blocks.

    """

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

    _is_abstract = True

    def __init__(
        self,
        *,
        enter_message: str = "",
        exit_message: str = "",
        print_continuously_from_background: bool = False,
        verbose: bool = True,
    ):
        assert isinstance(enter_message, str), repr(enter_message)
        self._enter_message = enter_message
        assert isinstance(exit_message, str), repr(exit_message)
        self._exit_message = exit_message
        self._print_continuously_from_background = print_continuously_from_background
        self._process: subprocess.Popen | None = None
        self._timer_process = None
        self._start_time: float | None = None
        self._stop_time: float | None = None
        assert isinstance(verbose, bool), repr(verbose)
        self._verbose = bool(verbose)

    def __enter__(self) -> "Timer":
        """
        Enters context manager.
        """
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        if self.print_continuously_from_background:
            path = (
                _Configuration.abjad_install_directory().parent / "scripts" / "timer.py"
            )
            interval = str(int(self.print_continuously_from_background))
            process = subprocess.Popen([path, interval], shell=False)
            self._process = process
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager.
        """
        self._stop_time = time.time()
        if self._process is not None:
            self._process.kill()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    @property
    def elapsed_time(self) -> float | None:
        """
        Gets elapsed time of timer.
        """
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self) -> str:
        """
        Gets timer enter message.
        """
        return self._enter_message

    @property
    def exit_message(self) -> str:
        """
        Gets timer exit message.
        """
        return self._exit_message

    @property
    def print_continuously_from_background(self) -> bool:
        """
        Is true when timer prints continuously from background.
        """
        return self._print_continuously_from_background

    @property
    def start_time(self) -> float | None:
        """
        Gets start time of timer.
        """
        return self._start_time

    @property
    def stop_time(self) -> float | None:
        """
        Gets stop time of timer.
        """
        return self._stop_time

    @property
    def total_time_message(self) -> str:
        """
        Gets total time message, truncated to nearest second.
        """
        assert self.elapsed_time is not None
        identifier = _string.pluralize("second", int(self.elapsed_time))
        message = f"total time {int(self.elapsed_time)} {identifier} ..."
        return message

    @property
    def verbose(self) -> bool:
        """
        Is true when timer prints messages.
        """
        return self._verbose
