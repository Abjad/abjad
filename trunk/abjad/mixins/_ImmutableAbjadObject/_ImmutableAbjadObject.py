from abc import ABCMeta
from abc import abstractproperty


class _ImmutableAbjadObject(object):
    '''.. versionadded:: 2.8
    
    Abstract base class for system-global functionality.

    _MutableAbjadObject and _ImmutableAbjadObject differ only in the implementation of __slots__.
    '''
    
    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self.class_name)

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _mandatory_argument_names(self):
        return ()

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


