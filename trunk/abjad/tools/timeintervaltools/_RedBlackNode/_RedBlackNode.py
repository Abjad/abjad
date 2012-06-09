from abjad.tools.abctools import AbjadObject


class _RedBlackNode(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('key', 'left', 'red', 'right', 'parent', 'payload',)

    ### INITIALIZER ###

    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.parent = None
        self.payload = None
        self.red = True
        self.right = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s(%s, %r)' % (type(self).__name__, self.key, self.payload)

    ### PUBLIC PROPERTIES ###

    @property
    def grandparent(self):
        if self.parent is not None and self.parent.parent is not None:
            return self.parent.parent
        else:
            return None

    @property
    def is_left_child(self):
        if self.parent is not None and self == self.parent.left:
            return True
        else:
            return False

    @property
    def is_right_child(self):
        if self.parent is not None and self == self.parent.right:
            return True
        else:
            return False

    @property
    def sibling(self):
        if self.parent is not None:
            if self.is_left_child:
                return self.parent.right
            else:
                return self.parent.left

    @property
    def uncle(self):
        if self.grandparent is not None:
            if self.parent.is_left_child:
                return self.grandparent.right
            else:
                return self.grandparent.left
        return None
