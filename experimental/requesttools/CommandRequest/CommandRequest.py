from experimental import symbolictimetools
from experimental.requesttools.Request import Request


class CommandRequest(Request):
    r'''.. versionadded:: 1.0

    Request `attribute` command active at `symbolic_offset` in `context_name`::

        >>> from experimental import *

    Example. Request division command active at start of measure 4 in ``'Voice 1'``::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(
        ...     staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    ::

        >>> selector = red_segment.select_background_measure_timespan(4, 5)
        >>> command_request = red_segment.request_division_command(
        ...     'Voice 1', selector=selector)

    ::

        >>> z(command_request)
        requesttools.CommandRequest(
            'divisions',
            symbolictimetools.SymbolicOffset(
                selector=symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    start_identifier=4,
                    stop_identifier=5,
                    time_relation=timerelationtools.TimespanTimespanTimeRelation(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                            selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                                identifier='red'
                                )
                            )
                        )
                    )
                ),
                context_name='Voice 1'
            )

    Command requested is canonically assumed to be a list or other iterable.

    Because of this the request affords list-manipulation attributes.
    These are `index`, `count`, `reverse`, `callback`.

    Purpose of a command request is to function as a setting source.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, symbolic_offset, context_name=None, 
        index=None, count=None, reverse=None, rotation=None, callback=None):
        assert attribute in self.attributes, repr(attribute)
        assert isinstance(symbolic_offset, symbolictimetools.SymbolicOffset)
        assert isinstance(context_name, (str, type(None))), repr(context_name)
        Request.__init__(self, index=index, count=count, reverse=reverse, rotation=rotation, callback=callback)
        self._attribute = attribute
        self._symbolic_offset = symbolic_offset
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def attribute(self):
        '''Command request attribute specified by user.

            >>> command_request.attribute
            'divisions'

        Return string.
        '''
        return self._attribute

    @property
    def context_name(self):
        '''Command request context name specified by user.

            >>> command_request.context_name
            'Voice 1'

        Return string.
        '''
        return self._context_name

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.symbolic_offset.start_segment_identifier``.

            >>> command_request.start_segment_identifier
            'red'

        Return string or none.
        '''
        return self.symbolic_offset.start_segment_identifier

    @property
    def symbolic_offset(self):
        '''Command request symbolic offset specified by user.

            >>> z(command_request.symbolic_offset)
            symbolictimetools.SymbolicOffset(
                selector=symbolictimetools.BackgroundMeasureSymbolicTimespan(
                    start_identifier=4,
                    stop_identifier=5,
                    time_relation=timerelationtools.TimespanTimespanTimeRelation(
                        'timespan_1.start <= timespan_2.start < timespan_1.stop',
                        timespan_1=symbolictimetools.SingleSourceSymbolicTimespan(
                            selector=symbolictimetools.SingleSegmentSymbolicTimespan(
                                identifier='red'
                                )
                            )
                        )
                    )
                )

        Return symbolic_offset.
        '''
        return self._symbolic_offset
