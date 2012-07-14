from abjad.tools.abctools.AbjadObject import AbjadObject


class ResolvedValue(AbjadObject):
    r'''.. versionadded:: 1.0

    Triple of value, fresh, truncate.

    This is the value actually used to build stuff during interpretation.

    The idea is that a resolved setting is pretty good.

    But a resolved value is even better.
    '''

    ### INITIALIZER ###

    def __init__(self, value, fresh, truncate):
        assert isinstance(fresh, bool)
        assert isinstance(truncate, bool)
        self._value = value
        self._fresh = fresh
        self._truncate = truncate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        return self._fresh

    @property
    def truncate(self):
        return self._truncate

    @property
    def value(self):
        return self._value
