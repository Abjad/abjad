from experimental.interpretertools.DivisionCommand import DivisionCommand
import fractions


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, value, duration, start_offset, stop_offset, fresh, truncate, context_name):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(context_name, (str, type(None)))
        DivisionCommand.__init__(self, value, duration, start_offset, stop_offset, context_name)
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
