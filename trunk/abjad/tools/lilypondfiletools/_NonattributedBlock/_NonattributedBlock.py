class _NonattributedBlock(list):
    r'''Abjad model of the LilyPond input file blocks with no attributes.
    '''

    ### OVERLOADS ###

    def __repr__(self):
        if not len(self):
            return '%s()' % type(self).__name__
        else:
            return '%s(%s)' % (type(self).__name__, len(self))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        result = []
        if not len(self):
            if self._is_formatted_when_empty:
                result.append(r'%s {}' % self._escaped_name)
        else:
            result.append(r'%s {' % self._escaped_name)
            for x in self:
                if hasattr(x, '_format_pieces'):
                    result.extend(['\t' + piece for piece in x._format_pieces])
                elif isinstance(x, str):
                    result.append('\t%s' % x)
            result.append('}')
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        return '\n'.join(self._format_pieces)

    @apply
    def is_formatted_when_empty():
        def fget(self):
            return self._is_formatted_when_empty
        def fset(self, arg):
            if isinstance(arg, bool):
                self._is_formatted_when_empty = arg
            else:
                raise TypeError
        return property(**locals())
