from experimental.interpretertools.Token import Token
import fractions


class DivisionToken(Token):
    r'''.. versionadded:: 1.0

    Durated period of time over which a division-maker will apply.
    '''

    ### INITIALIZER ###

    def __init__(self, value, duration, fresh, truncate):
        assert isinstance(fresh, bool), repr(fresh)
        assert isinstance(truncate, bool), repr(truncate)
        self._value = value
        self._fresh = fresh
        self._truncate = truncate
        self._duration = duration

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def fresh(self):
        return self._fresh

    @property
    def truncate(self):
        return self._truncate

    @property
    def vector(self):
        return (self.value, self.duration, self.fresh, self.truncate)

    @property
    def value(self):
        return self._value
