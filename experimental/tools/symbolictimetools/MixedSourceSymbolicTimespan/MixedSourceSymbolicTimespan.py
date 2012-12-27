from abjad.tools import abctools
from experimental.tools.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class MixedSourceSymbolicTimespan(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

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

        >>> measure = red_segment.select_background_measures('Voice 1')[-1:]
        >>> start_offset = symbolictimetools.SymbolicOffset(anchor=measure)

    ::

        >>> measure = blue_segment.select_background_measures('Voice 1')[:1]
        >>> stop_offset = symbolictimetools.SymbolicOffset(anchor=measure, edge=Right)
        
    ::

        >>> timespan = symbolictimetools.MixedSourceSymbolicTimespan(
        ... start_offset=start_offset, stop_offset=stop_offset)

    ::

        >>> z(timespan)
        symbolictimetools.MixedSourceSymbolicTimespan(
            start_offset=symbolictimetools.SymbolicOffset(
                anchor=symbolictimetools.BackgroundMeasureSelector(
                    anchor='red',
                    voice_name='Voice 1',
                    modifications=datastructuretools.ObjectInventory([
                        'result = self.___getitem__(elements, start_offset, slice(-1, None, None))'
                        ])
                    )
                ),
            stop_offset=symbolictimetools.SymbolicOffset(
                anchor=symbolictimetools.BackgroundMeasureSelector(
                    anchor='blue',
                    voice_name='Voice 1',
                    modifications=datastructuretools.ObjectInventory([
                        'result = self.___getitem__(elements, start_offset, slice(None, 1, None))'
                        ])
                    ),
                edge=Right
                )
            )

    Mixed-source symbolic timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, start_offset=None, stop_offset=None, timespan_modifications=None):
        from experimental.tools import specificationtools
        from experimental.tools import symbolictimetools
        assert isinstance(start_offset, (symbolictimetools.SymbolicOffset, type(None))), repr(start_offset)
        assert isinstance(stop_offset, (symbolictimetools.SymbolicOffset, type(None))), repr(stop_offset)
        SymbolicTimespan.__init__(self, timespan_modifications=timespan_modifications)
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when `expr` equals self. Otherwise false.

        Return boolean.
        '''
        if isintance(expr, type(self)):
            if self.start_offset == timespan_2.start_offset:
                if self.stop_offset == timespan_2.stop_offset:
                    return True
        return False

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, context_name):
        '''Evaluate start and stop offsets of symbolic timespan when applied
        to `context_name` in `score_specification`.

        .. note:: not yet implemented.

        Return pair.
        '''
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
