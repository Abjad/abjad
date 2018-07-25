import inspect
import itertools
import numbers
import typing
import uqbar.enums
from abjad.system.Signature import Signature
from abjad.system.AbjadValueObject import AbjadValueObject


class Expression(AbjadValueObject):
    """
    Expression.

    ..  container:: example expression

        Makes identity expression:

        >>> expression = abjad.Expression()

        >>> expression() is None
        True

        >>> expression(99)
        99

        >>> expression([99, 99.25])
        [99, 99.25]

    ..  container:: example expression

        Makes integer initialization expression:

        >>> expression = abjad.Expression(evaluation_template='int({})')

        >>> expression()
        0

        >>> expression(99)
        99

        >>> expression(99.25)
        99

    ..  container:: example expression

        Makes binary integer initialization expression:

        >>> expression = abjad.Expression(evaluation_template='int({}, base=2)')

        >>> expression('1')
        1

        >>> expression('11')
        3

        >>> expression('111')
        7

    ..  container:: example expression

        Makes three-integer addition expression:

        >>> expression = abjad.Expression(
        ...     argument_count=3,
        ...     evaluation_template='{} + {} + {}',
        ...     )

        >>> expression(1, 2, 3)
        6

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_argument_count',
        '_argument_values',
        '_callbacks',
        '_evaluation_template',
        '_force_return',
        '_has_parentheses',
        '_is_composite',
        '_is_initializer',
        '_is_postfix',
        '_keywords',
        '_lone',
        '_map_operand',
        '_markup_maker_callback',
        '_module_names',
        '_name',
        '_next_name',
        '_precedence',
        '_proxy_class',
        '_qualified_method_name',
        '_string_template',
        '_subclass_hook',
        '_subexpressions',
        '_template',
        )

    _private_attributes_to_copy: typing.List[str] = []

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        argument_count=None,
        argument_values=None,
        callbacks=None,
        evaluation_template=None,
        force_return=None,
        has_parentheses=None,
        is_composite=None,
        is_initializer=None,
        is_postfix=None,
        keywords=None,
        lone=None,
        map_operand=None,
        markup_maker_callback=None,
        module_names=None,
        name=None,
        next_name=None,
        precedence=None,
        proxy_class=None,
        qualified_method_name=None,
        string_template=None,
        subclass_hook=None,
        subexpressions=None,
        template=None,
        ):
        if argument_count is not None:
            assert isinstance(argument_count, int) and 0 <= argument_count
        self._argument_count = argument_count
        if argument_values is not None:
            assert isinstance(argument_values, dict)
            argument_values = argument_values or None
        self._argument_values = argument_values
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks
        if not isinstance(evaluation_template, (str, type(None))):
            message = 'must be string or none: {!r}.'
            message = message.format(evaluation_template)
            raise TypeError(message)
        self._evaluation_template = evaluation_template
        self._force_return = force_return
        if has_parentheses is not None:
            has_parentheses = bool(has_parentheses)
        self._has_parentheses = has_parentheses
        if is_composite is not None:
            is_composite = bool(is_composite)
        self._is_composite = is_composite
        self._is_initializer = is_initializer
        if not isinstance(keywords, (dict, type(None))):
            message = 'keywords must be dictionary or none: {!r}.'
            message = message.format(keywords)
            raise TypeError(message)
        if is_postfix is not None:
            is_postfix = bool(is_postfix)
        self._is_postfix = is_postfix
        self._keywords = keywords
        if not isinstance(map_operand, (Expression, list, type(None))):
            message = 'must be expression, expression list or none: {!r}.'
            message = message.format(map_operand)
            raise TypeError(message)
        self._lone = lone
        self._map_operand = map_operand
        if markup_maker_callback is not None:
            assert isinstance(markup_maker_callback, str)
        self._markup_maker_callback = markup_maker_callback
        self._module_names = module_names
        if not isinstance(name, (str, type(None))):
            message = 'name must be string or none: {!r}.'
            message = message.format(name)
            raise TypeError(name)
        self._name = name
        if not isinstance(next_name, (str, type(None))):
            message = 'next name must be string or none: {!r}.'
            message = message.format(next_name)
            raise TypeError(next_name)
        self._next_name = next_name
        self._precedence = precedence
        self._proxy_class = proxy_class
        if not isinstance(string_template, (str, type(None))):
            message = 'must be string or none: {!r}.'
            message = message.format(string_template)
            raise TypeError(message)
        if qualified_method_name is not None:
            assert isinstance(qualified_method_name, str)
        self._qualified_method_name = qualified_method_name
        self._string_template = string_template
        if not isinstance(subclass_hook, (str, type(None))):
            message = 'must be string or none: {!r}.'
            message = message.format(subclass_hook)
            raise TypeError(message)
        self._subclass_hook = subclass_hook
        if subexpressions is not None:
            subexpressions = tuple(subexpressions)
        self._subexpressions = subexpressions
        self._template = template

    ### SPECIAL METHODS ###

    @Signature(
        markup_maker_callback='_make_expression_add_markup',
        )
    def __add__(self, i):
        """
        Gets proxy method or adds expressions.

        ..  container:: example expression

            Adds expressions:

            >>> expression_1 = abjad.Expression(
            ...     argument_count=3,
            ...     evaluation_template='{} + {} + {}',
            ...     )
            >>> expression_2 = abjad.Expression(
            ...     argument_count=2,
            ...     evaluation_template='{} + {}',
            ...     )
            >>> expression = expression_1 + expression_2
            >>> abjad.f(expression)
            abjad.Expression(
                argument_count=2,
                evaluation_template='{}.__add__({})',
                is_composite=True,
                markup_maker_callback='_make_add_expression_markup',
                qualified_method_name='abjad.Expression.__add__',
                string_template='{} + {}',
                subexpressions=(
                    abjad.Expression(
                        argument_count=3,
                        evaluation_template='{} + {} + {}',
                        ),
                    abjad.Expression(
                        argument_count=2,
                        evaluation_template='{} + {}',
                        ),
                    ),
                )

            >>> expression(1, 2, 3, 4, 5)
            15

        """
        if not isinstance(i, Expression):
            proxy_method = self.__getattr__('__add__')
            return proxy_method(i)
        evaluation_template = '{}.__add__({})'
        template = '{} + {}'
        lhs_module_names = self.module_names or []
        rhs_module_names = i.module_names or []
        module_names = lhs_module_names + rhs_module_names
        module_names = list(set(module_names))
        module_names.sort()
        module_names = module_names or None
        return type(self)(
            argument_count=2,
            evaluation_template=evaluation_template,
            is_composite=True,
            markup_maker_callback='_make_add_expression_markup',
            module_names=module_names,
            proxy_class=self.proxy_class,
            qualified_method_name='abjad.Expression.__add__',
            string_template=template,
            subexpressions=[self, i],
            )

    def __call__(self, *arguments, **keywords):
        """
        Calls expression on ``arguments`` with ``keywords``.

        ..  container:: example expression

            Calls identity expression:

            >>> expression = abjad.Expression()

            >>> expression() is None
            True

        Returns ouput of last callback.
        """
        arguments = list(arguments)
        results = []
        for subexpression in self.subexpressions or []:
            argument_count = subexpression.argument_count or 1
            arguments_ = []
            for i in range(argument_count):
                argument = arguments.pop(0)
                arguments_.append(argument)
            result = subexpression(*arguments_, **keywords)
            keywords = {}
            results.append(result)
        arguments = results or arguments
        if self.argument_count is not None:
            if len(arguments) != self.argument_count:
                message = '{} arguments (not {}) required: {!r}.'
                message = message.format(
                    self.argument_count,
                    len(arguments),
                    arguments,
                    )
                raise Exception(message)
        thread_arguments = False
        if self.evaluation_template is not None:
            result = self._evaluate(*arguments, **keywords)
            keywords = {}
        elif not arguments:
            result = None
        elif len(arguments) == 1:
            result = arguments[0]
        else:
            result = arguments
            thread_arguments = True
        for expression in self.callbacks or []:
            if expression.evaluation_template:
                if thread_arguments:
                    result = expression._evaluate(*result, **keywords)
                    thread_arguments = False
                else:
                    result = expression._evaluate(result, **keywords)
            else:
                if thread_arguments:
                    result = expression(*result, **keywords)
                    thread_arguments = False
                else:
                    result = expression(result, **keywords)
        return result

    def __dict__(self):
        """
        Gets attributes.

        Returns list or strings.
        """
        return dir(self)

    def __eq__(self, argument):
        """
        Is true when expression storage format equals ``argument`` storage
        format.

        ..  container:: example

            >>> expression_1 = abjad.Expression().sequence()
            >>> expression_2 = abjad.Expression().sequence()
            >>> expression_1 == expression_2
            True

            >>> expression_1 = abjad.Expression().sequence()
            >>> expression_2 = abjad.new(expression_1)
            >>> expression_1 == expression_2
            True

        ..  container:: example

            >>> expression_1 = abjad.Expression().sequence()
            >>> expression_2 = abjad.Expression().sequence().reverse()
            >>> expression_1 == expression_2
            False

            >>> expression_1 = abjad.Expression().sequence()
            >>> expression_1 == 'text'
            False

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats expression.

        ..  container:: example expression

            Formats identity expression:

            >>> expression = abjad.Expression()

            >>> abjad.f(expression)
            abjad.Expression()

        Returns string.
        """
        return super().__format__(format_specification=format_specification)

    def __getattr__(self, name):
        """
        Gets attribute ``name``.

        Returns proxy method when proxy class is set.

        Returns normally when proxy class is not set.
        """
        if self.__getattribute__('_proxy_class') is not None:
            if hasattr(self._proxy_class, name):
                proxy_object = self._proxy_class()
                if not hasattr(proxy_object, name):
                    message = 'proxy object {!r} has no attribute {!r}.'
                    message = message.format(proxy_object, name)
                    raise Exception(message)
                if not hasattr(proxy_object, '_expression'):
                    class_name = proxy_object.__name__
                    message = 'does not implement expression protocol: {}.'
                    message = message.format(class_name)
                    raise Exception(message)
                proxy_object._expression = self
                callable_ = getattr(proxy_object, name)
                assert callable(callable_), repr(callable_)
                if inspect.isfunction(callable_):
                    callable_.__dict__['frozen_expression'] = self
                return callable_
        message = '{} object has no attribute {!r}.'
        message = message.format(type(self).__name__, name)
        raise AttributeError(message)

    def __getitem__(self, argument):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__('__getitem__')
        return proxy_method(argument)

    def __hash__(self):
        """
        Hashes expression.

        Returns integer.
        """
        return super().__hash__()

    def __iadd__(self, i):  # type: ignore
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__('__iadd__')
        return proxy_method(i)

    def __radd__(self, i):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__('__radd__')
        return proxy_method(i)

    def __repr__(self):
        """
        Gets interpreter representation.

        ..  container:: example expression

            Gets interpreter representation of identity expression:

            >>> expression = abjad.Expression()

            >>> expression
            Expression()

        Returns string.
        """
        return super().__repr__()

    def __setitem__(self, i, argument):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__('__setitem__')
        return proxy_method(i, argument)

    def __str__(self):
        """
        Gets string representation of expression.

        ..  container:: example expression

            Gets string representation of identity expression:

            >>> expression = abjad.Expression()

            >>> str(expression)
            'Expression()'

        Returns string.
        """
        return super().__str__()

    ### PRIVATE METHODS ###

    def _apply_callback_markup(
        self,
        name,
        direction=None,
        previous_callback=None,
        ):
        import abjad
        if previous_callback and previous_callback.next_name:
            name = previous_callback.next_name
        markup = name
        if isinstance(markup, str):
            markup = abjad.Markup(markup).bold()
        if not self.callbacks:
            return markup
        callback = self.callbacks[0]
        if (previous_callback and
            previous_callback.is_composite and
            not callback.is_composite):
            markup = abjad.MarkupList(['(', markup, ')']).concat()
        markup = callback._make_method_markup(markup)
        previous_precedence = callback.precedence or 0
        previous_callback = callback
        for callback in self.callbacks[1:]:
            if previous_callback and previous_callback.next_name:
                markup = previous_callback.next_name
                if isinstance(markup, str):
                    markup = abjad.Markup(markup).bold()
            current_precedence = callback.precedence or 0
            parenthesize_argument = False
            if (previous_precedence < current_precedence and
                not previous_callback.is_initializer):
                parenthesize_argument = True
            elif previous_callback.is_composite:
                parenthesize_argument = True
            if previous_callback and previous_callback.next_name:
                parenthesize_argument = False
            if parenthesize_argument:
                markup = abjad.MarkupList(['(', markup, ')']).concat()
            markup = callback._make_method_markup(markup)
            previous_callback = callback
        markup = abjad.new(markup, direction=direction)
        return markup

    def _compile_callback_strings(self, name):
        string = name
        previous_callback = None
        for callback in self.callbacks or []:
            if previous_callback and previous_callback.next_name:
                string = previous_callback.next_name
            template = callback.string_template
            if template is None:
                message = 'callback {!r} has no string template.'
                message = message.format(callback)
                raise ValueError(message)
            try:
                string = template.format(string)
            except Exception as e:
                message = 'callback {!r} with template {!r}'
                message += ' and name {!r} raises {!r}.'
                message = message.format(callback, template, string, e)
                raise Exception(message)
            previous_callback = callback
        return string

    def _evaluate(self, *arguments, **keywords):
        import abjad
        assert self.evaluation_template
        if self.evaluation_template == 'map':
            return self._evaluate_map(*arguments)
        if self.evaluation_template == 'group_by':
            return self._evaluate_group_by(*arguments)
        if self.subclass_hook:
            assert isinstance(self.subclass_hook, str)
            subclass_hook = getattr(self, self.subclass_hook)
            return subclass_hook(*arguments)
        argument_count = self.argument_count or 1
        if (len(arguments) != argument_count and
            len(arguments) != 0):
            message = '{} {} (not {}) required: {!r}.'
            message = message.format(
                argument_count,
                abjad.String('argument').pluralize(argument_count),
                len(arguments),
                arguments,
                )
            raise Exception(message)
        globals_ = self._make_globals()
        statement = self.evaluation_template
        strings = []
        if self.is_initializer:
            for i, argument in enumerate(arguments):
                if argument is None:
                    continue
                string = '__argument_{i}'
                string = string.format(i=i)
                globals_[string] = argument
                strings.append(string)
            keywords_ = self.keywords or {}
            keywords_.update(keywords)
            for key, value in keywords_.items():
                value = self._to_evaluable_string(value)
                string = '{key}={value}'
                string = string.format(key=key, value=value)
                strings.append(string)
            strings = ', '.join(strings)
            statement = '{class_name}({strings})'
            class_name = self.evaluation_template
            statement = statement.format(
                class_name=class_name,
                strings=strings,
                )
        else:
            if not arguments:
                statement = statement.replace('{}', '')
            else:
                strings = []
                __argument_0 = arguments[0]
                for i, argument in enumerate(arguments):
                    string = '__argument_' + str(i)
                    globals_[string] = argument
                    strings.append(string)
                try:
                    statement = statement.format(*strings)
                except Exception as exception:
                    message = 'statement {!r} raises {!r}.'
                    message = message.format(statement, exception.args[0])
                    raise type(exception)(message)
        try:
            result = eval(statement, globals_)
        except Exception as exception:
            message = 'evaluable statement {!r} raises {!r}.'
            message = message.format(statement, exception.args[0])
            raise type(exception)(message)
        if self.force_return:
            result = __argument_0
        return result

    def _evaluate_group_by(self, *arguments):
        assert len(arguments) == 1, repr(arguments)
        globals_ = self._make_globals()
        assert '__argument_0' not in globals_
        __argument_0 = arguments[0]
        class_ = type(__argument_0)
        map_operand = self.map_operand
        if map_operand is None:
            def map_operand(argument):
                return True
        globals_['__argument_0'] = __argument_0
        globals_['class_'] = class_
        globals_['map_operand'] = map_operand
        globals_['itertools'] = itertools
        statement = 'itertools.groupby(__argument_0, map_operand)'
        try:
            pairs = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            message = '{!r} raises {!r}.'
            message = message.format(statement, e)
            raise Exception(message)
        items = []
        for count, group in pairs:
            try:
                item = class_(items=group)
            except TypeError:
                pass
            items.append(item)
        try:
            result = class_(items)
        except TypeError:
            result = items
        return result

    def _evaluate_map(self, *arguments):
        assert len(arguments) == 1, repr(arguments)
        assert self.map_operand is not None
        globals_ = self._make_globals()
        assert '__argument_0' not in globals_
        __argument_0 = arguments[0]
        class_ = type(__argument_0)
        map_operand = self.map_operand
        globals_['__argument_0'] = __argument_0
        globals_['class_'] = class_
        globals_['map_operand'] = map_operand
        statement = '[map_operand(_) for _ in __argument_0]'
        try:
            result = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            message = '{!r} raises {!r}.'
            message = message.format(statement, e)
            raise Exception(message)
        try:
            result = class_(result)
        except TypeError:
            pass
        return result

    @classmethod
    def _frame_to_callback(
        class_,
        frame,
        evaluation_template=None,
        force_return=None,
        is_composite=None,
        is_initializer=None,
        is_postfix=None,
        keywords=None,
        map_operand=None,
        module_names=None,
        precedence=None,
        string_template=None,
        subclass_hook=None,
        ):
        if evaluation_template is None:
            evaluation_template = class_._get_evaluation_template(frame)
        result = class_._read_signature_decorator(frame)
        argument_values = result['argument_values']
        qualified_method_name = result['qualified_method_name']
        string_template = result['string_template'] or string_template
        return class_(
            argument_values=argument_values,
            evaluation_template=evaluation_template,
            force_return=force_return,
            is_composite=is_composite,
            is_initializer=is_initializer,
            is_postfix=is_postfix,
            keywords=keywords,
            map_operand=map_operand,
            module_names=module_names,
            precedence=precedence,
            qualified_method_name=qualified_method_name,
            string_template=string_template,
            subclass_hook=subclass_hook,
            )

    @staticmethod
    def _get_callback(callback_name, function, function_self):
        callback = None
        callback_name = getattr(function, callback_name, None)
        if callback_name is not None:
            assert isinstance(callback_name, str), repr(callback_name)
            callback = getattr(function_self, callback_name, None)
            if callback is None:
                callback = getattr(Expression, callback_name, None)
            if callback is None:
                message = 'can not find callback {!r}.'
                message = message.format(callback_name)
                raise ValueError(message)
        return callback

    @staticmethod
    def _get_evaluation_template(frame, static_class=None):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            arguments = Expression._wrap_arguments(
                frame,
                static_class=static_class,
                )
            template = '{{}}.{function_name}({arguments})'
            template = template.format(
                function_name=function_name,
                arguments=arguments,
                )
        finally:
            del frame
        return template

    def _get_format_specification(self):
        import abjad
        if self.template is None:
            return super()._get_format_specification()
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.template],
            storage_format_forced_override=self.template,
            storage_format_kwargs_names=(),
            )

    @staticmethod
    def _get_method_name(
        function_name,
        function,
        function_self,
        argument_values,
        ):
        if getattr(function, 'method_name', None) is not None:
            return getattr(function, 'method_name')
        method_name_callback = Expression._get_callback(
            'method_name_callback',
            function,
            function_self,
            )
        if method_name_callback:
            return method_name_callback(**argument_values)
        return function_name

    def _is_singular_get_item(self):
        if not self.callbacks:
            return False
        callback = self.callbacks[-1]
        if getattr(callback, '_lone', None):
            return True
        if (callback.evaluation_template == 'group_by' and
            callback.map_operand is None):
            return True
        if not callback.qualified_method_name.endswith('__getitem__'):
            return False
        template = callback.evaluation_template
        if 'slice' in template:
            return False
        if 'Pattern' in template:
            return False
        if 'abjad.index' in template:
            return False
        return True

    @staticmethod
    def _make___add___markup(markup, argument):
        import abjad
        markup_list = abjad.MarkupList()
        markup_list.append(markup)
        markup_list.append('+')
        markup_list.append(str(argument))
        markup = markup_list.line()
        return markup

    @staticmethod
    def _make___add___string_template(argument):
        return '{} + ' + str(argument)

    @staticmethod
    def _make___getitem___markup(markup, argument):
        import abjad
        markup_list = abjad.MarkupList()
        markup_list.append(markup)
        string = Expression._make_subscript_string(argument, markup=True)
        subscript_markup = abjad.Markup(string).sub()
        markup_list.append(subscript_markup)
        markup = markup_list.concat()
        return markup

    @staticmethod
    def _make___getitem___string_template(argument):
        string = Expression._make_subscript_string(argument, markup=False)
        return '{}' + string

    @staticmethod
    def _make___radd___markup(markup, argument):
        import abjad
        markup_list = abjad.MarkupList()
        markup_list.append(str(argument))
        markup_list.append('+')
        markup_list.append(markup)
        markup = markup_list.line()
        return markup

    @staticmethod
    def _make___radd___string_template(argument):
        return str(argument) + ' + {}'

    @staticmethod
    def _make_establish_equivalence_markup(lhs, rhs):
        import abjad
        markup_list = abjad.MarkupList()
        lhs = abjad.Markup(lhs).bold()
        markup_list.append(lhs)
        markup_list.append('=')
        assert isinstance(rhs, abjad.Markup)
        markup_list.append(rhs)
        markup = markup_list.line()
        return markup

    def _make_evaluable_keywords(self, keywords):
        result = {}
        for key, value in keywords.items():
            if isinstance(value, type):
                value = self._to_evaluable_string(value)
            result[key] = value
        return result

    @staticmethod
    def _make_expression_add_markup(markups):
        import abjad
        assert len(markups) == 2
        markup_list = abjad.MarkupList()
        markup_list.append(markups[0])
        markup_list.append('+')
        markup_list.append(markups[1])
        markup = markup_list.line()
        return markup

    @staticmethod
    def _make_function_markup(
        markup,
        method_name,
        argument_list_callback,
        method,
        argument_values,
        ):
        import abjad
        if argument_list_callback:
            arguments = argument_list_callback(**argument_values)
        else:
            arguments = Expression._wrap_arguments_new(method, argument_values)
        markup_list = abjad.MarkupList()
        markup_list.append(method_name + '(')
        markup_list.append(markup)
        if arguments:
            markup_list.append(', ' + arguments + ')')
        else:
            markup_list.append(')')
        markup = markup_list.concat()
        return markup

    # TODO: eventually do not pass frame
    @staticmethod
    def _make_function_string_template(
        frame,
        method_name,
        argument_values,
        argument_list_callback,
        ):
        if argument_list_callback:
            arguments = argument_list_callback(**argument_values)
        else:
            arguments = Expression._wrap_arguments(frame)
        if arguments:
            template = '{}({{}}, {})'
            template = template.format(method_name, arguments)
        else:
            template = method_name + '({})'
        return template

    def _make_globals(self):
        import abjad
        globals_ = {'abjad': abjad}
        globals_.update(abjad.__dict__.copy())
        module_names = self.module_names or []
        if self.qualified_method_name is not None:
            parts = self.qualified_method_name.split('.')
            root_package_name = parts[0]
            module_names.append(root_package_name)
        for module_name in module_names:
            module = __import__(module_name)
            globals_[module_name] = module
        return globals_

    def _make_initializer_callback(
        self,
        class_,
        module_names=None,
        string_template=None,
        **keywords
        ):
        assert isinstance(class_, type), repr(class_)
        if not hasattr(class_, '_expression'):
            message = 'class does not implement expression protocol: {!r}.'
            message = message.format(class_)
            raise TypeError(message)
        parts = class_.__module__.split('.')
        if parts[-1] != class_.__name__:
            parts.append(class_.__name__)
        if 'abjad' in parts:
            parts = [_ for _ in parts if 'tools' not in _]
        evaluation_template = '.'.join(parts)
        keywords = self._make_evaluable_keywords(keywords)
        keywords = keywords or None
        return type(self)(
            evaluation_template=evaluation_template,
            is_initializer=True,
            keywords=keywords,
            module_names=module_names,
            string_template=string_template,
            )

    def _make_method_markup(self, markup):
        import abjad
        if self.is_initializer:
            assert self.qualified_method_name is None
            return abjad.Markup(markup)
        qualified_method_name = self.qualified_method_name
        assert isinstance(qualified_method_name, str), repr(self)
        if qualified_method_name == 'abjad.Expression.establish_equivalence':
            markup = self._make_establish_equivalence_markup(
                self.next_name,
                markup,
                )
            return markup
        assert '.' in qualified_method_name, repr(self)
        globals_ = self._make_globals()
        method = eval(qualified_method_name, globals_)
        if not getattr(method, 'has_signature_decorator', False):
            message = '{} has no signature decorator.'
            message = message.format(method)
            raise Exception(message)
        callback_name = getattr(method, 'markup_maker_callback', None)
        if callback_name is not None:
            parts = qualified_method_name.split('.')
            parts.pop(-1)
            parts.append(callback_name)
            qualified_callback_name = '.'.join(parts)
            try:
                callback = eval(qualified_callback_name, globals_)
            except AttributeError:
                callback = getattr(self, callback_name)
            argument_values = self.argument_values or {}
            markup = callback(markup, **argument_values)
            return markup
        callback_name = getattr(method, 'method_name_callback', None)
        if callback_name is not None:
            parts = qualified_method_name.split('.')
            parts.pop(-1)
            parts.append(callback_name)
            callback_name = '.'.join(parts)
            callback = eval(callback_name, globals_)
            method_name = callback(**self.argument_values)
        elif getattr(method, 'method_name', None) is not None:
            method_name = method.method_name
        else:
            method_name = method.__name__
        assert isinstance(method_name, str), repr((self, method))
        if getattr(method, 'is_operator', None):
            subscript = getattr(method, 'subscript', None)
            if subscript is not None:
                subscript = self.argument_values[subscript]
            superscript = getattr(method, 'superscript', None)
            if superscript is not None:
                superscript = self.argument_values[superscript]
            markup = Expression._make_operator_markup(
                markup,
                method_name=method_name,
                subscript=subscript,
                superscript=superscript,
                )
        else:
            argument_list_callback = getattr(method, 'argument_list_callback')
            if argument_list_callback is not None:
                parts = qualified_method_name.split('.')
                parts.pop(-1)
                parts.append(argument_list_callback)
                qualified_callback_name = '.'.join(parts)
                argument_list_callback = eval(
                    qualified_callback_name,
                    globals_,
                    )
            markup = Expression._make_function_markup(
                markup,
                method_name,
                argument_list_callback,
                method,
                self.argument_values,
                )
        return markup

    @staticmethod
    def _make_operator_markup(
        markup,
        method_name=None,
        subscript=None,
        superscript=None,
        ):
        import abjad
        markup_list = abjad.MarkupList([method_name, markup])
        if superscript is not None:
            superscript = abjad.Markup(str(superscript))
            superscript = superscript.super()
            markup_list.insert(1, superscript)
        if subscript is not None:
            subscript = abjad.Markup(str(subscript))
            subscript = subscript.sub()
            markup_list.insert(1, subscript)
        markup = markup_list.concat()
        return markup

    @staticmethod
    def _make_operator_string_template(
        method_name=None,
        subscript=None,
        superscript=None,
        ):
        template = method_name
        if superscript is not None:
            template += str(superscript)
        if subscript is not None:
            template += str(subscript)
        template += '({})'
        return template

    @staticmethod
    def _make_subscript_string(i, markup=False):
        import abjad
        if isinstance(i, (int, abjad.Pattern)):
            if markup:
                subscript_string = '{i}'
            else:
                subscript_string = '[{i}]'
            start = stop = step = None
        elif isinstance(i, slice):
            if i.step is not None:
                raise NotImplementedError
            if i.start is None and i.stop is None:
                subscript_string = '[:]'
            elif i.start is None:
                subscript_string = '[:{stop}]'
            elif i.stop is None:
                subscript_string = '[{start}:]'
            else:
                subscript_string = '[{start}:{stop}]'
            start = i.start
            stop = i.stop
            step = i.step
        else:
            message = 'must be integer or slice: {!r}.'
            message = message.format(i)
            raise TypeError(message)
        subscript_string = subscript_string.format(
            i=i,
            start=start,
            stop=stop,
            step=step,
            )
        return subscript_string

    @staticmethod
    def _read_signature_decorator(frame):
        try:
            function_name = inspect.getframeinfo(frame).function
            argument_info = inspect.getargvalues(frame)
            assert argument_info.args[0] == 'self'
            function_self = argument_info.locals['self']
            function = getattr(function_self, function_name)
            class_ = function_self.__class__
            parts = class_.__module__.split('.')
            if parts[-1] != class_.__name__:
                parts.append(class_.__name__)
            if 'abjad' in parts:
                parts = [_ for _ in parts if 'tools' not in _]
            parts.append(function_name)
            qualified_method_name = '.'.join(parts)
            assert '.' in qualified_method_name
            argument_values = {}
            if not getattr(function, 'has_signature_decorator', False):
                return {
                    'argument_values': argument_values,
                    'qualified_method_name': qualified_method_name,
                    'string_template': None,
                    }
            argument_names = argument_info.args[1:]
            for argument_name in argument_names:
                argument_value = argument_info.locals[argument_name]
                argument_values[argument_name] = argument_value
            string_template_callback = Expression._get_callback(
                'string_template_callback',
                function,
                function_self,
                )
            if string_template_callback is not None:
                string_template = string_template_callback(**argument_values)
            elif getattr(function, 'is_operator', None):
                method_name = Expression._get_method_name(
                    function_name,
                    function,
                    function_self,
                    argument_values,
                    )
                subscript = getattr(function, 'subscript', None)
                if subscript is not None:
                    subscript = argument_info.locals[subscript]
                superscript = getattr(function, 'superscript', None)
                if superscript is not None:
                    superscript = argument_info.locals[superscript]
                string_template = Expression._make_operator_string_template(
                    method_name=method_name,
                    subscript=subscript,
                    superscript=superscript,
                    )
            else:
                method_name = Expression._get_method_name(
                    function_name,
                    function,
                    function_self,
                    argument_values,
                    )
                argument_list_callback = Expression._get_callback(
                    'argument_list_callback',
                    function,
                    function_self,
                    )
                # TODO: eventually do not pass frame
                string_template = Expression._make_function_string_template(
                    frame,
                    method_name,
                    argument_values,
                    argument_list_callback,
                    )
        finally:
            del frame
        return {
            'argument_values': argument_values,
            'qualified_method_name': qualified_method_name,
            'string_template': string_template,
            }

    @staticmethod
    def _to_evaluable_string(argument):
        if argument is None:
            pass
        elif isinstance(argument, str):
            argument = repr(argument)
        elif isinstance(argument, numbers.Number):
            argument = str(argument)
        elif isinstance(argument, (list, tuple)):
            item_strings = []
            item_count = len(argument)
            for item in argument:
                item_string = Expression._to_evaluable_string(item)
                item_strings.append(item_string)
            items = ', '.join(item_strings)
            if isinstance(argument, list):
                argument = f'[{items}]'
            elif isinstance(argument, tuple):
                if item_count == 1:
                    items += ','
                argument = f'({items})'
            else:
                raise Exception(repr(argument))
        elif isinstance(argument, slice):
            argument = repr(argument)
        elif isinstance(argument, uqbar.enums.StrictEnumeration):
            argument = f'abjad.{repr(argument)}'
        # abjad object
        elif not inspect.isclass(argument):
            try:
                argument = format(argument, 'storage')
            except (TypeError, ValueError):
                raise Exception(f'can not make storage format: {argument!r}.')
        # abjad class
        elif inspect.isclass(argument) and 'abjad' in argument.__module__:
            argument = argument.__module__.split('.')
            argument = argument[-2:]
            argument = '.'.join(argument)
        # builtin class like tuple in classes=(tuple,)
        elif inspect.isclass(argument) and 'abjad' not in argument.__module__:
            argument = argument.__name__
        else:
            raise Exception(f'can not make evaluable string: {argument!r}.')
        return argument

    @staticmethod
    def _wrap_arguments(frame, static_class=None):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            argument_info = inspect.getargvalues(frame)
            if static_class:
                method_name = frame.f_code.co_name
                static_method = getattr(static_class, method_name)
                signature = inspect.signature(static_method)
                argument_names = argument_info.args[:]
            else:
                assert argument_info.args[0] == 'self'
                self = argument_info.locals['self']
                function = getattr(self, function_name)
                signature = inspect.signature(function)
                argument_names = argument_info.args[1:]
            argument_strings = []
            for argument_name in argument_names:
                argument_value = argument_info.locals[argument_name]
                parameter = signature.parameters[argument_name]
                # positional argument
                if parameter.default == inspect.Parameter.empty:
                    argument_value = Expression._to_evaluable_string(
                        argument_value
                        )
                    argument_string = argument_value
                    argument_strings.append(argument_string)
                # keyword argument
                elif argument_value != parameter.default:
                    argument_string = '{argument_name}={argument_value}'
                    argument_value = Expression._to_evaluable_string(
                        argument_value)
                    argument_string = argument_string.format(
                        argument_name=argument_name,
                        argument_value=argument_value,
                        )
                    argument_strings.append(argument_string)
            arguments = ', '.join(argument_strings)
        finally:
            del frame
        return arguments

    @staticmethod
    def _wrap_arguments_new(method, argument_values):
        signature = inspect.signature(method)
        argument_names = [_ for _ in signature.parameters][1:]
        argument_strings = []
        for argument_name in argument_names:
            argument_value = argument_values[argument_name]
            parameter = signature.parameters[argument_name]
            if argument_value != parameter.default:
                argument_string = '{argument_name}={argument_value}'
                argument_value = Expression._to_evaluable_string(
                    argument_value)
                argument_string = argument_string.format(
                    argument_name=argument_name,
                    argument_value=argument_value,
                    )
                argument_strings.append(argument_string)
        arguments = ', '.join(argument_strings)
        return arguments

    ### PUBLIC PROPERTIES ###

    @property
    def argument_count(self):
        """
        Gets argument count.

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        """
        return self._argument_count

    @property
    def argument_values(self):
        """
        Gets argument values.

        Defaults to none.

        Set to dictionary or none.

        Returns dictionary or none.
        """
        return self._argument_values

    @property
    def callbacks(self):
        """
        Gets callbacks.

        ..  container:: example expression

            Defaults to none:

            >>> expression = abjad.Expression()
            >>> expression.callbacks is None
            True

        Set to callbacks or none.
        """
        if self._callbacks:
            return list(self._callbacks)

    @property
    def evaluation_template(self):
        """
        Gets evaluation template.

        Defaults to none.

        Set to string.

        Returns string.
        """
        return self._evaluation_template

    @property
    def force_return(self):
        """
        Is true when expression should return primary input argument.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._force_return

    @property
    def has_parentheses(self):
        """
        Is true when expression has parentheses.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._has_parentheses

    @property
    def is_composite(self):
        """
        Is true when expression is composite.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._is_composite

    @property
    def is_initializer(self):
        """
        Is true when expression is initializer.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._is_initializer

    @property
    def is_postfix(self):
        """
        Is true when expression is postfix.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._is_postfix

    @property
    def is_selector(self):
        """
        Is true when expression is selector.

        ..  container:: example

            >>> expression = abjad.select().leaf(0)
            >>> expression.is_selector
            True

            >>> expression = abjad.sequence().rotate(n=-1)
            >>> expression.is_selector
            False

        """
        if self.callbacks:
            first_callback = self.callbacks[0]
            if '.Selection' in first_callback.evaluation_template:
                return True
        return False

    @property
    def keywords(self):
        """
        Gets keywords.

        Defaults to none.

        Set to dictionary or none.

        Returns dictionary or none.
        """
        return self._keywords

    @property
    def lone(self):
        """
        Is true when expression return a singular get-item.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        """
        return self._lone

    @property
    def map_operand(self):
        """
        Gets expression to map.

        Defaults to none.

        Set to expression or none.

        Returns expression or none.
        """
        return self._map_operand

    @property
    def markup_maker_callback(self):
        """
        Gets markup-maker callback.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._markup_maker_callback

    @property
    def module_names(self):
        """
        Gets module names.

        Defaults to none.

        Set to strings or none.

        Returns strings or none.
        """
        return self._module_names

    @property
    def name(self):
        """
        Gets name.

        ..  container:: example expression

            Preserves name after initializer callback:

            >>> expression = abjad.Expression(name='J')
            >>> expression.name
            'J'

            >>> expression = expression.sequence()
            >>> expression.name
            'J'

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._name

    @property
    def next_name(self):
        """
        Gets next name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._next_name

    @property
    def precedence(self):
        """
        Gets precedence.

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        """
        return self._precedence

    @property
    def proxy_class(self):
        """
        Gets proxy class.

        Defaults to none.

        Set to class or none.

        Returns class or none.
        """
        return self._proxy_class

    @property
    def qualified_method_name(self):
        """
        Gets qualified method name of expression.

        Returns string or none.
        """
        return self._qualified_method_name

    @property
    def string_template(self):
        """
        Gets string template.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._string_template

    @property
    def subclass_hook(self):
        """
        Gets subclass hook.

        Only to be set by expression subclasses.

        Set to name of custom evaluation method.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        """
        return self._subclass_hook

    @property
    def subexpressions(self):
        """
        Gets subexpressions.

        Defaults to none.

        Set to expressions or none.

        Returns list of expressions or none.
        """
        return self._subexpressions

    @property
    def template(self):
        """
        Gets template.

        Returns string or none.
        """
        return self._template

    ### PUBLIC METHODS ###

    def append_callback(self, callback):
        """
        Appends callback to expression.

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression.callbacks is None
            True

            >>> callback = abjad.Expression(evaluation_template='int({})')
            >>> expression = expression.append_callback(callback)
            >>> for callback in expression.callbacks:
            ...     callback
            Expression(evaluation_template='int({})')

            >>> callback = abjad.Expression(evaluation_template='{}**2')
            >>> expression = expression.append_callback(callback)
            >>> for expression in expression.callbacks:
            ...     expression
            Expression(evaluation_template='int({})')
            Expression(evaluation_template='{}**2')

        Returns new expression.
        """
        import abjad
        callbacks = self.callbacks or []
        callbacks = callbacks + [callback]
        return abjad.new(self, callbacks=callbacks)

    def color(self, argument, colors=None):
        """Colors ``argument``.

        Returns none.
        """
        import abjad
        if self._is_singular_get_item():
            colors = colors or ['green']
            color = colors[0]
            abjad.label(argument).color_leaves(color=color)
        else:
            colors = colors or ['red', 'blue']
            colors = abjad.CyclicTuple(colors)
            for i, item in enumerate(argument):
                color = colors[i]
                abjad.label(item).color_leaves(color=color)

    def establish_equivalence(self, name):
        r"""
        Makes new expression with ``name``.

        ..  container:: example expression

            >>> expression = abjad.Expression(name='J')
            >>> expression = expression.pitch_class_segment()
            >>> expression = expression.rotate(n=1)
            >>> expression = expression.rotate(n=2)
            >>> expression = expression.establish_equivalence(name='Q')

            >>> expression([-2, -1.5, 6, 7, -1.5, 7])
            PitchClassSegment([7, 10.5, 7, 10, 10.5, 6])

            >>> expression.get_string()
            'Q = r2(r1(J))'

            >>> markup = expression.get_markup()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \line
                        {
                            \bold
                                Q
                            =
                            \concat
                                {
                                    r
                                    \sub
                                        2
                                    \concat
                                        {
                                            r
                                            \sub
                                                1
                                            \bold
                                                J
                                        }
                                }
                        }
                    }

        Returns new expression.
        """
        template = '{name} = {{}}'
        template = template.format(name=name)
        callback = self.make_callback(
            evaluation_template='{}',
            is_composite=True,
            next_name=name,
            qualified_method_name='abjad.Expression.establish_equivalence',
            string_template=template,
            )
        return self.append_callback(callback)

    def get_markup(self, direction=None, name=None):
        """
        Gets markup directly.

        Avoids markup expressions.

        Returns markup or none.
        """
        import abjad
        argument_count = self.argument_count or 1
        markup = None
        if argument_count <= 1:
            if name is None:
                name = self.name
            if name is None:
                for callback in self.callbacks or []:
                    if callback.name is not None:
                        name = callback.name
                        break
            if name is None:
                message = 'expression name not found: {!r}.'
                message = message.format(self)
                raise ValueError(message)
            #markup = self._compile_callback_markup(name)
            markup = self._apply_callback_markup(name)
        else:
            markups = []
            for subexpression in self.subexpressions or []:
                #markup = subexpression.get_markup_directly()
                markup = subexpression.get_markup()
                markups.append(markup)
            if len(markups) != argument_count:
                message = 'argument count of {} with {} markups found.'
                message = message.format(argument_count, len(markups))
                raise ValueError(message)
            markup = self._make_method_markup(markups)
            #markup = self._compile_callback_markup(
            markup = self._apply_callback_markup(
                markup,
                previous_callback=self,
                )
        if markup is not None:
            markup = abjad.new(markup, direction=direction)
        return markup

    def get_string(self, name=None):
        """
        Gets string.

        ..  container:: example

            Gets string for sequence expression:

            ..  container:: example expression

                Without name:

                >>> expression = abjad.sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.rotate(n=2)

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([2, 1, 6, 5, 4, 3])

                >>> abjad.Expression.get_string(expression, name='J')
                'r2(R(J))'

            ..  container:: example expression

                With name:

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.rotate(n=2)

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([2, 1, 6, 5, 4, 3])

                >>> abjad.Expression.get_string(expression)
                'r2(R(J))'

                Overrides name:

                >>> abjad.Expression.get_string(expression, name='K')
                'r2(R(K))'

        ..  container:: example

            Gets string for segment expression:

            ..  container:: example expression

                Without name:

                >>> expression = abjad.Expression()
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.invert()
                >>> expression = expression.rotate(n=2)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([1.5, 5, 2, 1.5, 6, 5])

                >>> abjad.Expression.get_string(expression, name='J')
                'r2(I(J))'

            ..  container:: example expression

                With name:

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.invert()
                >>> expression = expression.rotate(n=2)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([1.5, 5, 2, 1.5, 6, 5])

                >>> abjad.Expression.get_string(expression)
                'r2(I(J))'

                Overrides name:

                >>> abjad.Expression.get_string(expression, name='K')
                'r2(I(K))'

        Returns string or none.
        """
        argument_count = self.argument_count or 1
        if argument_count <= 1:
            if name is None:
                name = self.name
            if name is None:
                for callback in self.callbacks or []:
                    if callback.name is not None:
                        name = callback.name
                        break
            if name is None:
                message = 'expression name not found: {!r}.'
                message = message.format(self)
                raise ValueError(message)
            return self._compile_callback_strings(name)
        else:
            strings = []
            for subexpression in self.subexpressions or []:
                string = subexpression.get_string()
                strings.append(string)
            if len(strings) != argument_count:
                message = 'argument count of {} with {} strings found.'
                message = message.format(argument_count, len(strings))
                raise ValueError(message)
            template = self.string_template
            if template is None:
                message = 'expression has no string template: {!r}.'
                message = message.format(self)
                raise ValueError(message)
            try:
                string = template.format(*strings)
            except Exception as e:
                message = '{!r} with template {!r} raises {!r}.'
                message = message.format(self, template, e)
                raise Exception(message)
            return self._compile_callback_strings(string)

    def label(self, **keywords):
        r"""
        Makes label expression.

        ..  container:: example

            Makes expression to label logical tie durations:

            ..  container:: example

                >>> staff = abjad.Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")

            ..  container:: example expression

                >>> expression = abjad.Expression()
                >>> expression = expression.label()
                >>> expression = expression.with_durations()

                >>> expression(staff)
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        c'4.
                        ^ \markup {
                            \fraction
                                3
                                8
                            }
                        d'8
                        ^ \markup {
                            \fraction
                                1
                                2
                            }
                        ~
                        d'4.
                        e'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        [
                        ef'16
                        ^ \markup {
                            \fraction
                                1
                                16
                            }
                        ]
                    }

        Returns expression.
        """
        import abjad
        class_ = abjad.Label
        callback = self._make_initializer_callback(class_, **keywords)
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    @staticmethod
    def make_callback(
        argument_count=None,
        evaluation_template=None,
        force_return=None,
        has_parentheses=None,
        is_composite=None,
        is_initializer=None,
        is_postfix=None,
        keywords=None,
        map_operand=None,
        module_names=None,
        next_name=None,
        precedence=None,
        qualified_method_name=None,
        string_template=None,
        ):
        """
        Makes callback.

        Returns expression.
        """
        return Expression(
            argument_count=argument_count,
            evaluation_template=evaluation_template,
            force_return=force_return,
            has_parentheses=has_parentheses,
            is_composite=is_composite,
            is_initializer=is_initializer,
            is_postfix=is_postfix,
            keywords=keywords,
            map_operand=map_operand,
            module_names=module_names,
            next_name=next_name,
            precedence=precedence,
            qualified_method_name=qualified_method_name,
            string_template=string_template,
            )

    def pitch_class_segment(self, **keywords):
        r"""
        Makes pitch-class segment expression.

        ..  container:: example

            Makes expression to transpose pitch-class segment:

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> J = abjad.PitchClassSegment(items=items)
            >>> J
            PitchClassSegment([10, 10.5, 6, 7, 10.5, 7])

            >>> abjad.show(J) # doctest: +SKIP

            ..  container:: example expression

                >>> expression = abjad.Expression(name='J')
                >>> expression = expression.pitch_class_segment()
                >>> expression = expression.transpose(n=13)

                >>> expression([-2, -1.5, 6, 7, -1.5, 7])
                PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])

                >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                >>> markup = expression.get_markup()
                >>> abjad.show(segment, figure_name=markup) # doctest: +SKIP

                ..  docs::

                    >>> lilypond_file = segment.__illustrate__(
                    ...     figure_name=markup,
                    ...     )
                    >>> abjad.f(lilypond_file[abjad.Voice])
                    \new Voice
                    {
                        b'8
                        ^ \markup {
                            \concat
                                {
                                    T
                                    \sub
                                        13
                                    \bold
                                        J
                                }
                            }
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|." %! SCORE1
                        \override Score.BarLine.transparent = ##f
                    }

        Returns expression.
        """
        import abjad
        class_ = abjad.PitchClassSegment
        callback = self._make_initializer_callback(
            class_,
            string_template='{}',
            **keywords
            )
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    # TODO: add examples
    def pitch_set(self, **keywords):
        """
        Makes pitch set expression.

        Returns expression.
        """
        import abjad
        class_ = abjad.PitchSet
        callback = self._make_initializer_callback(
            class_,
            string_template='{}',
            **keywords
            )
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    def print(self, argument):
        """
        Prints ``argument``.

        Returns none.
        """
        if self._is_singular_get_item():
            print(repr(argument))
        else:
            for item in argument:
                print(repr(item))

    def select(self, **keywords):
        r"""
        Makes select expression.

        ..  container:: example

            Makes expression to select leaves:

            ..  container:: example

                >>> staff = abjad.Staff()
                >>> staff.append(abjad.Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                >>> staff.append(abjad.Measure((2, 8), "af'8 r8"))
                >>> staff.append(abjad.Measure((2, 8), "r8 gf'8"))
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(staff)
                    \new Staff
                    {
                        {   % measure
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }   % measure
                        {   % measure
                            af'8
                            r8
                        }   % measure
                        {   % measure
                            r8
                            gf'8
                        }   % measure
                    }

            ..  container:: example expression

                >>> expression = abjad.Expression()
                >>> expression = expression.select()
                >>> expression = expression.leaves()

                >>> for leaf in expression(staff):
                ...     leaf
                ...
                Chord("<c' bf'>8")
                Chord("<g' a'>8")
                Note("af'8")
                Rest('r8')
                Rest('r8')
                Note("gf'8")

        Returns expression.
        """
        import abjad
        class_ = abjad.Selection
        callback = self._make_initializer_callback(class_, **keywords)
        expression = self.append_callback(callback)
        return abjad.new(
            expression,
            proxy_class=class_,
            template='abjad.select()',
            )

    def sequence(self, **keywords):
        """
        Makes sequence expression.

        ..  container:: example expression

            Makes expression to initialize, flatten and reverse sequence:

            >>> expression = abjad.sequence()
            >>> expression = expression.reverse()
            >>> expression = expression.flatten(depth=-1)

            >>> expression([1, 2, 3, [4, 5, [6]]])
            Sequence([4, 5, 6, 3, 2, 1])

        Returns expression.
        """
        import abjad
        class_ = abjad.Sequence
        callback = self._make_initializer_callback(
            class_,
            string_template='{}',
            **keywords
            )
        expression = self.append_callback(callback)
        return abjad.new(expression, proxy_class=class_)

    def wrap_in_list(self):
        """
        Makes expression to wrap argument in list.

        ..  container:: example expression

            >>> expression = abjad.Expression()
            >>> expression = expression.wrap_in_list()

            >>> expression(abjad.Markup('Allegro assai'))
            [Markup(contents=['Allegro assai'])]

            >>> abjad.f(expression)
            abjad.Expression(
                callbacks=[
                    abjad.Expression(
                        evaluation_template='[{}]',
                        ),
                    ],
                )

        Returns expression.
        """
        callback = self.make_callback(evaluation_template='[{}]')
        return self.append_callback(callback)
