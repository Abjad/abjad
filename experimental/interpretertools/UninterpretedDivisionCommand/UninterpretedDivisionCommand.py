from experimental.interpretertools.DivisionCommand import DivisionCommand
import fractions


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, value, duration, fresh, truncate, source_context_name):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(source_context_name, str)
        DivisionCommand.__init__(self, value, duration)
        self._fresh = fresh
        self._truncate = truncate
        self._source_context_name = source_context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''Not yet implemented.
        '''
        return self._fresh

    @property
    def source_context_name(self):
        '''Name of source context giving rise to uninterpreted division command.
        '''
        return self._source_context_name

    @property
    def truncate(self):
        '''Not yet implemented.
        '''
        return self._truncate
