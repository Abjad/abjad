import sys
from .ContextManager import ContextManager


class RedirectedStreams(ContextManager):
    """
    A context manager for capturing stdout and stderr output.

    ..  container:: example

        >>> from io import StringIO
        >>> string_io = StringIO()
        >>> with abjad.RedirectedStreams(stdout=string_io):
        ...     print("hello, world!")
        ...
        >>> result = string_io.getvalue()
        >>> string_io.close()
        >>> print(result)
        hello, world!

    Redirected streams context manager is immutable.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Context managers'

    __slots__ = (
        '_stdout',
        '_stderr',
        '_old_stderr',
        '_old_stdout',
        )

    ### INITIALIZER ###

    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    ### SPECIAL METHODS ###

    def __enter__(self):
        """
        Enters redirected streams context manager.

        Returns none.
        """
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exits redirected streams context manager.

        Returns none.
        """
        try:
            self._stdout.flush()
            self._stderr.flush()
        except:
            pass
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def __repr__(self):
        """
        Gets interpreter representation of context manager.

        ..  container:: example

            >>> context_manager = abjad.RedirectedStreams()
            >>> context_manager
            <RedirectedStreams()>

        Returns string.
        """
        return super().__repr__()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad import system
        return system.FormatSpecification(
            self,
            repr_is_bracketed=True,
            repr_is_indented=False,
            storage_format_is_bracketed=True,
            storage_format_is_indented=False,
            storage_format_args_values=[],
            storage_format_kwargs_names=[],
            )

    ### PUBLIC PROPERTIES ###

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
