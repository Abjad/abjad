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
        manager = systemtools.StorageFormatManager
        tmp = manager.get_tools_package_qualified_class_name
        for name in manager.get_keyword_argument_names(self):
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
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        positional_argument_repr_string = [
            repr(x) for x in manager.get_positional_argument_values(self)]
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

    @property
    def _tools_package_name(self):
        for part in reversed(self.__module__.split('.')):
            if not part == type(self).__name__:
                return part

    @property
    def _tools_package_qualified_class_name(self):
        from abjad.tools import systemtools
        manager = systemtools.StorageFormatManager
        return manager.get_tools_package_qualified_class_name(self)
        #return '{}.{}'.format(self._tools_package_name, type(self).__name__)

    @property
    def _tools_package_qualified_indented_repr(self):
        return ''.join(
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

    def _get_tools_package_qualified_keyword_argument_repr_pieces(
        self, is_indented=True):
        from abjad.tools import systemtools
        result = []
        prefix, suffix = '', ', '
        if is_indented:
            prefix, suffix = '    ', ','
        manager = systemtools.StorageFormatManager
        for name in manager.get_keyword_argument_names(self):
            if self._has_default_attribute_values:
                default_keyword_argument_name = '_default_{}'.format(name)
                default_value = getattr(self, default_keyword_argument_name)
                value = getattr(self, name)
                if value == default_value:
                    value = None
            # change container.music to container._music
            elif hasattr(self, '_storage_format_attribute_mapping'):
                mapped_attribute_name = \
                    self._storage_format_attribute_mapping[name]
                value = getattr(self, mapped_attribute_name)
            else:
                value = getattr(self, name)
            if value is None or isinstance(value, types.MethodType):
                continue
            pieces = manager.format_one_value(value)
            pieces[0] = '{}={}'.format(name, pieces[0])
            for piece in pieces[:-1]:
                result.append(prefix + piece)
            result.append(prefix + pieces[-1] + suffix)
        return tuple(result)

    def _get_tools_package_qualified_positional_argument_repr_pieces(
        self, is_indented=True):
        from abjad.tools import systemtools
        result = []
        prefix, suffix = '', ', '
        if is_indented:
            prefix, suffix = '    ', ','
        manager = systemtools.StorageFormatManager
        for value in manager.get_positional_argument_values(self):
            pieces = manager.format_one_value(value, is_indented=is_indented)
            for piece in pieces[:-1]:
                result.append(prefix + piece)
            result.append(prefix + pieces[-1] + suffix)
        return tuple(result)

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_storage_format_pieces(
            self, is_indented=is_indented)
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
                result.append('    )')
            else:
                result.append(')')
        return tuple(result)
