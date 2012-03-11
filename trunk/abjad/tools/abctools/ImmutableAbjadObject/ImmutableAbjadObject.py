from abc import ABCMeta
from abjad.tools.abctools.AbjadObject import AbjadObject


class ImmutableAbjadObject(AbjadObject):
    '''.. versionadded:: 2.0

    Abstract base from which immutable custom classes should inherit.

    Immutable classes raise exceptions on calls to ``__setattr__``, ``__delattr__``.

    .. todo:: document ``__setattr__``, ``__delattr__``.
    '''

    ### CLASS ATTRIBUTES

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __copy__(self, *args):
        '''Return newly instantiated object initialized from self.
        '''
        return type(self)(self)

    # must be defined lexically later than __copy__
    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        '''Immutable objects raise an exception on calls to this method.
        '''
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __getstate__(self):
        '''Return empty dictionary.

        .. todo:: explain.
        '''
        return {}

    def __setattr__(self, *args):
        '''Immutable objects raise an exception on calls to this method.
        '''
        raise AttributeError('{} objects are immutable.'.format(self._class_name))

    def __setstate__(self, state):
        '''Pass.
        
        .. todo:: explain.
        '''
        pass
