from collections import Iterable


class _LilyPondSyntaxNode(object):

    __slots__ = ('type', 'value')

    def __init__(self, type, value = [ ]):
        self.type = type
        if isinstance(value, list):
            self.value = tuple(value)
        else:
            self.value = value

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s, <%s>)' % (type(self).__name__, self.type, type(self.value))

    def __str__(self):
        return '\n'.join(self._format_pieces)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        space = '  '
        result = [ ]
        result.append('%s: [' % self.type)
        if isinstance(self.value, Iterable) and \
            any([isinstance(x, type(self)) for x in self.value]):
            for child in self.value:
                if isinstance(child, type(self)):
                    result.extend(['%s%s' % (space, x) for x in child._format_pieces])
                else:
                    result.append('%s%s' % (space, child))
        else:
            result.append('%s%s' % (space, self.value))
        result[-1] += ' ]'
        return result
