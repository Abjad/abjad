# -*- encoding: utf-8 -*-
import abc
import types


class StorageFormatManager(object):

    ### PUBLIC METHODS ###

    @staticmethod
    def compare(object_one, object_two):
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
    def format_one_value(value, is_indented=True):
        prefix, suffix = '', ', '
        if is_indented:
            prefix, suffix = '\t', ','
        result = []
        if isinstance(value, types.MethodType):
            return result
        if type(value) is abc.ABCMeta:
            value = \
                StorageFormatManager.get_tools_package_qualified_class_name(
                    value)
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
        return result

    @staticmethod
    def get_input_argument_values(object_):
        return StorageFormatManager.get_positional_argument_values(object_) + \
            StorageFormatManager.get_keyword_argument_values(object_)

    @staticmethod
    def get_keyword_argument_dictionary(object_):
        names = StorageFormatManager.get_keyword_argument_names(object_)
        values = StorageFormatManager.get_keyword_argument_values(object_)
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @staticmethod
    def get_keyword_argument_names(object_):
        if StorageFormatManager.is_instance(object_):
            if hasattr(object_, '_keyword_argument_names'):
                return object_._keyword_argument_names
        return StorageFormatManager.get_signature_keyword_argument_names(
            object_)

    @staticmethod
    def get_keyword_argument_values(object_):
        result = []
        for name in StorageFormatManager.get_keyword_argument_names(object_):
            result.append(getattr(object_, name))
        return tuple(result)

    @staticmethod
    def get_positional_argument_dictionary(object_):
        names = StorageFormatManager.get_positional_argument_names(object_)
        values = StorageFormatManager.get_positional_argument_values(object_)
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @staticmethod
    def get_positional_argument_names(object_):
        if StorageFormatManager.is_instance(object_):
            if hasattr(object_, '_positional_argument_names'):
                return object_._positional_argument_names
        return StorageFormatManager.get_signature_positional_argument_names(
            object_)

    @staticmethod
    def get_positional_argument_values(object_):
        if StorageFormatManager.is_instance(object_):
            if hasattr(object_, '_positional_argument_values'):
                return object_._positional_argument_values
        names = StorageFormatManager.get_positional_argument_names(object_)
        result = []
        for name in names:
            result.append(getattr(object_, name))
        return tuple(result)

    @staticmethod
    def get_signature_keyword_argument_names(object_):
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
    def get_tools_package_name(object_):
        r'''Gets tools-package name of `object_`:

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_name(Note)
            'scoretools'

        '''
        if StorageFormatManager.is_instance(object_):
            class_name = type(object_).__name__
            if hasattr(object_, '_tools_package_name'):
                return object_._tools_package_name
        else:
            class_name = object_.__name__
        for part in reversed(object_.__module__.split('.')):
            if not part == class_name:
                return part

    @staticmethod
    def get_tools_package_qualified_class_name(object_):
        r'''Gets tools-package qualified class name of `object_`:

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_qualified_class_name(Note)
            'scoretools.Note'

        Returns string.
        '''
        tools_package_name = None
        if StorageFormatManager.is_instance(object_):
            class_name = type(object_).__name__
            if hasattr(object_, '_tools_package_name'):
                tools_package_name = object_._tools_package_name
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
        if isinstance(object_, types.TypeType):
            return False
        elif type(object_) is object_.__class__:
            return True
        return False

    @staticmethod
    def get_storage_format_pieces(
        object_,
        is_indented=True,
        keyword_argument_names=None,
        positional_argument_values=None,
        tools_package_name=None,
        ):
        result = []
        argument_pieces = []
        argument_pieces.extend(
            StorageFormatManager.get_storage_format_positional_pieces(
                object_,
                is_indented=is_indented,
                positional_argument_values=positional_argument_values,
                ))
        argument_pieces.extend(
            StorageFormatManager.get_storage_format_keyword_pieces(
                object_,
                is_indented=is_indented,
                keyword_argument_names=keyword_argument_names,
                ))
        if argument_pieces:
            argument_pieces[-1] = argument_pieces[-1].rstrip(' ')
            argument_pieces[-1] = argument_pieces[-1].rstrip(',')
        class_name = type(object_).__name__
        tools_package_name = tools_package_name or \
            StorageFormatManager.get_tools_package_name(object_)
        tools_package_qualified_class_name = '{}.{}'.format(
            tools_package_name, class_name)
        if len(argument_pieces) == 0:
            result.append('{}()'.format(tools_package_qualified_class_name))
        else:
            result.append('{}('.format(tools_package_qualified_class_name))
            result.extend(argument_pieces)
            if is_indented:
                result.append('\t)')
            else:
                result.append(')')
        return tuple(result)

    @staticmethod
    def get_storage_format_keyword_argument_pieces(
        object_,
        is_indented=True,
        keyword_argument_names=None,
        ):
        prefix, suffix = '', ', '
        if is_indented:
            prefix, suffix = '\t', ','

    @staticmethod
    def get_storage_format_positional_argument_pieces(
        object_,
        is_indented=True,
        positional_argument_values=None,
        ):
        prefix, suffix = '', ', '
        if is_indented:
            prefix, suffix = '\t', ','
