from abc import ABCMeta


class StrictComparator(object):
    '''.. versionadded:: 2.8

    Abstract base class to confer strict comparison behavior to any custom class.

    Abjad classes inheriting from this class should also inherit from
    either ``AbjadObject`` or ``ImmutableAbjadObject``.

    This class will be unnecessary when Abjad migrates to Python 3.x
    because Python 3.x implements strict comparison behavior by default.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __eq__(self, arg):
        return id(self) == id(arg)

    def __ge__(self, arg):
        raise NotImplementedError('\n\tGreater-equal not implemented on "{!r}".'.format(arg))

    def __gt__(self, arg):
        raise NotImplementedError('\n\tGreater-than not implemented on "{!r}".'.format(arg))

    def __le__(self, arg):
        raise NotImplementedError('\n\tLess-equal not implemented on "{!r}".'.format(arg))

    def __lt__(self, arg):
        raise NotImplementedError('\n\tLess-than not implemented on "{!r}".'.format(arg))

    def __ne__(self, arg):
        return not self == arg

    def __nonzero__(self):
        return True
