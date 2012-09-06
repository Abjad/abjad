import abc

from abjad.tools.abctools.SortableAttributeEqualityAbjadObject import SortableAttributeEqualityAbjadObject


class PitchObject(SortableAttributeEqualityAbjadObject):
    '''.. versionadded:: 2.0

    Pitch base class.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_format_string', )

    ### INITIALIZER ###
    
    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        raise NotImplementedError('TODO: all pitch-related classes must implement abs.')

    def __float__(self):
        raise NotImplementedError('TODO: all pitch-related classes must implement float.')

    def __hash__(self):
        return hash(repr(self))

    def __int__(self):
        raise NotImplementedError('TODO: all pitch-related classes must implement int.')

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)
