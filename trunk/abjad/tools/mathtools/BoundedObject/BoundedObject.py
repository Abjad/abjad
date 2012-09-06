import abc
from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class BoundedObject(ImmutableAbjadObject):
    r'''.. versionadded:: 2.10

    Bounded object mix-in.

    Bounded objects are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_closed(self):
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        return not self.is_left_open == self.is_right_open

    @property
    def is_open(self):
        return not self.is_left_closed and not self.is_right_closed

    ### READ / WRITE PUBLIC PROPERTIES ### 

    @apply
    def is_left_closed():
        def fget(self):
            return self._is_left_closed
        def fset(self, is_left_closed):
            assert isinstance(is_left_closed, bool), is_left_closed
            self._is_left_closed = is_left_closed
        return property(**locals())

    @apply
    def is_left_open():
        def fget(self):
            return not self.is_left_closed
        def fset(self, is_left_open):
            assert isinstance(is_left_open, bool), is_left_open
            self._is_left_closed = not is_left_open
        return property(**locals())

    @apply
    def is_right_closed():
        def fget(self):
            return self._is_right_closed
        def fset(self, is_right_closed):
            assert isinstance(is_right_closed, bool), is_right_closed
            self._is_right_closed = is_right_closed
        return property(**locals())

    @apply
    def is_right_open():
        def fget(self):
            return not self.is_right_closed
        def fset(self, is_right_open):
            assert isinstance(is_right_open, bool), is_right_open
            self._is_right_closed = not is_right_open
        return property(**locals())
