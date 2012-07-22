from experimental.interpretertools.DivisionToken import DivisionToken
import fractions


class UninterpretedDivisionToken(DivisionToken):
    r'''.. versionadded:: 1.0

    Division token ``fresh`` and ``truncate`` parameters not yet interpreted.

    Uninterpreted division tokens appear relatively early in the process of interpretation.
    '''

    ### INITIALIZER ###

    def __init__(self, value, duration, fresh, truncate):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        DivisionToken.__init__(self, value, duration)
        self._fresh = fresh
        self._truncate = truncate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    @property
    def truncate(self):
        return self._truncate
