from abjad.utilities import Infinity, NegativeInfinity
from .Timespan import Timespan


class AnnotatedTimespan(Timespan):
    """
    Annotated timespan.

    ..  container:: example

        >>> annotated_timespan = abjad.AnnotatedTimespan(
        ...    annotation=['a', 'b', 'c'],
        ...    start_offset=(1, 4),
        ...    stop_offset=(7, 8),
        ...    )
        >>> abjad.f(annotated_timespan)
        abjad.AnnotatedTimespan(
            start_offset=abjad.Offset(1, 4),
            stop_offset=abjad.Offset(7, 8),
            annotation=['a', 'b', 'c'],
            )

    Annotated timespans maintain their annotations duration mutation:

    ..  container:: example

        >>> left, right = annotated_timespan.split_at_offset((1, 2))
        >>> left.annotation.append('foo')
        >>> abjad.f(right)
        abjad.AnnotatedTimespan(
            start_offset=abjad.Offset(1, 2),
            stop_offset=abjad.Offset(7, 8),
            annotation=['a', 'b', 'c', 'foo'],
            )

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Timespans'

    __slots__ = (
        '_annotation',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_offset=NegativeInfinity,
        stop_offset=Infinity,
        annotation=None,
        ):
        Timespan.__init__(
            self,
            start_offset=start_offset,
            stop_offset=stop_offset,
            )
        self._annotation = annotation

    ### PUBLIC PROPERTIES ###

    @property
    def annotation(self):
        """
        Gets and sets annotated timespan annotation.

        ..  container:: example

            Gets annotation:

            >>> annotated_timespan = abjad.AnnotatedTimespan(
            ...    annotation=['a', 'b', 'c', 'foo'],
            ...    start_offset=(1, 4),
            ...    stop_offset=(7, 8),
            ...    )
            >>> annotated_timespan.annotation
            ['a', 'b', 'c', 'foo']

        ..  container:: example

            Sets annotation:

            >>> annotated_timespan.annotation = 'baz'

        Returns arbitrary object.
        """
        return self._annotation

    @annotation.setter
    def annotation(self, argument):
        self._annotation = argument
