import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class AttributeEqualityAbjadObject(AbjadObject):
    '''.. versionadded:: 2.0

    Abstract base class to confer nonsorting attribute-equality to any custom class.

    Nonsorting objects raise exceptions on ``__gt__``, ``__ge__``, ``__lt__``, ``__le__``.

    Attribute-equality objects compare equal only with equal comparison attributes.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ('_comparison_attribute', '_format_string')

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        arg = self._massage_comparison_arg(arg)
        return arg and self._comparison_attribute == arg._comparison_attribute

    def __ne__(self, arg):
        '''Initialize new object from `arg` and evaluate comparison attributes.

        Return boolean.
        '''
        return not self == arg

    def __repr__(self):
        '''Interpreter representation of object defined equal to class name and format string.

        Return string.
        '''
        return '%s(%s)' % (self.__class__.__name__, self._format_string)

    ### PRIVATE METHODS ###

    def _massage_comparison_arg(self, arg):
        if not isinstance(arg, type(self)):
            try:
                arg = type(self)(arg)
            except (ValueError, TypeError):
                return False
        return arg
