from abjad.tools.spannertools.Spanner import Spanner


class _DirectedSpanner(Spanner):
    
    def __init__(self, components=[], direction=None):
        Spanner.__init__(self, components)
        self.direction = direction

    ### PUBLIC ATTRIBUTES ###

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, direction):
            assert isinstance(direction, (str, type(None)))
            if direction in ('^', 'up'):
                direction = '^'
            elif direction in ('_', 'down'):
                direction = '_'
            elif direction in ('-', 'default', 'neutral'):
                direction = '-'
            elif direction is None:
                direction = None
            else:
                raise ValueError('can not set direction for %s.' % type(self).__name__)
            self._direction = direction
        return property(**locals())
