from experimental.interpretertools.Token import Token


class DivisionToken(Token):
    r'''.. versionadded:: 1.0

    Abstract division token from which concrete division tokens inherit.
    '''

    ### INITIALIZER ###

    def __init__(self, value, fresh, truncate, duration):
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
    def value(self):
        return self._value
