from abc import ABCMeta


class AbjadObject(object):
    '''.. versionadded:: 2.8

    Abstract base class from which all custom classes should inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta
    __slots__ = ()

    ### OVERLOADS ###

    def __repr__(self):
        '''Interpreter representation of Abjad object.

        Default to class name, mandatory arguments, keyword arguments.

        Return string.
        '''
        return '{}()'.format(self._class_name)

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _class_name(self):
        return type(self).__name__ 

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
    def _keyword_argument_values(self):
        result = []
        for name in self._keyword_argument_names:
            result.append(getattr(self, name))
        return result

    @property
    def _mandatory_argument_values(self):
        return ()

    @property
    def _one_line_menuing_summary(self):
        return str(self)        

    @property
    def _repr_pieces(self):
        return [repr(self)]

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self._class_name:
                return part

    @property
    def _tools_package_qualified_class_name(self):
        return '{}.{}'.format(self._tools_package, self._class_name)

    @property
    def _tools_package_qualified_repr(self):
        return '{}.{}'.format(self._tools_package, repr(self))

    @property
    def _tools_package_qualified_repr_pieces(self):
        return [self._tools_package_qualified_repr]
