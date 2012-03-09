from abc import ABCMeta
from abjad.mixins._ImmutableAbjadObject import _ImmutableAbjadObject


class _ImmutableDictionary(dict, _ImmutableAbjadObject):
    '''.. versionadded:: 2.0
    
    Abstract base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### OVERLOADS ###

    def __delitem__(self, *args):
        raise AttributeError('objects are immutable: "{}".'.format(self._class_name))

    def __setitem__(self, *args):
        raise AttributeError('objects are immutable: "{}".'.format(self._class_name))
