import importlib
import inspect
import itertools
import numbers
import typing

import quicktions
import uqbar.enums

from . import storage
from .new import new


class Expression:
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_argument_values",
        "_callbacks",
        "_evaluation_template",
        "_is_initializer",
        "_keywords",
        "_lone",
        "_map_operand",
        "_module_names",
        "_proxy_class",
        "_qualified_method_name",
        "_subexpressions",
        "_template",
    )

    _private_attributes_to_copy: typing.List[str] = []

    ### INITIALIZER ###

    def __init__(
        self,
        argument_values=None,
        callbacks=None,
        evaluation_template=None,
        is_initializer=None,
        keywords=None,
        lone=None,
        map_operand=None,
        module_names=None,
        proxy_class=None,
        qualified_method_name=None,
        subexpressions=None,
        template=None,
    ):
        if argument_values is not None:
            assert isinstance(argument_values, dict)
            argument_values = argument_values or None
        self._argument_values = argument_values
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks
        if not isinstance(evaluation_template, (str, type(None))):
            message = f"must be string or none: {evaluation_template!r}."
            raise TypeError(message)
        self._evaluation_template = evaluation_template
        self._is_initializer = is_initializer
        if not isinstance(keywords, (dict, type(None))):
            raise TypeError(f"keywords must be dictionary or none: {keywords!r}.")
        self._keywords = keywords
        if not isinstance(map_operand, (Expression, list, type(None))):
            message = f"must be expression, expression list or none: {map_operand!r}."
            raise TypeError(message)
        self._lone = lone
        self._map_operand = map_operand
        self._module_names = module_names
        self._proxy_class = proxy_class
        if qualified_method_name is not None:
            assert isinstance(qualified_method_name, str)
        self._qualified_method_name = qualified_method_name
        if subexpressions is not None:
            subexpressions = tuple(subexpressions)
        self._subexpressions = subexpressions
        self._template = template

    ### SPECIAL METHODS ###

    def __call__(self, *arguments, **keywords):
        """
        Calls expression on ``argument`` with ``keywords``.

        ..  container:: example expression

            Calls identity expression:

            >>> expression = abjad.Expression()

            >>> expression() is None
            True

        Returns ouput of last callback.
        """
        results = []
        for subexpression in self.subexpressions or []:
            result = subexpression(*arguments, **keywords)
            keywords = {}
            results.append(result)
        arguments = results or arguments
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
            assert isinstance(expression, Expression)
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
        """
        return dir(self)

    def __eq__(self, argument) -> bool:
        """
        Is true when expression storage format equals ``argument`` storage format.
        """
        return storage.StorageFormatManager.compare_objects(self, argument)

    def __getattr__(self, name):
        """
        Gets attribute ``name``.

        Returns proxy method when proxy class is set.

        Returns normally when proxy class is not set.
        """
        if self.__getattribute__("_proxy_class") is not None:
            if hasattr(self._proxy_class, name):
                proxy_object = self._proxy_class()
                if not hasattr(proxy_object, name):
                    message = (
                        f"proxy object {proxy_object!r} has no attribute {name!r}."
                    )
                    raise Exception(message)
                if not hasattr(proxy_object, "_expression"):
                    class_name = proxy_object.__name__
                    message = f"does not implement expression protocol: {class_name}."
                    raise Exception(message)
                proxy_object._expression = self
                callable_ = getattr(proxy_object, name)
                assert callable(callable_), repr(callable_)
                if inspect.isfunction(callable_):
                    callable_.__dict__["frozen_expression"] = self
                return callable_
        class_name = type(self).__name__
        raise AttributeError(f"{class_name} object has no attribute {name!r}.")

    def __getitem__(self, argument):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__("__getitem__")
        return proxy_method(argument)

    def __hash__(self) -> int:
        """
        Hashes expression.
        """
        return super().__hash__()

    def __iadd__(self, i):  # type: ignore
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__("__iadd__")
        return proxy_method(i)

    def __radd__(self, i):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__("__radd__")
        return proxy_method(i)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.

        ..  container:: example expression

            Gets interpreter representation of identity expression:

            >>> expression = abjad.Expression()

            >>> expression
            Expression()

        """
        return storage.StorageFormatManager(self).get_repr_format()

    def __setitem__(self, i, argument):
        """
        Gets proxy method.
        """
        proxy_method = self.__getattr__("__setitem__")
        return proxy_method(i, argument)

    def __str__(self) -> str:
        """
        Gets string representation of expression.

        ..  container:: example expression

            Gets string representation of identity expression:

            >>> expression = abjad.Expression()

            >>> str(expression)
            'Expression()'

        """
        return super().__str__()

    ### PRIVATE METHODS ###

    def _evaluate(self, *arguments, **keywords):
        assert self.evaluation_template
        if self.evaluation_template == "map":
            return self._evaluate_map(*arguments)
        if self.evaluation_template == "group_by":
            return self._evaluate_group_by(*arguments)
        globals_ = self._make_globals()
        statement = self.evaluation_template
        strings = []
        if self.is_initializer:
            for i, argument in enumerate(arguments):
                if argument is None:
                    continue
                string = f"__argument_{i}"
                globals_[string] = argument
                strings.append(string)
            keywords_ = self.keywords or {}
            keywords_.update(keywords)
            for key, value in keywords_.items():
                value = Expression._to_evaluable_string(value)
                string = f"{key}={value}"
                strings.append(string)
            strings = ", ".join(strings)
            class_name = self.evaluation_template
            statement = f"{class_name}({strings})"
        else:
            if not arguments:
                statement = statement.replace("{}", "")
            else:
                strings = []
                for i, argument in enumerate(arguments):
                    string = "__argument_" + str(i)
                    globals_[string] = argument
                    strings.append(string)
                try:
                    statement = statement.format(*strings)
                except Exception as exception:
                    arg = exception.args[0]
                    message = f"statement {statement!r} raises {arg!r}."
                    raise type(exception)(message)
        try:
            result = eval(statement, globals_)
        except Exception as exception:
            arg = exception.args[0]
            message = f"evaluable statement {statement!r} raises {arg!r}."
            raise type(exception)(message)
        return result

    def _evaluate_group_by(self, *arguments):
        assert len(arguments) == 1, repr(arguments)
        globals_ = self._make_globals()
        assert "__argument_0" not in globals_
        __argument_0 = arguments[0]
        class_ = type(__argument_0)
        map_operand = self.map_operand
        if map_operand is None:

            def map_operand(argument):
                return True

        globals_["__argument_0"] = __argument_0
        globals_["class_"] = class_
        globals_["map_operand"] = map_operand
        globals_["itertools"] = itertools
        statement = "itertools.groupby(__argument_0, map_operand)"
        try:
            pairs = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            raise Exception(f"{statement!r} raises {e!r}.")
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
        assert "__argument_0" not in globals_
        __argument_0 = arguments[0]
        class_ = type(__argument_0)
        map_operand = self.map_operand
        globals_["__argument_0"] = __argument_0
        globals_["class_"] = class_
        globals_["map_operand"] = map_operand

        def make_items(map_operand, ___argument_0):
            items = []
            for i, item in enumerate(__argument_0):
                item_ = map_operand(item)
                items.append(item_)
            return items

        globals_["make_items"] = make_items
        statement = "make_items(map_operand, __argument_0)"
        try:
            result = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            raise Exception(f"{statement!r} raises {e!r}.")
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
        is_initializer=None,
        keywords=None,
        map_operand=None,
        module_names=None,
    ):
        if evaluation_template is None:
            evaluation_template = class_._get_evaluation_template(frame)
        result = class_._read_signature_decorator(frame)
        argument_values = result["argument_values"]
        qualified_method_name = result["qualified_method_name"]
        return class_(
            argument_values=argument_values,
            evaluation_template=evaluation_template,
            is_initializer=is_initializer,
            keywords=keywords,
            map_operand=map_operand,
            module_names=module_names,
            qualified_method_name=qualified_method_name,
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
                raise ValueError(f"can not find callback {callback_name!r}.")
        return callback

    @staticmethod
    def _get_evaluation_template(frame):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            arguments = Expression._wrap_arguments(frame)
            template = f"{{}}.{function_name}({arguments})"
        finally:
            del frame
        return template

    def _get_format_specification(self):
        if self.template is None:
            return storage.FormatSpecification(client=self)
        return storage.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=[self.template],
            storage_format_forced_override=self.template,
            storage_format_keyword_names=(),
        )

    def _is_singular_get_item(self):
        if not self.callbacks:
            return False
        callback = self.callbacks[-1]
        if getattr(callback, "_lone", None):
            return True
        if callback.evaluation_template == "group_by" and callback.map_operand is None:
            return True
        if not callback.qualified_method_name.endswith("__getitem__"):
            return False
        template = callback.evaluation_template
        if "slice" in template:
            return False
        if "Pattern" in template:
            return False
        if "abjad.index" in template:
            return False
        return True

    @staticmethod
    def _make___getitem___string_template(argument):
        string = Expression._make_subscript_string(argument, markup=False)
        return "{}" + string

    @staticmethod
    def _make_evaluable_keywords(keywords):
        result = {}
        for key, value in keywords.items():
            if isinstance(value, type):
                value = Expression._to_evaluable_string(value)
            result[key] = value
        return result

    def _make_globals(self):
        abjad = importlib.import_module("abjad")
        globals_ = {"abjad": abjad, "quicktions": quicktions}
        globals_.update(abjad.__dict__.copy())
        module_names = self.module_names or []
        if self.qualified_method_name is not None:
            parts = self.qualified_method_name.split(".")
            root_package_name = parts[0]
            module_names.append(root_package_name)
        for module_name in module_names:
            module = __import__(module_name)
            globals_[module_name] = module
        return globals_

    @staticmethod
    def _make_initializer_callback(
        class_,
        *,
        callback_class=None,
        module_names=None,
        **keywords,
    ):
        assert isinstance(class_, type), repr(class_)
        if not hasattr(class_, "_expression"):
            message = f"class does not implement expression protocol: {class_!r}."
            raise TypeError(message)
        parts = class_.__module__.split(".")
        if parts[-1] != class_.__name__:
            parts.append(class_.__name__)
        if "abjad" in parts:
            assert parts[0] == "abjad", repr(parts)
            evaluation_template = f"abjad.{class_.__name__}"
        else:
            evaluation_template = ".".join(parts)
        keywords = Expression._make_evaluable_keywords(keywords)
        keywords = keywords or None
        if callback_class is None:
            callback_class = Expression
        return callback_class(
            evaluation_template=evaluation_template,
            is_initializer=True,
            keywords=keywords,
            module_names=module_names,
        )

    @staticmethod
    def _make_subscript_string(i, markup=False):
        if hasattr(i, "_make_subscript_string"):
            subscript_string = i._make_subscript_string()
            if not markup:
                subscript_string = f"[{subscript_string}]"
            return subscript_string
        if isinstance(i, int):
            if markup:
                subscript_string = "{i}"
            else:
                subscript_string = "[{i}]"
            start = stop = step = None
        elif isinstance(i, slice):
            if i.step is not None:
                raise NotImplementedError
            if i.start is None and i.stop is None:
                subscript_string = "[:]"
            elif i.start is None:
                subscript_string = "[:{stop}]"
            elif i.stop is None:
                subscript_string = "[{start}:]"
            else:
                subscript_string = "[{start}:{stop}]"
            start = i.start
            stop = i.stop
            step = i.step
        else:
            raise TypeError(f"must be integer or slice: {i!r}.")
        subscript_string = subscript_string.format(
            i=i, start=start, stop=stop, step=step
        )
        return subscript_string

    @staticmethod
    def _read_signature_decorator(frame):
        try:
            function_name = inspect.getframeinfo(frame).function
            argument_info = inspect.getargvalues(frame)
            assert argument_info.args[0] == "self"
            function_self = argument_info.locals["self"]
            class_ = function_self.__class__
            parts = class_.__module__.split(".")
            if parts[-1] != class_.__name__:
                parts.append(class_.__name__)
            if "abjad" in parts:
                assert parts[0] == "abjad"
                parts = ["abjad", class_.__name__]
            parts.append(function_name)
            qualified_method_name = ".".join(parts)
            assert "." in qualified_method_name
            argument_values = {}
            return {
                "argument_values": argument_values,
                "qualified_method_name": qualified_method_name,
            }
        finally:
            del frame
        return {
            "argument_values": argument_values,
            "qualified_method_name": qualified_method_name,
        }

    @staticmethod
    def _to_evaluable_string(argument):
        if argument is None:
            pass
        elif isinstance(argument, str):
            argument = repr(argument)
        elif argument.__class__ is quicktions.Fraction:
            argument = f"quicktions.{argument!r}"
        elif isinstance(argument, quicktions.Fraction):
            argument = f"abjad.{argument!r}"
        elif isinstance(argument, numbers.Number):
            argument = str(argument)
        elif isinstance(argument, (list, tuple)):
            item_strings = []
            item_count = len(argument)
            for item in argument:
                item_string = Expression._to_evaluable_string(item)
                item_strings.append(item_string)
            items = ", ".join(item_strings)
            if isinstance(argument, list):
                argument = f"[{items}]"
            elif isinstance(argument, tuple):
                if item_count == 1:
                    items += ","
                argument = f"({items})"
            else:
                raise Exception(repr(argument))
        elif isinstance(argument, slice):
            argument = repr(argument)
        elif isinstance(argument, uqbar.enums.StrictEnumeration):
            argument = f"abjad.{argument!r}"
        # abjad object
        elif not inspect.isclass(argument):
            try:
                argument = storage.storage(argument)
            except (TypeError, ValueError):
                try:
                    argument = storage.StorageFormatManager(
                        argument
                    ).get_storage_format()
                except (TypeError, ValueError):
                    raise Exception(f"can not make storage format: {argument!r}.")
        # abjad class
        elif inspect.isclass(argument) and "abjad" in argument.__module__:
            argument = f"abjad.{argument.__name__}"
        # builtin class [like tuple used in classes=(tuple,)]
        elif inspect.isclass(argument) and "abjad" not in argument.__module__:
            argument = argument.__name__
        else:
            raise Exception(f"can not make evaluable string: {argument!r}.")
        return argument

    @staticmethod
    def _wrap_arguments(frame):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            argument_info = inspect.getargvalues(frame)
            # bound method
            if argument_info.args and argument_info.args[0] == "self":
                self = argument_info.locals["self"]
                function = getattr(self, function_name)
                signature = inspect.signature(function)
                argument_names = argument_info.args[1:]
            # function
            else:
                function = frame.f_globals[function_name]
                signature = inspect.signature(function)
                argument_names = argument_info.args[:]
            argument_strings = []
            for argument_name in argument_names:
                argument_value = argument_info.locals[argument_name]
                parameter = signature.parameters[argument_name]
                # positional argument
                if parameter.default == inspect.Parameter.empty:
                    argument_value = Expression._to_evaluable_string(argument_value)
                    argument_string = argument_value
                    argument_strings.append(argument_string)
                # keyword argument
                elif argument_value != parameter.default:
                    argument_string = "{argument_name}={argument_value}"
                    argument_value = Expression._to_evaluable_string(argument_value)
                    argument_string = argument_string.format(
                        argument_name=argument_name,
                        argument_value=argument_value,
                    )
                    argument_strings.append(argument_string)
            arguments = ", ".join(argument_strings)
        finally:
            del frame
        return arguments

    ### PUBLIC PROPERTIES ###

    @property
    def argument_values(self) -> typing.Optional[typing.Dict]:
        """
        Gets argument values.
        """
        return self._argument_values

    @property
    def callbacks(self) -> typing.Optional[typing.List]:
        """
        Gets callbacks.

        ..  container:: example expression

            Defaults to none:

            >>> expression = abjad.Expression()
            >>> expression.callbacks is None
            True

        """
        if self._callbacks:
            return list(self._callbacks)
        return None

    @property
    def evaluation_template(self) -> typing.Optional[str]:
        """
        Gets evaluation template.
        """
        return self._evaluation_template

    @property
    def is_initializer(self) -> typing.Optional[bool]:
        """
        Is true when expression is initializer.
        """
        return self._is_initializer

    @property
    def keywords(self) -> typing.Dict:
        """
        Gets keywords.
        """
        return self._keywords

    @property
    def lone(self) -> typing.Optional[bool]:
        """
        Is true when expression return a singular get-item.
        """
        return self._lone

    @property
    def map_operand(self) -> typing.Optional["Expression"]:
        """
        Gets expression to map.
        """
        return self._map_operand

    @property
    def module_names(self) -> typing.Optional[typing.List[str]]:
        """
        Gets module names.
        """
        return self._module_names

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
    def qualified_method_name(self) -> typing.Optional[str]:
        """
        Gets qualified method name of expression.
        """
        return self._qualified_method_name

    @property
    def subexpressions(self) -> typing.Optional[typing.List["Expression"]]:
        """
        Gets subexpressions.
        """
        return self._subexpressions

    @property
    def template(self) -> typing.Optional[str]:
        """
        Gets template.
        """
        return self._template

    ### PUBLIC METHODS ###

    def append_callback(self, callback) -> "Expression":
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

        """
        callbacks = self.callbacks or []
        callbacks = callbacks + [callback]
        return new(self, callbacks=callbacks)

    def print(self, argument) -> None:
        """
        Prints ``argument``.
        """
        if self._is_singular_get_item():
            print(repr(argument))
        else:
            for item in argument:
                print(repr(item))
