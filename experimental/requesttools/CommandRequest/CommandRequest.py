from experimental import timespantools
from experimental.requesttools.Request import Request


class CommandRequest(Request):
    r'''.. versionadded:: 1.0

    Request `attribute` command active at `timepoint` in `context_name`::

        >>> from experimental import *

    Example. Request division command active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.append_segment(name='red')

    ::

        >>> selector = segment.select_background_measure(4)
        >>> command_request = segment.request_division_command(
        ...     context_name='Voice 1', selector=selector)

    ::

        >>> z(command_request)
        requesttools.CommandRequest(
            'divisions',
            timespantools.SymbolicTimepoint(
                selector=selectortools.BackgroundMeasureSelector(
                    inequality=timespaninequalitytools.TimespanInequality(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=timespantools.SingleSourceSymbolicTimespan(
                            selector=selectortools.SingleSegmentSelector(
                                identifier='red'
                                )
                            )
                        ),
                    start_identifier=4,
                    stop_identifier=5
                    )
                ),
                context_name='Voice 1'
            )

    Command requested is canonically assumed to be a list or other iterable.

    Because of this the request affords list-manipulation attributes.
    These are `offset`, `count`, `reverse`, `callback`.

    Purpose of a command request is to function as a setting source.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, timepoint,
        context_name=None, offset=None, count=None, reverse=None, callback=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(timepoint, timespantools.SymbolicTimepoint)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        Request.__init__(self, callback=callback, count=count, offset=offset, reverse=reverse)
        self._attribute = attribute
        self._timepoint = timepoint
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Command request attribute specified by user.

        Return string.
        '''
        return self._attribute

    @property
    def context_name(self):
        '''Command request context name specified by user.

        Return string.
        '''
        return self._context_name

    @property
    def segment_identifier(self):
        '''Delegate to ``self.timepoint.segment_identifier``.

        Return string or none.
        '''
        return self.timepoint.segment_identifier

    @property
    def timepoint(self):
        '''Command request timepoint specified by user.

        Return timepoint.
        '''
        return self._timepoint
