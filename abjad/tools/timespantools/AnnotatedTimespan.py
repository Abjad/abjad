# -*- coding: utf-8 -*-
from abjad.tools.timespantools.Timespan import Timespan


class AnnotatedTimespan(Timespan):
    r'''An annotated timespan.

    ::

        >>> annotated_timespan = timespantools.AnnotatedTimespan(
        ...    annotation=['a', 'b', 'c'],
        ...    start_offset=Offset(1, 4),
        ...    stop_offset=Offset(7, 8),
        ...    )
        >>> print(format(annotated_timespan))
        timespantools.AnnotatedTimespan(
            start_offset=durationtools.Offset(1, 4),
            stop_offset=durationtools.Offset(7, 8),
            annotation=['a', 'b', 'c'],
            )

    Annotated timespans maintain their annotations duration mutation:

    ::

        >>> left, right = annotated_timespan.split_at_offset(Offset(1, 2))
        >>> left.annotation.append('foo')
        >>> print(format(right))
        timespantools.AnnotatedTimespan(
            start_offset=durationtools.Offset(1, 2),
            stop_offset=durationtools.Offset(7, 8),
            annotation=['a', 'b', 'c', 'foo'],
            )

    '''

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
        r'''Gets and sets annotated timespan annotation.

        ..  container:: example

            Gets annotation:

            ::

                >>> annotated_timespan.annotation
                ['a', 'b', 'c', 'foo']

        ..  container:: example

            Sets annotation:

            ::

                >>> annotated_timespan.annotation = 'baz'

        Returns arbitrary object.
        '''
        return self._annotation

    @annotation.setter
    def annotation(self, expr):
        self._annotation = expr
