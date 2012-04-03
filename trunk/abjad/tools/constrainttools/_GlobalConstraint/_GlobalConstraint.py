from abjad.tools.constrainttools._Constraint._Constraint import _Constraint


class _GlobalConstraint(_Constraint):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, predicate):
        object.__setattr__(self, '_kind', 'global')
        assert isinstance(predicate, type(lambda: None))
        assert predicate.func_code.co_argcount == 1
        object.__setattr__(self, '_predicate', predicate)

    ### PRIVATE PROPERTIES ###

    @property
    def _format_string(self):
        return '%r' % self._predicate
