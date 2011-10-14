class _LilyPondSyntaxNode(object):

    __slots__ = ('name', 'children')

    def __init__(self, name, children = [ ]):
        self.name = name
        self.children = tuple(children)

    ### OVERRIDES ###

    def __getitem__(self, item):
        return self.children[item]

    def __repr__(self):
        return '%s(%s, <%d>)' % (type(self).__name__, self.name, len(self.children))

    def __str__(self):
        return '\n'.join(self._format_pieces)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_pieces(self):
        space = '  '
        result = [ ]
        result.append('%s: [' % self.name)
        for child in self.children:
            if isinstance(child, type(self)):
                result.extend(['%s%s' % (space, x) for x in child._format_pieces])
            else:
                result.append('%s%s' % (space, child))
        result.append(']')
        return result
