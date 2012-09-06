import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class ImmutableAbjadObject(AbjadObject):
    '''.. versionadded:: 2.8

    Abstract base class from which all custom classes which also subclass
    immutable builtin classes, such as tuple and frozenset, should inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __new__(klass, *args, **kwargs):
        pass

    def __init__(self, *args, **kwargs):
        pass

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _mandatory_argument_names(self):
        initializer = type(self).__new__
        if initializer.func_defaults:
            keyword_argument_count = len(initializer.func_defaults)
        else:
            keyword_argument_count = 0
        initializer_code = initializer.func_code
        mandatory_argument_count = (initializer_code.co_argcount - keyword_argument_count - 1)
        start_index, stop_index = 1, 1 + mandatory_argument_count
        return initializer_code.co_varnames[start_index:stop_index]

    ### PRIVATE METHODS ###

    @classmethod
    def _get_keyword_argument_names(cls):
        if hasattr(cls.__new__, 'func_defaults'):
            initializer = cls.__new__
            if initializer.func_defaults:
                keyword_argument_count = len(initializer.func_defaults)
                initializer_code = initializer.func_code
                mandatory_argument_count = (
                    initializer_code.co_argcount - keyword_argument_count - 1)
                start_index = 1 + mandatory_argument_count
                stop_index = start_index + keyword_argument_count
                return initializer_code.co_varnames[start_index:stop_index]
            else:
                return ()
        return ()
