from abc import ABCMeta
from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class Immutable(ImmutableAbjadObject):
    '''.. versionadded:: 2.0

    Abstract base from which immutable custom classes can inherit.
    '''

    ### CLASS ATTRIBUTES

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self)

    # must be defined lexically later than __copy__
    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __getstate__(self):
        return {}

    def __setattr__(self, *args):
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __setstate__(self, state):
        pass
