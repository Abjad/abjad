from abc import ABCMeta
from abc import abstractproperty


class _MutableAbjadObject(object):
    '''.. versionadded:: 2.8

    Abstract base class for system-global functionality.

    _MutableAbjadObject and _ImmutableAbjadObject differ only in the implementation of __slots__.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self.class_name)

    @property
    def _keyword_argument_name_value_strings(self):
        result = []
        for name in self._keyword_argument_names:
            value = getattr(self, name)
            string = '{}={!r}'.format(name, value)
            result.append(string)
        return tuple(result)

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _mandatory_argument_values(self):
        return ()

    @property
    def _one_line_menuing_summary(self):
        return str(self)        

    @property
    def _repr_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, repr(self))

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self.class_name:
                return part
    
    ### PUBLIC READ-ONLY ATTRIBUTES ###

    @property
    def class_name(self):
        return type(self).__name__ 
