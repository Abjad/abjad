class _Constraint(object):

    __slots__ = ('_kind', '_predicate')    

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    ### PUBLIC ATTRIBUTES ###

    @property
    def kind(self):
        return self._kind

    @property
    def predicate(self):
        return self._predicate
