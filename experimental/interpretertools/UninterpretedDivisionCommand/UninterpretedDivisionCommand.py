from experimental.interpretertools.DivisionCommand import DivisionCommand
import fractions


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    # TODO: move context_name to DivisionCommand initializer
    def __init__(self, value, duration, start_offset, stop_offset, fresh, truncate, context_name):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        assert isinstance(context_name, (str, type(None)))
        DivisionCommand.__init__(self, value, duration, start_offset, stop_offset)
        self._fresh = fresh
        self._truncate = truncate
        self._context_name = context_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''Not yet implemented.
        '''
        return self._fresh

    @property
    def context_name(self):
        '''Name of context giving rise to uninterpreted division command.
        '''
        return self._context_name

    @property
    def truncate(self):
        '''Not yet implemented.
        '''
        return self._truncate
