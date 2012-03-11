from abc import ABCMeta
from abjad.tools.abctools.AbjadObject import AbjadObject


class NonsortingIdEqualityAbjadObject(AbjadObject):
    '''.. versionadded:: 2.0

    Abstract base class to confer nonsorting ID-equality to any custom class.

    Nonsorting objects raise exceptions on ``__gt__``, ``__ge__``, ``__lt__``, ``__le__``.

    ID-equality objects compare equal only with equal object IDs.

    This class will be unnecessary when Abjad migrates to Python 3.x
    because Python 3.x implements nonsorting ID comparability by default.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __eq__(self, arg):
        '''True when ``id(self)`` equals ``id(arg)``.

        Return boolean.
        '''
        return id(self) == id(arg)

    def __ge__(self, arg):
        '''Nonsorting objects do not implement this method.
        
        Raise exception.
        '''
        raise NotImplementedError('Greater-equal not implemented on "{!r}".'.format(arg))

    def __gt__(self, arg):
        '''Nonsorting objects do not implement this method.
    
        Raise exception
        '''
        raise NotImplementedError('Greater-than not implemented on "{!r}".'.format(arg))

    def __le__(self, arg):
        '''Nonsorting objects do not implement this method.
    
        Raise exception.
        '''
        raise NotImplementedError('Less-equal not implemented on "{!r}".'.format(arg))

    def __lt__(self, arg):
        '''Nonsorting objects do not implement this method.

        Raise exception.
        '''
        raise NotImplementedError('Less-than not implemented on "{!r}".'.format(arg))

    def __ne__(self, arg):
        '''True when ``id(self)`` does not equal ``id(arg)``.

        Return boolean.
        '''
        return not self == arg

    def __nonzero__(self):
        '''Defined equal to true.

        Return boolean.
        '''
        return True
