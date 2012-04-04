from abc import ABCMeta
from abc import abstractmethod
import types


class AbjadObject(object):
    '''.. versionadded:: 2.0

    Abstract base class from which all custom classes should inherit.

    Abajd objects raise exceptions on ``__gt__``, ``__ge__``, ``__lt__``, ``__le__``.

    Abjad objects compare equal only with equal object IDs.

    Authors of custom classes should override these behaviors as required.
    '''

    ### CLASS ATTRIBUTES ###

    _has_default_attribute_values = False
    __metaclass__ = ABCMeta
    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    ### SPECIAL METHODS ###

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

    def __repr__(self):
        '''Interpreter representation of Abjad object defaulting to 
        class name, mandatory arguments, keyword arguments.

        Return string.
        '''
        return '{}({})'.format(self._class_name, self._contents_repr_string)

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _class_name(self):
        return type(self).__name__ 

    @property
    def _contents_repr_string(self):
        result = []
        mandatory_argument_repr_string = self._mandatory_argument_repr_string
        if mandatory_argument_repr_string:
            result.append(mandatory_argument_repr_string)
        keyword_argument_repr_string = ', '.join(self._keyword_argument_name_value_strings)
        if keyword_argument_repr_string:
            result.append(keyword_argument_repr_string)
        return ', '.join(result)

    @property
    def _keyword_argument_name_value_strings(self):
        result = []
        for name in self._keyword_argument_names:
            value = getattr(self, name)
            if value is not None:
                if not isinstance(value, types.MethodType):
                    string = '{}={!r}'.format(name, value)
                    result.append(string)
        return tuple(result)

    @property
    def _keyword_argument_names(self):
        if hasattr(self.__init__, '__func__'):
            initializer = type(self).__init__.__func__
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

    @property
    def _keyword_argument_values(self):
        result = []
        for name in self._keyword_argument_names:
            result.append(getattr(self, name))
        return result

    @property
    def _mandatory_argument_names(self):
        if hasattr(self.__init__, '__func__'):
            initializer = type(self).__init__.__func__
            if initializer.func_defaults:
                keyword_argument_count = len(initializer.func_defaults)
            else:
                keyword_argument_count = 0
            initializer_code = initializer.func_code
            mandatory_argument_count = (initializer_code.co_argcount - keyword_argument_count - 1)
            start_index, stop_index = 1, 1 + mandatory_argument_count
            return initializer_code.co_varnames[start_index:stop_index]
        return ()

    @property
    def _mandatory_argument_repr_string(self):
        mandatory_argument_repr_string = [repr(x) for x in self._mandatory_argument_values]
        mandatory_argument_repr_string = ', '.join(mandatory_argument_repr_string)
        return mandatory_argument_repr_string

    @property
    def _mandatory_argument_values(self):
        result = []
        for name in self._mandatory_argument_names:
            result.append(getattr(self, name))
        return tuple(result)

    @property
    def _one_line_menuing_summary(self):
        return str(self)        

    @property
    def _repr_pieces(self):
        return [repr(self)]

    @property
    def _storage_format(self):
        return self._tools_package_qualified_indented_repr

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self._class_name:
                return part

    @property
    def _tools_package_qualified_class_name(self):
        return '{}.{}'.format(self._tools_package, self._class_name)

    @property
    def _tools_package_qualified_indented_repr(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces(is_indented=True))

    @property
    def _tools_package_qualified_repr(self):
        repr_pieces = self._get_tools_package_qualified_repr_pieces(is_indented=False)
        return ''.join(repr_pieces)

    # temporary alias to be removed after development
    @property
    def _z(self):
        return self._tools_package_qualified_indented_repr

    ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        result = []
        if is_indented:
            prefix, suffix = '\t', ','
        else:
            prefix, suffix = '', ', '
        for name in self._keyword_argument_names:
            if self._has_default_attribute_values:
                private_keyword_argument_name = '_{}'.format(name)
                value = getattr(self, private_keyword_argument_name)
            else:
                value = getattr(self, name)
            if value is not None:
                if not isinstance(value, types.MethodType):
                    if hasattr(value, '_get_tools_package_qualified_repr_pieces'):
                        pieces = value._get_tools_package_qualified_repr_pieces(is_indented=is_indented)
                        if len(pieces) == 1:
                            result.append('{}{}={}{}'.format(prefix, name, pieces[0], suffix))
                        else:
                            assert 3 <= len(pieces)
                            result.append('{}{}={}'.format(prefix, name, pieces[0]))
                            for piece in pieces[1:-1]:
                                result.append('{}{}'.format(prefix, piece)) 
                            result.append('{}{}{}'.format(prefix, pieces[-1], suffix))
                    elif hasattr(value, '_tools_package'):
                        result.append('{}{}={}.{!r}{}'.format(
                            prefix, name, value._tools_package, value, suffix))
                    else:
                        result.append('{}{}={!r}{}'.format(prefix, name, value, suffix))
        return result

    def _get_tools_package_qualified_mandatory_argument_repr_pieces(self, is_indented=True):
        result = []
        if is_indented:
            prefix, suffix = '\t', ','
        else:
            prefix, suffix = '', ', '
        for value in self._mandatory_argument_values:
            if hasattr(value, '_get_tools_package_qualified_repr_pieces'):
                pieces = value._get_tools_package_qualified_repr_pieces(is_indented=is_indented)
                for piece in pieces[:-1]:
                    result.append('{}{}'.format(prefix, piece))
                result.append('{}{}{}'.format(prefix, pieces[-1], suffix))
            elif hasattr(value, '_tools_package'):
                result.append('{}{}.{!r}{}'.format(prefix, value._tools_package, value, suffix))
            else:
                result.append('{}{!r}{}'.format(prefix, value, suffix))
        return result

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        argument_repr_pieces = []
        argument_repr_pieces.extend(
            self._get_tools_package_qualified_mandatory_argument_repr_pieces(is_indented=is_indented))
        argument_repr_pieces.extend(
            self._get_tools_package_qualified_keyword_argument_repr_pieces(is_indented=is_indented))
        if argument_repr_pieces:
            argument_repr_pieces[-1] = argument_repr_pieces[-1].rstrip(' ')
            argument_repr_pieces[-1] = argument_repr_pieces[-1].rstrip(',')
        if len(argument_repr_pieces) == 0:
            result.append('{}()'.format(self._tools_package_qualified_class_name))
        else:
            result.append('{}('.format(self._tools_package_qualified_class_name))
            result.extend(argument_repr_pieces)
            if is_indented:
                result.append('\t)')
            else:
                result.append(')')
        return result
