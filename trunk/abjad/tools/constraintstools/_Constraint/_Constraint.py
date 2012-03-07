from abjad.mixins import _Immutable


class _Constraint(_Immutable):

    __slots__ = ('_kind', '_predicate')    

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _sort_tuple(self):
        if self.kind == 'relative':
            return (0, self.index_span)
        elif self.kind == 'absolute':
            return (1, self.max_index)
        elif self.kind == 'global':
            return (2, 0)
        else:
            raise Exception('Cannot generate sort tuple for %r.' % self)

    ### PUBLIC ATTRIBUTES ###

    @property
    def kind(self):
        return self._kind

    @property
    def predicate(self):
        return self._predicate
