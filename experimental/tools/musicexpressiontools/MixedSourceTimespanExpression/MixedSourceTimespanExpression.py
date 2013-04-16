from abjad.tools import abctools
from experimental.tools.musicexpressiontools.TimespanExpression import TimespanExpression


class MixedSourceTimespanExpression(TimespanExpression):
    r'''Mixed-source timespan expression.

    Definitions:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')

    Example. Mixed-source timespan starting at the left edge of the last measure
    that starts during segment ``'red'``
    and stoppding at the right edge of the first measure
    that starts during segment ``'blue'``:

    ::

        >>> measure = red_segment.select_measures('Voice 1')[-1:]
        >>> start_offset = measure.start_offset

    ::

        >>> measure = blue_segment.select_measures('Voice 1')[:1]
        >>> stop_offset = measure.stop_offset

    ::

        >>> timespan = musicexpressiontools.MixedSourceTimespanExpression(start_offset, stop_offset)

    ::

        >>> z(timespan)
        musicexpressiontools.MixedSourceTimespanExpression(
            start_offset=musicexpressiontools.OffsetExpression(
                anchor=musicexpressiontools.MeasureSelectExpression(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=musicexpressiontools.CallbackInventory([
                        'result = self._getitem__(payload_expression, slice(-1, None, None))'
                        ])
                    )
                ),
            stop_offset=musicexpressiontools.OffsetExpression(
                anchor=musicexpressiontools.MeasureSelectExpression(
                    anchor='blue',
                    voice_name='Voice 1',
                    callbacks=musicexpressiontools.CallbackInventory([
                        'result = self._getitem__(payload_expression, slice(None, 1, None))'
                        ])
                    ),
                edge=Right
                )
            )

    Mixed-source timespan expressions are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None, callbacks=None):
        from experimental.tools import musicexpressiontools
        assert isinstance(start_offset, (musicexpressiontools.OffsetExpression, type(None))), repr(start_offset)
        assert isinstance(stop_offset, (musicexpressiontools.OffsetExpression, type(None))), repr(stop_offset)
        TimespanExpression.__init__(self, callbacks=callbacks)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### PRIVATE METHODS ###

    def evaluate(self):
        '''Evaluate mixed-suorce timespan expression.

        Not yet implemented.
        '''
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Mixed-source timespan expression start offset.

        Return offset expression.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Mixed-source timespan expression stop offset.

        Return offset expression.
        '''
        return self._stop_offset
