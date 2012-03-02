class _Constraint(object):

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)
