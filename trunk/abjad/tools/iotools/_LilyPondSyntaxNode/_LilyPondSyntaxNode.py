class _LilyPondSyntaxNode(object):

    def __init__(self, name, children = [ ]):
        self.name = name
        self.children = children

    def __repr__(self):
        return '%s(%s, %s)' % ('Node', self.name, self.children)
