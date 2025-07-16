"""
Context managers.
"""

import contextlib
import filecmp
import os
import pathlib
import shutil
import subprocess
import sys
import time
import types
import typing

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
        for path in self.remove():
            assert not os.path.exists(path), repr(path)
        for path in self.keep():
            assert os.path.exists(path), repr(path)
            assert os.path.isfile(path) or os.path.isdir(path), repr(path)
        for path in self.keep():
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
        backup_paths = (_ + ".backup" for _ in self.keep())
        for path in backup_paths:
            assert os.path.exists(path), repr(path)
        for path in self.keep():
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
        for path in self.remove():
            if os.path.exists(path):
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    raise TypeError(f"neither file nor directory: {path}.")
        for path in self.keep():
            assert os.path.exists(path), repr(path)
        for path in backup_paths:
            assert not os.path.exists(path), repr(path)

    def keep(self) -> tuple[str, ...]:
        """
        Gets paths to restore on exit.
        """
        return self._keep

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
            Clef(name='alto')
            Note("d'4")
            Clef(name='alto')

        """
        for component_ in _iterate.components(self.component()):
            _updatelib._update_now(
                component_, indicators=True, offsets=True, offsets_in_seconds=True
            )
        self.component()._is_forbidden_to_update = True
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Exits context manager.
        """
        self.component()._is_forbidden_to_update = False
        if self.update_on_exit() is True:
            for component_ in _iterate.components(self.component()):
                _updatelib._update_now(
                    component_,
                    indicators=True,
                    offsets=True,
                    offsets_in_seconds=True,
                )
        else:
            assert self.update_on_exit() is False

    def component(self) -> _score.Component:
        """
        Gets component.
        """
        return self._component

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

    def __init__(
        self,
        *,
        stdout: typing.TextIO | None = None,
        stderr: typing.TextIO | None = None,
    ):
        if stdout is None:
            self._stdout = sys.stdout
        else:
            self._stdout = stdout
        if stderr is None:
            self._stderr = sys.stderr
        else:
            self._stderr = stderr

    def __enter__(self) -> "RedirectedStreams":
        """
        Enters redirected streams context manager.
        """
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self.stdout(), self.stderr()
        return self

    def __exit__(
        self,
        exc_type: typing.Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        """
        Exits redirected streams context manager.
        """
        try:
            self.stdout().flush()
            self.stderr().flush()
        except Exception:
            pass
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def stderr(self) -> typing.TextIO:
        """
        Gets stderr of context manager.
        """
        return self._stderr

    def stdout(self) -> typing.TextIO:
        """
        Gets stdout of context manager.
        """
        return self._stdout


@contextlib.contextmanager
def temporary_directory_change(directory: str | os.PathLike) -> typing.Iterator[None]:
    """
    Temporary directory change context manager.
    """
    original_directory = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(original_directory)


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
        >>> timer.elapsed_time() # doctest: +SKIP
        0.092742919921875

    ..  container:: example

        Prints elapsed time while timer is running; timers can be reused
        between with-blocks:

        >>> with abjad.contextmanagers.Timer() as timer: # doctest: +SKIP
        ...     for _ in range(5):
        ...         for _ in range(1000000):
        ...             x = 1 + 1
        ...         print(timer.elapsed_time())
        ...
        0.101150989532
        0.203935861588
        0.304930925369
        0.4057970047
        0.50649189949

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
        if self.enter_message() and self.verbose():
            print(self.enter_message())
        self._stop_time = None
        self._start_time = time.time()
        if self.print_continuously_from_background():
            path = (
                _Configuration.abjad_install_directory().parent / "scripts" / "timer.py"
            )
            interval = str(int(self.print_continuously_from_background()))
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
        if self.exit_message() and self.verbose():
            print(self.exit_message(), self.total_time_message())

    def elapsed_time(self) -> float:
        """
        Gets elapsed time of timer.
        """
        start_time, stop_time = self.start_time(), self.stop_time()
        if start_time is not None:
            if stop_time is not None:
                return stop_time - start_time
            return time.time() - start_time
        return 0

    def enter_message(self) -> str:
        """
        Gets timer enter message.
        """
        return self._enter_message

    def exit_message(self) -> str:
        """
        Gets timer exit message.
        """
        return self._exit_message

    def print_continuously_from_background(self) -> bool:
        """
        Is true when timer prints continuously from background.
        """
        return self._print_continuously_from_background

    def start_time(self) -> float | None:
        """
        Gets start time of timer.
        """
        return self._start_time

    def stop_time(self) -> float | None:
        """
        Gets stop time of timer.
        """
        return self._stop_time

    def total_time_message(self) -> str:
        """
        Gets total time message, truncated to nearest second.
        """
        identifier = _string.pluralize("second", int(self.elapsed_time()))
        message = f"total time {int(self.elapsed_time())} {identifier} ..."
        return message

    def verbose(self) -> bool:
        """
        Is true when timer prints messages.
        """
        return self._verbose
