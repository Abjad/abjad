from abc import ABCMeta
from abjad.tools.abctools.AbjadObject import AbjadObject


class NonsortingIdEqualityComparatorAbjadObject(AbjadObject):
    '''.. versionadded:: 2.0

    Abstract base class to confer nonsorting ID-equality comparability to any custom class.

    Nonsorting objects raise exceptions on gt, ge, lt, le.

    ID-equality comparators compare equal only with equal ojbect IDs.

    This class will be unnecessary when Abjad migrates to Python 3.x
    because Python 3.x implements nonsorting ID comparability by default.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __eq__(self, arg):
        return id(self) == id(arg)

    def __ge__(self, arg):
        raise NotImplementedError('Greater-equal not implemented on "{!r}".'.format(arg))

    def __gt__(self, arg):
        raise NotImplementedError('Greater-than not implemented on "{!r}".'.format(arg))

    def __le__(self, arg):
        raise NotImplementedError('Less-equal not implemented on "{!r}".'.format(arg))

    def __lt__(self, arg):
        raise NotImplementedError('Less-than not implemented on "{!r}".'.format(arg))

    def __ne__(self, arg):
        return not self == arg

    def __nonzero__(self):
        return True
