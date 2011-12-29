class _LilyPondEvent(object):

    def __init__(self, name, **kwargs):
        self.name = name
        for k, v in kwargs.iteritems( ):
            if k != 'name':
                setattr(self, k, v)

    def __repr__(self):        
        return '%s(%s)' % (type(self).__name__, self._format_string)

    @property
    def _format_string(self):
        result = repr(self.name)
        for key in self.__dict__:
            if key == 'name':
                continue
            result += ', %s = %r' % (key, getattr(self, key))
        return result
