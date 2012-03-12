from abc import ABCMeta


class AbjadObject(object):
    '''.. versionadded:: 2.0

    Abstract base class from which all custom classes should inherit.

    Abajd objects raise exceptions on ``__gt__``, ``__ge__``, ``__lt__``, ``__le__``.

    Abjad objects compare equal only with equal object IDs.

    Authors of custom classes should override these behaviors as required.
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
        '''Abjad objects by default do not implement this method.
        
        Raise exception.
        '''
        raise NotImplementedError('Greater-equal not implemented on "{!r}".'.format(arg))

    def __gt__(self, arg):
        '''Abjad objects by default do not implement this method.
    
        Raise exception
        '''
        raise NotImplementedError('Greater-than not implemented on "{!r}".'.format(arg))

    def __le__(self, arg):
        '''Abjad objects by default do not implement this method.
    
        Raise exception.
        '''
        raise NotImplementedError('Less-equal not implemented on "{!r}".'.format(arg))

    def __lt__(self, arg):
        '''Abjad objects by default do not implement this method.

        Raise exception.
        '''
        raise NotImplementedError('Less-than not implemented on "{!r}".'.format(arg))

    def __ne__(self, arg):
        '''True when ``id(self)`` does not equal ``id(arg)``.

        Return boolean.
        '''
        return not self == arg

    # TODO: should this be elimiated?
    def __nonzero__(self):
        '''Defined equal to true.

        Return boolean.
        '''
        return True

    def __repr__(self):
        '''Interpreter representation of Abjad object defaulting to 
        class name, mandatory arguments, keyword arguments.

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
