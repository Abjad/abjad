from experimental.interpretertools.DivisionCommand import DivisionCommand
import fractions


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    # TODO: change 'value' to 'resolved_value'
    def __init__(self, 
        value, duration, start_segment_name, start_offset, stop_offset, context_name, fresh, truncate):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(context_name, (str, type(None)))
        #assert stop_offset - start_offset == duration, repr((stop_offset, start_offset, duration))
        DivisionCommand.__init__(
            self, value, duration, start_segment_name, start_offset, stop_offset, context_name)
        self._fresh = fresh
        self._truncate = truncate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''Not yet implemented.
        '''
        return self._fresh

    @property
    def truncate(self):
        '''Not yet implemented.
        '''
        return self._truncate
