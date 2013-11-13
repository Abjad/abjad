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
        names = self.client._keyword_argument_names
        values = self.client._keyword_argument_values
        assert len(names) == len(values)
        result = dict(zip(names, values))
        return result

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
    def get_keyword_argument_names(class_):
        if isinstance(class_, types.InstanceType):
            class_ = type(class_)
        if hasattr(class_.__init__, '__func__'):
            initializer = class_.__init__.__func__
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
    def get_positional_argument_names(class_):
        if isinstance(class_, types.InstanceType):
            class_ = type(class_)
        if hasattr(class_.__init__, '__func__'):
            initializer = class_.__init__.__func__
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
    def get_tools_package_qualified_class_name(class_):
        r'''Gets tools-package qualified class name from class:

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_qualified_class_name(Note)
            'scoretools.Note'

        Returns string.
        '''
        if isinstance(class_, types.InstanceType):
            class_ = type(class_)
        module_parts = class_.__module__.split('.')
        unique_parts = [module_parts[0]]
        for part in module_parts[1:]:
            if part != unique_parts[-1]:
                unique_parts.append(part)
        tools_package_qualified_class_name = '.'.join(unique_parts[-2:])
        return tools_package_qualified_class_name
