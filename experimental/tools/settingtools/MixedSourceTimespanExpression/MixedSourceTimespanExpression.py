from abjad.tools import abctools
from experimental.tools.settingtools.TimespanExpression import TimespanExpression


class MixedSourceTimespanExpression(TimespanExpression):
    r'''Mixed-source timespan expression.

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
        >>> blue_segment = score_specification.append_segment(name='blue')

    Mixed-source timespan.

    Mixed-source timespan starting at the left edge of the last measure
    that starts during segment ``'red'``
    and stoppding at the right edge of the first measure 
    that starts during segment ``'blue'``::

        >>> measure = red_segment.select_measures('Voice 1')[-1:]
        >>> start_offset = measure.start_offset

    ::

        >>> measure = blue_segment.select_measures('Voice 1')[:1]
        >>> stop_offset = measure.stop_offset
        
    ::

        >>> timespan = settingtools.MixedSourceTimespanExpression(start_offset, stop_offset)

    ::

        >>> z(timespan)
        settingtools.MixedSourceTimespanExpression(
            start_offset=settingtools.OffsetExpression(
                anchor=selectortools.MeasureSelector(
                    anchor='red',
                    voice_name='Voice 1',
                    callbacks=settingtools.CallbackInventory([
                        'result = self.___getitem__(expr, start_offset, slice(-1, None, None))'
                        ])
                    )
                ),
            stop_offset=settingtools.OffsetExpression(
                anchor=selectortools.MeasureSelector(
                    anchor='blue',
                    voice_name='Voice 1',
                    callbacks=settingtools.CallbackInventory([
                        'result = self.___getitem__(expr, start_offset, slice(None, 1, None))'
                        ])
                    ),
                edge=Right
                )
            )

    Mixed-source timespan expression properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None, callbacks=None):
        from experimental.tools import specificationtools
        from experimental.tools import settingtools
        assert isinstance(start_offset, (settingtools.OffsetExpression, type(None))), repr(start_offset)
        assert isinstance(stop_offset, (settingtools.OffsetExpression, type(None))), repr(stop_offset)
        TimespanExpression.__init__(self, callbacks=callbacks)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` equals self. Otherwise false.

        Return boolean.
        '''
        if isintance(expr, type(self)):
            return self.is_congruent_to_expr(expr)
        return False

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification, context_name):
        raise NotImplementedError

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start_offset(self):
        '''Mixed-source timespan start offset specified by user.

        Return offset or none.
        '''
        return self._start_offset

    @property
    def stop_offset(self):
        '''Mixed-source timepsan stop offset specified by user.

        Return offset or none.
        '''
        return self._stop_offset
