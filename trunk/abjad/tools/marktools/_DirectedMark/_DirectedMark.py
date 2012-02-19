from abjad.tools.marktools.Mark import Mark


class _DirectedMark(Mark):

    __slots__ = ('_direction', '_format_slot')

    def __init__(self, *args, **kwargs):
        Mark.__init__(self, *args)
        if 'direction' in kwargs:
            self.direction = kwargs['direction']
        else:
            self.direction = None
    
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
