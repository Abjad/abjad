# -*- encoding: utf-8 -*-
import abc
import types


class AbjadObject(object):
    '''.. versionadded:: 2.0

    Abstract base class from which all custom classes should inherit.

    Abajd objects raise exceptions on ``__gt__``, ``__ge__``, 
    ``__lt__``, ``__le__``.

    Abjad objects compare equal only with equal object IDs.
    '''

    ### CLASS VARIABLES ###

    _has_default_attribute_values = False

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when ``id(self)`` equals ``id(expr)``.

        Return boolean.
        '''
        return id(self) == id(expr)

    def __ne__(self, expr):
        r'''Defined equal to the opposite of equality.

        Return boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Interpreter representation of Abjad object.

        Return string.
        '''
        return '{}({})'.format(self._class_name, self._contents_repr_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _class_name(self):
        return type(self).__name__

    @property
    def _contents_repr_string(self):
        result = []
        positional_argument_repr_string = \
            self._positional_argument_repr_string
        if positional_argument_repr_string:
            result.append(positional_argument_repr_string)
        keyword_argument_repr_string = ', '.join(
            self._keyword_argument_name_value_strings)
        if keyword_argument_repr_string:
            result.append(keyword_argument_repr_string)
        return ', '.join(result)

    @property
    def _input_argument_values(self):
        return self._positional_argument_values + \
            self._keyword_argument_values

    @property
    def _keyword_argument_dictionary(self):
        names = self._keyword_argument_names
        values = self._keyword_argument_values
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @property
    def _keyword_argument_name_value_strings(self):
        from abjad.tools import introspectiontools
        result = []
        tmp = introspectiontools.class_to_tools_package_qualified_class_name
        for name in self._keyword_argument_names:
            value = getattr(self, name)
            if value is not None:
                # if the value is a class like Note (which is unusual)
                if type(value) is abc.ABCMeta:
                    value = tmp(value)
                    string = '{}={}'.format(name, value)
                    result.append(string)
                elif not isinstance(value, types.MethodType):
                    string = '{}={!r}'.format(name, value)
                    result.append(string)
        return tuple(result)

    @property
    def _keyword_argument_names(self):
        return self._get_keyword_argument_names()

    @property
    def _keyword_argument_values(self):
        result = []
        for name in self._keyword_argument_names:
            result.append(getattr(self, name))
        return tuple(result)

    @property
    def _one_line_menuing_summary(self):
        return str(self)

    @property
    def _positional_argument_dictionary(self):
        names = self._positional_argument_names
        values = self._positional_argument_values
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @property
    def _positional_argument_names(self):
        if hasattr(self.__init__, '__func__'):
            initializer = type(self).__init__.__func__
            if initializer.func_defaults:
                keyword_argument_count = len(initializer.func_defaults)
            else:
                keyword_argument_count = 0
            initializer_code = initializer.func_code
            positional_argument_count = (
                initializer_code.co_argcount - keyword_argument_count - 1)
            start_index, stop_index = 1, 1 + positional_argument_count
            return initializer_code.co_varnames[start_index:stop_index]
        return ()

    @property
    def _positional_argument_repr_string(self):
        positional_argument_repr_string = [
            repr(x) for x in self._positional_argument_values]
        positional_argument_repr_string = ', '.join(
            positional_argument_repr_string)
        return positional_argument_repr_string

    @property
    def _positional_argument_values(self):
        result = []
        for name in self._positional_argument_names:
            result.append(getattr(self, name))
        return tuple(result)

    @property
    def _repr_pieces(self):
        return [repr(self)]

    @property
    def _storage_format(self):
        return self._tools_package_qualified_indented_repr

    @property
    def _tools_package_name(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self._class_name:
                return part

    @property
    def _tools_package_qualified_class_name(self):
        return '{}.{}'.format(self._tools_package_name, self._class_name)

    @property
    def _tools_package_qualified_indented_repr(self):
        return '\n'.join(
            self._get_tools_package_qualified_repr_pieces(is_indented=True))

    @property
    def _tools_package_qualified_repr(self):
        repr_pieces = self._get_tools_package_qualified_repr_pieces(
            is_indented=False)
        return ''.join(repr_pieces)

    @property
    def _z(self):
        return self._tools_package_qualified_indented_repr

    ### PRIVATE METHODS ###

    def _debug(self, value, annotation=None, blank=False):
        if annotation is None:
            print 'debug: {!r}'.format(value)
        else:
            print 'debug ({}): {!r}'.format(annotation, value)
        if blank:
            print ''

    def _debug_values(self, values, annotation=None, blank=True):
        if values:
            for value in values:
                self._debug(value, annotation=annotation)
            if blank:
                print ''
        else:
            self._debug(repr(values), annotation=annotation)
            if blank:
                print ''

    @classmethod
    def _get_keyword_argument_names(cls):
        if hasattr(cls.__init__, '__func__'):
            initializer = cls.__init__.__func__
            if initializer.func_defaults:
                keyword_argument_count = len(initializer.func_defaults)
                initializer_code = initializer.func_code
                positional_argument_count = (
                    initializer_code.co_argcount - keyword_argument_count - 1)
                start_index = 1 + positional_argument_count
                stop_index = start_index + keyword_argument_count
                return initializer_code.co_varnames[start_index:stop_index]
            else:
                return ()
        return ()

    def _get_tools_package_qualified_keyword_argument_repr_pieces(
        self, is_indented=True):
        from abjad.tools import introspectiontools
        result = []
        if is_indented:
            prefix, suffix = '\t', ','
        else:
            prefix, suffix = '', ', '
        tmp = introspectiontools.class_to_tools_package_qualified_class_name
        for name in self._keyword_argument_names:
            if self._has_default_attribute_values:
                private_keyword_argument_name = '_{}'.format(name)
                value = getattr(self, private_keyword_argument_name)
            else:
                value = getattr(self, name)
            if value is not None:
                if not isinstance(value, types.MethodType):
                    # if value is noninstantiable class
                    if type(value) is abc.ABCMeta:
                        value = tmp(value)
                        result.append('{}{}={}{}'.format(
                            prefix, name, value, suffix))
                    elif hasattr(
                        value, '_get_tools_package_qualified_repr_pieces'):
                        pieces = \
                            value._get_tools_package_qualified_repr_pieces(
                            is_indented=is_indented)
                        if len(pieces) == 1:
                            result.append('{}{}={}{}'.format(
                                prefix, name, pieces[0], suffix))
                        else:
                            assert 3 <= len(pieces)
                            result.append('{}{}={}'.format(
                                prefix, name, pieces[0]))
                            for piece in pieces[1:-1]:
                                result.append('{}{}'.format(prefix, piece))
                            result.append('{}{}{}'.format(
                                prefix, pieces[-1], suffix))
                    elif hasattr(value, '_tools_package_name'):
                        result.append('{}{}={}.{!r}{}'.format(
                            prefix, 
                            name, 
                            value._tools_package_name, 
                            value, 
                            suffix,
                            ))
                    else:
                        result.append('{}{}={!r}{}'.format(
                            prefix, name, value, suffix))
        return tuple(result)

    def _get_tools_package_qualified_positional_argument_repr_pieces(
        self, is_indented=True):
        from abjad.tools import introspectiontools
        result = []
        if is_indented:
            prefix, suffix = '\t', ','
        else:
            prefix, suffix = '', ', '
        tmp = introspectiontools.class_to_tools_package_qualified_class_name
        for value in self._positional_argument_values:
            # if value is a (noninstantiated) class
            if type(value) is abc.ABCMeta:
                value = tmp(value)
                result.append('{}{}{}'.format(prefix, value, suffix))
            elif hasattr(value, '_get_tools_package_qualified_repr_pieces'):
                pieces = value._get_tools_package_qualified_repr_pieces(
                    is_indented=is_indented)
                for piece in pieces[:-1]:
                    result.append('{}{}'.format(prefix, piece))
                result.append('{}{}{}'.format(prefix, pieces[-1], suffix))
            elif hasattr(value, '_tools_package_name'):
                result.append('{}{}.{!r}{}'.format(
                    prefix, value._tools_package_name, value, suffix))
            else:
                result.append('{}{!r}{}'.format(prefix, value, suffix))
        return tuple(result)

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        argument_repr_pieces = []
        argument_repr_pieces.extend(
            self._get_tools_package_qualified_positional_argument_repr_pieces(
                is_indented=is_indented))
        argument_repr_pieces.extend(
            self._get_tools_package_qualified_keyword_argument_repr_pieces(
                is_indented=is_indented))
        if argument_repr_pieces:
            argument_repr_pieces[-1] = argument_repr_pieces[-1].rstrip(' ')
            argument_repr_pieces[-1] = argument_repr_pieces[-1].rstrip(',')
        if len(argument_repr_pieces) == 0:
            result.append('{}()'.format(
                self._tools_package_qualified_class_name))
        else:
            result.append('{}('.format(
                self._tools_package_qualified_class_name))
            result.extend(argument_repr_pieces)
            if is_indented:
                result.append('\t)')
            else:
                result.append(')')
        return tuple(result)

    ### PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        r'''Storage format of Abjad object.

        Return string.
        '''
        return self._tools_package_qualified_indented_repr
