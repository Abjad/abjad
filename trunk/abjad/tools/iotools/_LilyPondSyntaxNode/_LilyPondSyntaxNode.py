class _LilyPondSyntaxNode(object):

    def __init__(self, name, children = [ ]):
        self.name = name
        self.children = children

    def __repr__(self):
        return '\n'.join(self._format_pieces)

    @property
    def _format_pieces(self):
        space = '  '
        result = [ ]
        result.append('%s: [' % self.name)
        for child in self.children:
            if isinstance(child, type(self)):
                result.extend(['%s%s' % (space, x) for x in child._format_pieces])
            elif isinstance(child, str):
                result.append('%s%s' % (space, child))
        result.append(']')
        return result
