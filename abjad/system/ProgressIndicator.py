import sys
from .ContextManager import ContextManager


class ProgressIndicator(ContextManager):
    """
    A context manager for printing progress indications.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_is_warning',
        '_message',
        '_progress',
        '_total',
        '_verbose',
        )

    RED = '\033[91m'
    END = '\033[0m'

    ### INITIALIZER ###

    def __init__(
        self,
        message='',
        total=None,
        verbose=True,
        is_warning=None,
        ):
        self._message = message
        self._progress = 0
        self._total = total
        self._verbose = bool(verbose)
        self._is_warning = bool(is_warning)

    ### SPECIAL METHODS ###

    def __enter__(self):
        """
        Enters progress indicator.
        """
        self._print()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits progress indicator.
        """
        if self.verbose:
            print()

    def __repr__(self):
        """
        Gets interpreter representation of context manager.

        ..  container:: example

            >>> context_manager = abjad.ProgressIndicator()
            >>> context_manager
            <ProgressIndicator()>

        Returns string.
        """
        return '<{}()>'.format(type(self).__name__)

    ### PRIVATE METHODS ###

    def _print(self):
        if not self.verbose:
            return
        message = self.message or 'Progress'
        if self.total is not None:
            message = '{}: {} / {}'.format(
                message,
                self.progress,
                self.total,
                )
        else:
            message = '{}: {}'.format(
                message,
                self.progress,
                )
        if self.is_warning and self.progress:
            message = self.RED + message + self.END
        print(message, end='')

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
            print('\r', end='')
        self._print()

    ### PUBLIC PROPERTIES ###

    @property
    def is_warning(self):
        """
        Is true if progress indicator prints in red when its progress goes
        above zero.

        Returns true or false.
        """
        return self._is_warning

    @property
    def message(self):
        """
        Gets message of progress indicator.

        Returns string.
        """
        return self._message

    @property
    def progress(self):
        """
        Gets progress.

        Returns integer.
        """
        return self._progress

    @property
    def total(self):
        """
        Gets total count.

        Returns integer or none.
        """
        return self._total

    @property
    def verbose(self):
        """
        Is true if progress indicator prints status.

        Returns true or false.
        """
        return self._verbose
