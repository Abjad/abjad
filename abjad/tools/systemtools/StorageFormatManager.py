# -*- encoding: utf-8 -*-
import abc
import types


class StorageFormatManager(object):
    r'''Manages Abjad object storage formats.
    '''

    ### PUBLIC METHODS ###

    @staticmethod
    def compare(object_one, object_two):
        r'''Compares `object_one` to `object_two`.

        Returns boolean.
        '''
        if type(object_one) is not type(object_two):
            return False
        if StorageFormatManager.get_positional_argument_values(object_one) != \
            StorageFormatManager.get_positional_argument_values(object_two):
            return False
        if StorageFormatManager.get_keyword_argument_values(object_one) != \
            StorageFormatManager.get_keyword_argument_values(object_two):
            return False
        return True

    @staticmethod
    def format_one_value(
        value,
        as_storage_format=True,
        is_indented=True,
        ):
        r'''Formats one value.

        Returns list.
        '''
        result = []
        prefix, infix, suffix = StorageFormatManager.get_indentation_strings(
            is_indented)
        if isinstance(value, types.MethodType):
            return result
        if type(value) is abc.ABCMeta:
            if as_storage_format:
                value = '{}.{}'.format(
                    StorageFormatManager.get_tools_package_name(value),
                    value.__name__,
                    )
            else:
                value = value.__name__
            result.append(value)
        elif as_storage_format and hasattr(
            value, '_storage_format_specification'):
            specification = value._storage_format_specification
            pieces = StorageFormatManager.get_format_pieces(
                specification,
                as_storage_format=True,
                )
            result.extend(pieces)
        elif not as_storage_format and hasattr(
            value, '_repr_specification'):
            specification = value._repr_specification
            pieces = StorageFormatManager.get_format_pieces(
                specification,
                as_storage_format=False,
                )
            result.extend(pieces)
        elif isinstance(value, (list, tuple)):
            # just return the repr, if all contents are builtin types
            if all(isinstance(x, (bool, int, float, str, type(None)))
                for x in value):
                piece = repr(value)
                if len(piece) < 50:
                    return [repr(value)]
            if isinstance(value, list):
                braces = '[', ']'
            else:
                braces = '(', ')'
            result.append('{}{}'.format(braces[0], infix))
            for x in value:
                pieces = StorageFormatManager.format_one_value(
                    x,
                    as_storage_format=as_storage_format,
                    is_indented=is_indented,
                    )
                for piece in pieces[:-1]:
                    result.append('{}{}'.format(prefix, piece))
                result.append('{}{}{}'.format(prefix, pieces[-1], suffix))
            if not is_indented:
                if isinstance(value, list) or 1 < len(value):
                    result[-1] = result[-1].rstrip(suffix)
                else:
                    result[-1] = result[-1].rstrip()
            result.append('{}{}'.format(prefix, braces[1]))
        elif isinstance(value, dict):
            result.append('{{{}'.format(infix))
            for key, value in sorted(value.items()):
                key_pieces = StorageFormatManager.format_one_value(
                    key,
                    as_storage_format=as_storage_format,
                    is_indented=is_indented,
                    )
                value_pieces = StorageFormatManager.format_one_value(
                    value,
                    as_storage_format=as_storage_format,
                    is_indented=is_indented,
                    )
                for x in key_pieces[:-1]:
                    result.append('{}{}'.format(prefix, x))
                result.append('{}{}: {}'.format(
                    prefix, key_pieces[-1], value_pieces[0]))
                for x in value_pieces[1:]:
                    result.append('{}{}'.format(prefix, x))
                result[-1] = '{}{}'.format(result[-1], suffix)
            if not is_indented:
                result[-1] = result[-1].rstrip(suffix) + infix
            result.append('{}}}'.format(prefix))
        else:
            result.append(repr(value))
        return result

    @staticmethod
    def get_format_pieces(
        specification,
        as_storage_format=True,
        ):
        r'''Gets format pieces.
        '''
        if specification.storage_format_pieces is not None:
            return specification.storage_format_pieces

        result = []
        prefix, infix, suffix = StorageFormatManager.get_indentation_strings(
            specification.is_indented)

        class_name = type(specification.instance).__name__
        if as_storage_format:
            tools_package_name = specification.tools_package_name
            class_name_prefix = '{}.{}'.format(
                tools_package_name, class_name)
        else:
            class_name_prefix = class_name

        positional_argument_pieces = []
        for value in specification.positional_argument_values:
            pieces = StorageFormatManager.format_one_value(
                value,
                as_storage_format=as_storage_format,
                is_indented=specification.is_indented,
                )
            for piece in pieces[:-1]:
                positional_argument_pieces.append(prefix + piece)
            positional_argument_pieces.append(prefix + pieces[-1] + suffix)

        keyword_argument_pieces = []
        for name in specification.keyword_argument_names:
            value = getattr(specification.instance, name)
            if value is None or isinstance(value, types.MethodType):
                continue
            pieces = StorageFormatManager.format_one_value(
                value,
                as_storage_format=as_storage_format,
                is_indented=specification.is_indented,
                )
            pieces[0] = '{}={}'.format(name, pieces[0])
            for piece in pieces[:-1]:
                keyword_argument_pieces.append(prefix + piece)
            keyword_argument_pieces.append(prefix + pieces[-1] + suffix)

        if not as_storage_format and specification.is_bracketted:
            result.append('<')

        if not as_storage_format and specification.body_text:
            result.append('{}({})'.format(
                class_name_prefix,
                specification.body_text,
                ))
        else:
            if not positional_argument_pieces and not keyword_argument_pieces:
                result.append('{}()'.format(class_name_prefix))
            else:
                result.append('{}({}'.format(
                    class_name_prefix,
                    infix,
                    ))
                result.extend(positional_argument_pieces)
                if positional_argument_pieces and not keyword_argument_pieces:
                    result[-1] = result[-1].rstrip(suffix) + infix
                else:
                    result.extend(keyword_argument_pieces)
                if not as_storage_format:
                    result[-1] = result[-1].rstrip(suffix) + infix
                if specification.is_indented:
                    result.append('{})'.format(prefix))
                else:
                    result.append(')')

        if not as_storage_format and specification.is_bracketted:
            result.append('>')

        if not specification.is_indented:
            return (''.join(result),)
        return tuple(result)

    @staticmethod
    def get_hash_values(object_):
        r'''Gets hash values for `object_`.

        The hash values are a tuple of the type of `object_`, the values of its
        positional arguments, and the values of its keyword arguments, both
        sorted by argument name.

        Return tuple.
        '''
        def make_hashable(value):
            if isinstance(value, dict):
                value = tuple(value.items())
            elif isinstance(value, list):
                value = tuple(value)
            elif isinstance(value, (set, frozenset)):
                value = tuple(value)
            return value
        values = []
        values.append(type(object_))
        positional_argument_dictionary = \
            StorageFormatManager.get_positional_argument_dictionary(object_)
        keyword_argument_dictionary = \
            StorageFormatManager.get_keyword_argument_dictionary(object_)
        for key, value in sorted(positional_argument_dictionary.items()):
            values.append(make_hashable(value))
        for key, value in sorted(keyword_argument_dictionary.items()):
            values.append(make_hashable(value))
        return tuple(values)

    @staticmethod
    def get_indentation_strings(is_indented):
        r'''Gets indentation strings.
        '''
        prefix, infix, suffix = '', '', ', '
        if is_indented:
            prefix, infix, suffix = '    ', '\n', ',\n'
        return prefix, infix, suffix

    @staticmethod
    def get_input_argument_values(object_):
        r'''Gets input argument values.
        '''
        return StorageFormatManager.get_positional_argument_values(object_) + \
            StorageFormatManager.get_keyword_argument_values(object_)

    @staticmethod
    def get_keyword_argument_dictionary(object_):
        r'''Gets keyword argument dictionary.
        '''
        names = StorageFormatManager.get_keyword_argument_names(object_)
        values = StorageFormatManager.get_keyword_argument_values(object_)
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @staticmethod
    def get_keyword_argument_names(object_):
        r'''Gets keyword argument names.
        '''
        return StorageFormatManager.get_signature_keyword_argument_names(
            object_)

    @staticmethod
    def get_keyword_argument_values(object_):
        r'''Gets keyword argument values.
        '''
        result = []
        for name in StorageFormatManager.get_keyword_argument_names(object_):
            result.append(getattr(object_, name))
        return tuple(result)

    @staticmethod
    def get_positional_argument_dictionary(object_):
        r'''Gets positional argument dictionary.
        '''
        names = StorageFormatManager.get_positional_argument_names(object_)
        values = StorageFormatManager.get_positional_argument_values(object_)
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @staticmethod
    def get_positional_argument_names(object_):
        r'''Gets positional argument names.
        '''
        return StorageFormatManager.get_signature_positional_argument_names(
            object_)

    @staticmethod
    def get_positional_argument_values(object_):
        r'''Gets positional argument values.
        '''
        names = StorageFormatManager.get_positional_argument_names(object_)
        result = []
        for name in names:
            result.append(getattr(object_, name))
        return tuple(result)

    @staticmethod
    def get_repr_format(
        object_,
        ):
        r'''Gets interpreter representation format.
        '''
        assert '_repr_specification' in dir(object_)
        specification = object_._repr_specification
        pieces = StorageFormatManager.get_format_pieces(
            specification,
            as_storage_format=False,
            )
        return ''.join(pieces)

    @staticmethod
    def get_signature_keyword_argument_names(object_):
        r'''Gets signature keyword argument names.
        '''
        if hasattr(object_.__init__, '__func__'):
            initializer = object_.__init__.__func__
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

    @staticmethod
    def get_signature_positional_argument_names(object_):
        r'''Gets signature positional argument names.
        '''
        if hasattr(object_.__init__, '__func__'):
            initializer = object_.__init__.__func__
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

    @staticmethod
    def get_storage_format(
        object_,
        ):
        r'''Gets storage format.
        '''
        assert '_storage_format_specification' in dir(object_)
        specification = object_._storage_format_specification
        pieces = StorageFormatManager.get_format_pieces(
            specification,
            as_storage_format=True,
            )
        result = ''.join(pieces)
        return result

    @staticmethod
    def get_tools_package_name(object_):
        r'''Gets tools-package name of `object_`.

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_name(Note)
            'scoretools'

        '''
        if StorageFormatManager.is_instance(object_):
            class_name = type(object_).__name__
        else:
            class_name = object_.__name__
        for part in reversed(object_.__module__.split('.')):
            if not part == class_name:
                return part

    @staticmethod
    def get_tools_package_qualified_class_name(object_):
        r'''Gets tools-package qualified class name of `object_`.

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_qualified_class_name(Note)
            'scoretools.Note'

        Returns string.
        '''
        tools_package_name = None
        if StorageFormatManager.is_instance(object_):
            class_name = type(object_).__name__
        else:
            class_name = object_.__name__
        if not tools_package_name:
            for part in reversed(object_.__module__.split('.')):
                if not part == class_name:
                    tools_package_name = part
                    break
        return '{}.{}'.format(tools_package_name, class_name)

    @staticmethod
    def is_instance(object_):
        r'''Is true when `object_` is instance. Otherwise false.

        Returns boolean.
        '''
        if isinstance(object_, types.TypeType):
            return False
        elif type(object_) is object_.__class__:
            return True
        return False
