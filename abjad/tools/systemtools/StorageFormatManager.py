# -*- coding: utf-8 -*-
import collections
import inspect
import sys
import types
from abjad.tools.abctools import AbjadObject


class StorageFormatManager(AbjadObject):
    r'''Manages Abjad object storage formats.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Storage formatting'

    unindented_whitespace = '', '', ', '
    indented_whitespace = '    ', '\n', ',\n'

    ### PUBLIC METHODS ###

    @staticmethod
    def accepts_kwargs(subject):
        r'''Is true when `subject` accepts \*\*kwargs. Otherwise false.

        Returns true or false.
        '''
        args, varargs, varkw, defaults = inspect.getargspec(subject.__init__)
        if varkw is not None:
            return True
        return False

    @staticmethod
    def compare(object_one, object_two):
        r'''Compares `object_one` to `object_two`.

        Returns true or false.
        '''
        if not isinstance(object_two, type(object_one)):
            return False
        if (
            StorageFormatManager.get_positional_argument_values(object_one) !=
            StorageFormatManager.get_positional_argument_values(object_two)
            ):
            return False
        if (
            StorageFormatManager.get_keyword_argument_values(object_one) !=
            StorageFormatManager.get_keyword_argument_values(object_two)
            ):
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
        from abjad.tools import datastructuretools
        result = []

        if is_indented:
            prefix, infix, suffix = StorageFormatManager.indented_whitespace
        else:
            prefix, infix, suffix = StorageFormatManager.unindented_whitespace

        if isinstance(value, types.MethodType):
            return result

        if isinstance(value, type):
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
            prototype = (bool, int, float, str, type(None))
            if all(isinstance(x, prototype) for x in value):
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

        elif isinstance(value, (
            collections.OrderedDict,
            datastructuretools.TypedOrderedDict,
            )):
            result.append('[{}'.format(infix))
            for item in list(value.items()):
                try:
                    item_pieces = StorageFormatManager.format_one_value(
                        item,
                        as_storage_format=as_storage_format,
                        is_indented=is_indented,
                        )
                except:
                    print(item)
                    raise
                for x in item_pieces:
                    result.append('{}{}'.format(prefix, x))
                result[-1] = '{}{}'.format(result[-1], suffix)
            if not is_indented:
                result[-1] = result[-1].rstrip(suffix) + infix
            result.append('{}]'.format(prefix))

        elif isinstance(value, dict):
            result.append('{{{}'.format(infix))
            items = list(value.items())
            if not isinstance(value, collections.OrderedDict):
                items = sorted(items)
            for key, value in items:
                try:
                    key_pieces = StorageFormatManager.format_one_value(
                        key,
                        as_storage_format=as_storage_format,
                        is_indented=is_indented,
                        )
                except:
                    print(key)
                    raise
                try:
                    value_pieces = StorageFormatManager.format_one_value(
                        value,
                        as_storage_format=as_storage_format,
                        is_indented=is_indented,
                        )
                except:
                    print(value)
                    raise
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

        if specification.is_indented:
            prefix, infix, suffix = StorageFormatManager.indented_whitespace
        else:
            prefix, infix, suffix = StorageFormatManager.unindented_whitespace

        class_name = type(specification.instance).__name__
        if as_storage_format:
            tools_package_name = specification.tools_package_name
            class_name_prefix = '{}.{}'
            class_name_prefix = class_name_prefix.format(
                tools_package_name, class_name)
        else:
            class_name_prefix = class_name

        positional_argument_pieces = []
        for value in specification.positional_argument_values:
            try:
                pieces = StorageFormatManager.format_one_value(
                    value,
                    as_storage_format=as_storage_format,
                    is_indented=specification.is_indented,
                    )
            except:
                print(value)
                raise
            for piece in pieces[:-1]:
                positional_argument_pieces.append(prefix + piece)
            positional_argument_pieces.append(prefix + pieces[-1] + suffix)

        keyword_argument_pieces = []
        for name in specification.keyword_argument_names:
            value = getattr(specification.instance, name)
            if value is None or isinstance(value, types.MethodType):
                continue
            if specification.keyword_argument_callables:
                callables = dict(specification.keyword_argument_callables)
                if name in callables:
                    value = callables[name](value)
            try:
                pieces = StorageFormatManager.format_one_value(
                    value,
                    as_storage_format=as_storage_format,
                    is_indented=specification.is_indented,
                    )
            except:
                print(value)
                raise
            pieces[0] = '{}={}'.format(name, pieces[0])
            for piece in pieces[:-1]:
                keyword_argument_pieces.append(prefix + piece)
            keyword_argument_pieces.append(prefix + pieces[-1] + suffix)

        if not as_storage_format and specification.is_bracketed:
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

        if not as_storage_format and specification.is_bracketed:
            result.append('>')

        if not specification.is_indented:
            return (''.join(result),)

        return tuple(result)

    @staticmethod
    def get_hash_values(subject):
        r'''Gets hash values for `subject`.

        The hash values are a tuple of the type of `subject`, the values of its
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
        values.append(type(subject))
        positional_argument_dictionary = \
            StorageFormatManager.get_positional_argument_dictionary(subject)
        keyword_argument_dictionary = \
            StorageFormatManager.get_keyword_argument_dictionary(subject)
        for key, value in sorted(positional_argument_dictionary.items()):
            values.append(make_hashable(value))
        for key, value in sorted(keyword_argument_dictionary.items()):
            values.append(make_hashable(value))
        return tuple(values)

    @staticmethod
    def get_import_statements(subject):
        r'''Gets import statements for `subject`.

        ..  container:: example

            **Example 1.** Gets import statements for object in Abjad mainline:

            ::

                >>> note = Note("c'4")
                >>> systemtools.StorageFormatManager.get_import_statements(
                ...     note
                ...     )
                ('from abjad.tools import scoretools',)

        Returns tuple of strings.
        '''
        manager = StorageFormatManager
        import_statements = set()
        classes = manager.get_types(subject)
        for class_ in classes:
            root_package_name = manager.get_root_package_name(class_)
            if root_package_name in ('builtins', '__builtin__'):
                continue
            elif root_package_name == 'abjad':
                tools_package_name = manager.get_tools_package_name(class_)
                import_statement = 'from abjad.tools import {}'.format(
                    tools_package_name)
            elif root_package_name == 'experimental':
                tools_package_name = manager.get_tools_package_name(class_)
                import_statement = 'from experimental.tools import {}'.format(
                    tools_package_name)
            else:
                import_statement = 'import {}'.format(root_package_name)
            import_statements.add(import_statement)
        return tuple(sorted(import_statements))

    @staticmethod
    def get_indentation_strings(is_indented):
        r'''Gets indentation strings.
        '''
        prefix, infix, suffix = '', '', ', '
        if is_indented:
            prefix, infix, suffix = '    ', '\n', ',\n'
        return prefix, infix, suffix

    @staticmethod
    def get_input_argument_values(subject):
        r'''Gets input argument values.
        '''
        return StorageFormatManager.get_positional_argument_values(subject) + \
            StorageFormatManager.get_keyword_argument_values(subject)

    @staticmethod
    def get_keyword_argument_dictionary(subject):
        r'''Gets keyword argument dictionary.
        '''
        names = StorageFormatManager.get_keyword_argument_names(subject)
        values = StorageFormatManager.get_keyword_argument_values(subject)
        assert len(names) == len(values)
        result = dict(list(zip(names, values)))
        return result

    @staticmethod
    def get_keyword_argument_names(subject):
        r'''Gets keyword argument names.
        '''
        return StorageFormatManager.get_signature_keyword_argument_names(
            subject)

    @staticmethod
    def get_keyword_argument_values(subject):
        r'''Gets keyword argument values.
        '''
        result = []
        for name in StorageFormatManager.get_keyword_argument_names(subject):
            argument = getattr(subject, name)
            result.append(argument)
        return tuple(result)

    @staticmethod
    def get_positional_argument_dictionary(subject):
        r'''Gets positional argument dictionary.
        '''
        names = StorageFormatManager.get_positional_argument_names(subject)
        values = StorageFormatManager.get_positional_argument_values(subject)
        assert len(names) == len(values)
        result = dict(list(zip(names, values)))
        return result

    @staticmethod
    def get_positional_argument_names(subject):
        r'''Gets positional argument names.
        '''
        return StorageFormatManager.get_signature_positional_argument_names(
            subject)

    @staticmethod
    def get_positional_argument_values(subject):
        r'''Gets positional argument values.
        '''
        names = StorageFormatManager.get_positional_argument_names(subject)
        result = []
        for name in names:
            result.append(getattr(subject, name))
        return tuple(result)

    @staticmethod
    def get_repr_format(
        subject,
        ):
        r'''Gets interpreter representation format.
        '''
        assert (
            '_repr_specification' in dir(subject) or
            hasattr(subject, '_repr_specification')
            )
        specification = subject._repr_specification
        pieces = StorageFormatManager.get_format_pieces(
            specification,
            as_storage_format=False,
            )
        return ''.join(pieces)

    @staticmethod
    def get_root_package_name(subject):
        r'''Gets root package name of `subject`.

        Returns string.
        '''
        if StorageFormatManager.is_instance(subject):
            class_ = type(subject)
        else:
            class_ = subject
        root_package_name, _, _ = class_.__module__.partition('.')
        return root_package_name

    @staticmethod
    def get_signature_keyword_argument_names(subject):
        r'''Gets signature keyword argument names.
        '''
        if hasattr(subject.__init__, '__func__'):
            initializer = subject.__init__.__func__
            if sys.version_info[0] == 2:
                defaults = initializer.func_defaults
                initializer_code = initializer.func_code
            else:
                defaults = initializer.__defaults__
                initializer_code = initializer.__code__
        elif hasattr(subject.__init__, '__defaults__'):
            defaults = subject.__init__.__defaults__
            initializer_code = subject.__init__.__code__
        else:
            return ()
        if defaults:
            keyword_argument_count = len(defaults)
            positional_argument_count = (
                initializer_code.co_argcount - keyword_argument_count - 1)
            start_index = 1 + positional_argument_count
            stop_index = start_index + keyword_argument_count
            return initializer_code.co_varnames[start_index:stop_index]
        else:
            return ()

    @staticmethod
    def get_signature_positional_argument_names(subject):
        r'''Gets signature positional argument names.
        '''
        if hasattr(subject.__init__, '__func__'):
            initializer = subject.__init__.__func__
            keyword_argument_count = 0
            if sys.version_info[0] == 2:
                if initializer.func_defaults:
                    keyword_argument_count = len(initializer.func_defaults)
                initializer_code = initializer.func_code
            else:
                if initializer.__defaults__:
                    keyword_argument_count = len(initializer.__defaults__)
                initializer_code = initializer.__code__
            positional_argument_count = (
                initializer_code.co_argcount - keyword_argument_count - 1)
            start_index, stop_index = 1, 1 + positional_argument_count
            return initializer_code.co_varnames[start_index:stop_index]
        return ()

    @staticmethod
    def get_storage_format(
        subject,
        ):
        r'''Gets storage format.
        '''
        assert (
            '_storage_format_specification' in dir(subject) or
            hasattr(subject, '_storage_format_specification')
            )
        specification = subject._storage_format_specification
        pieces = StorageFormatManager.get_format_pieces(
            specification,
            as_storage_format=True,
            )
        result = ''.join(pieces)
        return result

    @staticmethod
    def get_tools_package_name(subject):
        r'''Gets tools-package name of `subject`.

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_name(Note)
            'scoretools'

        Returns string.
        '''
        if StorageFormatManager.is_instance(subject):
            class_ = type(subject)
        else:
            class_ = subject
        class_name = class_.__name__
        parts = class_.__module__.split('.')
        if parts[0] in ('abjad', 'experimental', 'ide'):
            for part in reversed(class_.__module__.split('.')):
                if not part == class_name:
                    return part
        parts = class_.__module__.split('.')
        while parts and parts[-1] == class_name:
            parts.pop()
        return '.'.join(parts)

    @staticmethod
    def get_tools_package_qualified_class_name(object_):
        r'''Gets tools-package qualified class name of `object_`.

        ::

            >>> manager = systemtools.StorageFormatManager
            >>> manager.get_tools_package_qualified_class_name(Note)
            'scoretools.Note'

        Returns string.
        '''
        tools_package_name = StorageFormatManager.get_tools_package_name(
            object_)
        if StorageFormatManager.is_instance(object_):
            class_name = type(object_).__name__
        else:
            class_name = object_.__name__
        return '{}.{}'.format(tools_package_name, class_name)

    @staticmethod
    def get_types(subject, result=None):
        r'''Gets all non-builtin types referenced in storage format.

        ..  container:: example

            **Example 1.**

            ::

                >>> maker = rhythmmakertools.EvenDivisionRhythmMaker(
                ...     burnish_specifier=rhythmmakertools.BurnishSpecifier(
                ...         left_classes=[Rest],
                ...         left_counts=[1],
                ...         right_classes=[Rest],
                ...         right_counts=[2],
                ...         outer_divisions_only=True,
                ...         ),
                ...     )

            ::

                >>> types = systemtools.StorageFormatManager.get_types(maker)
                >>> for _ in types:
                ...     _
                ...
                <class 'abjad.tools.rhythmmakertools.BurnishSpecifier.BurnishSpecifier'>
                <class 'abjad.tools.rhythmmakertools.EvenDivisionRhythmMaker.EvenDivisionRhythmMaker'>
                <class 'abjad.tools.scoretools.Rest.Rest'>

        ..  container:: example

            **Example 2.**

            ::

                >>> dictionary = datastructuretools.TypedOrderedDict(
                ...     item_class=pitchtools.NamedPitch,
                ...     )

            ::

                >>> types = systemtools.StorageFormatManager.get_types(dictionary)
                >>> for _ in types:
                ...     _
                ...
                <class 'abjad.tools.datastructuretools.TypedOrderedDict.TypedOrderedDict'>
                <class 'abjad.tools.pitchtools.NamedPitch.NamedPitch'>

            .. todo:: Shouldn't the above example **not** return OrderedDict?

        Returns tuple of types.
        '''
        from abjad.tools import abctools

        if sys.version_info[0] == 2:
            type_type = types.TypeType
        else:
            type_type = type

        if result is None:
            result = set()
        manager = StorageFormatManager

        if isinstance(subject, str):
            return result

        arguments = []
        if not isinstance(subject, type_type):
            if hasattr(subject, '_storage_format_specification'):
                specification = subject._storage_format_specification
                for name in specification.keyword_argument_names:
                    value = getattr(subject, name)
                    arguments.append(value)
                for value in specification.positional_argument_values:
                    arguments.append(value)
            else:
                arguments.extend(manager.get_keyword_argument_values(subject))
                arguments.extend(manager.get_positional_argument_values(subject))

        if isinstance(subject, collections.Mapping):
            for key, value in subject.items():
                result.update(manager.get_types(key))
                result.update(manager.get_types(value))
        elif isinstance(subject, collections.Iterable):
            for value in subject:
                result.update(manager.get_types(value))

        arguments.append(subject)
        for argument in arguments:
            if not isinstance(argument, type_type):
                if argument is not subject:
                    result.update(manager.get_types(argument))
            if isinstance(argument, type_type):
                if not issubclass(argument, abctools.AbjadObject):
                    continue
            elif type(argument).__module__ in (
                'builtins',
                '__builtin__',
                'abc',
                ):
                continue
            if not isinstance(argument, type_type):
                if argument is not subject:
                    result.update(manager.get_types(argument))
                argument = type(argument)
            result.add(argument)

        result = sorted(result, key=lambda x: (x.__module__, x.__name__))

        return result

    @staticmethod
    def get_unique_python_path_parts(subject):
        r'''Gets unique Python path parts for `subject`.

        Returns tuple.
        '''
        if not isinstance(subject, type):
            subject = type(subject)
        path = '.'.join([subject.__module__, subject.__name__])
        parts = path.split('.')
        unique_parts = [parts[0]]
        for part in parts[1:]:
            if part != unique_parts[-1]:
                unique_parts.append(part)
        return unique_parts

    @staticmethod
    def is_instance(subject):
        r'''Is true when `subject` is instance. Otherwise false.

        Returns true or false.
        '''
        if isinstance(subject, type):
            return False
        elif type(subject) is subject.__class__:
            return True
        return False