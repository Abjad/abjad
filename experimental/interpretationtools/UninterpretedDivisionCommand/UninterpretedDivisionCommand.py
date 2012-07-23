from experimental.interpretationtools.DivisionCommand import DivisionCommand
import fractions


class UninterpretedDivisionCommand(DivisionCommand):
    r'''.. versionadded:: 1.0

    Division command ``fresh`` and ``truncate`` parameters not yet interpreted.

    Uninterpreted division commands appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, value, duration, fresh, truncate):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        DivisionCommand.__init__(self, value, duration)
        self._fresh = fresh
        self._truncate = truncate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    @property
    def truncate(self):
        return self._truncate
