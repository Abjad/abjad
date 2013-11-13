# -*- encoding: utf-8 -*-
import types


class StorageFormatManager(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def keyword_argument_dictionary(self):
        names = self.keyword_argument_names
        values = self.keyword_argument_values
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @property
    def keyword_argument_names(self):
        return self.get_keyword_argument_names(self.client)

    @property
    def keyword_argument_values(self):
        return self.get_keyword_argument_values(self.client)

    @property
    def positional_argument_dictionary(self):
        names = self.positional_argument_names
        values = self.positional_argument_values
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

    @property
    def positional_argument_names(self):
        return self.get_positional_argument_names(self.client)

    @property
    def positional_argument_values(self):
        return self.get_positional_argument_values(self.client)

    @property
    def tools_package_name(self):
        for part in reversed(self.client__module__.split('.')):
            if not part == type(self.client).__name__:
                return part

    @property
    def tools_package_qualified_class_name(self):
        return '{}.{}'.format(
            self.clienttools_package_name,
            type(self.client).__name__,
            )

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
    def get_tools_package_qualified_class_name(object_):
        r'''Gets tools-package qualified class name from class:

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_qualified_object_name(Note)
            'scoretools.Note'

        Returns string.
        '''
        if StorageFormatManager.is_instance(object_):
            object_ = type(object_)
        module_parts = object_.__module__.split('.')
        unique_parts = [module_parts[0]]
        for part in module_parts[1:]:
            if part != unique_parts[-1]:
                unique_parts.append(part)
        tools_package_qualified_object_name = '.'.join(unique_parts[-2:])
        return tools_package_qualified_object_name

    @staticmethod
    def is_instance(object_):
        if type(object_) is object_.__class__:
            return True
        return False

