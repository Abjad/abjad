import os
import subprocess
import time
from .ContextManager import ContextManager


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

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_enter_message',
        '_exit_message',
        '_print_continuously_from_background',
        '_process',
        '_start_time',
        '_stop_time',
        '_timer_process',
        '_verbose',
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
        self._print_continuously_from_background = \
            print_continuously_from_background
        self._process = None
        self._timer_process = None
        self._start_time = None
        self._stop_time = None
        self._verbose = bool(verbose)

    ### SPECIAL METHODS ###

    def __enter__(self):
        """
        Enters context manager.

        Returns context manager.
        """
        if self.enter_message and self.verbose:
            print(self.enter_message)
        self._stop_time = None
        self._start_time = time.time()
        if self.print_continuously_from_background:
            from abjad import abjad_configuration
            path = os.path.join(
                abjad_configuration.abjad_directory,
                'scr',
                'timer.py',
                )
            interval = str(int(self.print_continuously_from_background))
            process = subprocess.Popen([path, interval], shell=False)
            self._process = process
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exist context manager.

        Returns none.
        """
        self._stop_time = time.time()
        if self._process is not None:
            self._process.kill()
        if self.exit_message and self.verbose:
            print(self.exit_message, self.elapsed_time)

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self):
        """
        Elapsed time.

        Return float or none.
        """
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def enter_message(self):
        """
        Timer enter message.

        Returns string.
        """
        return self._enter_message

    @property
    def exit_message(self):
        """
        Timer exit message.

        Returns string.
        """
        return self._exit_message

    @property
    def print_continuously_from_background(self):
        """
        Is true when timer should print continuously from background.

        Returns true or false.
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
    def total_time_message(self):
        """
        Gets total time message.

        Truncated to the nearest second.

        Returns string.
        """
        import abjad
        identifier = abjad.String('second').pluralize(int(self.elapsed_time))
        message = 'total time {} {} ...'
        message = message.format(int(self.elapsed_time), identifier)
        return message

    @property
    def verbose(self):
        """
        Is true if timer should print messages.

        Returns true or false.
        """
        return self._verbose
