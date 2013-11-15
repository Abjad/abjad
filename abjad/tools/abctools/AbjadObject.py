# -*- encoding: utf-8 -*-
import abc
import types


class AbjadObject(object):
    '''Abstract base class from which all custom classes should inherit.

    Abjad objects compare equal only with equal object IDs.
    '''

    ### CLASS VARIABLES ###

    _has_default_attribute_values = False

    __metaclass__ = abc.ABCMeta

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''True when ID of `expr` equals ID of Abjad object.

        Returns boolean.
        '''
        return id(self) == id(expr)

    def __ne__(self, expr):
        r'''True when ID of `expr` does not equal ID of Abjad object.

        Returns boolean.
        '''
        return not self == expr

    def __repr__(self):
        r'''Interpreter representation of Abjad object.

        Returns string.
        '''
        result = '{}({})'
        result = result.format(
            type(self).__name__,
            self._contents_repr_string,
            )
        return result

    ### PRIVATE PROPERTIES ###

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
    def _keyword_argument_name_value_strings(self):
        from abjad.tools import systemtools
        result = []
        specification = self._storage_format_specification
        manager = systemtools.StorageFormatManager
        tmp = manager.get_tools_package_qualified_class_name
        for name in specification.keyword_argument_names:
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
    def _one_line_menuing_summary(self):
        return str(self)

    @property
    def _positional_argument_repr_string(self):
        specification = self._storage_format_specification
        positional_argument_repr_string = [
            repr(x) for x in specification.positional_argument_values
            ]
        positional_argument_repr_string = ', '.join(
            positional_argument_repr_string)
        return positional_argument_repr_string

    @property
    def _repr_pieces(self):
        return [repr(self)]

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(self)

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
