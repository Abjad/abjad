# -*- coding: utf-8 -*-
import functools
import inspect
from abjad.tools.abctools import AbjadObject


class Callback(AbjadObject):
    r'''Callback.

    ..  container:: example

        Built-in callback:

        ::

            >>> callback = expressiontools.Callback('int({})')

        ::

            >>> callback(99.25)
            99

    ..  container:: example

        Class callback:

        ::

            >>> callback = expressiontools.Callback('Sequence({})')

        ::

            >>> callback([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Function callback without arguments:

        ::

            >>> callback = expressiontools.Callback(
            ...     'sequencetools.flatten_sequence({})',
            ...     )

        ::

            >>> callback([1, 2, [3, [4]], 5])
            [1, 2, 3, 4, 5]

    ..  container:: example

        Function callback with arguments:

        ::

            >>> template = 'sequencetools.flatten_sequence({}, depth=1)'
            >>> callback = expressiontools.Callback(template)

        ::

            >>> callback([1, 2, [3, [4]], 5])
            [1, 2, 3, [4], 5]

    ..  container:: example

        Single-item list callback:

        ::

            >>> callback = expressiontools.Callback('[{}]')

        ::

            >>> callback(99)
            [99]

        ::

            >>> callback('text')
            ['text']

        ::

            >>> callback(Markup('text').italic())
            [Markup(contents=(MarkupCommand('italic', 'text'),))]

    Initializer returns callback.

    Call returns object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_arguments',
        '_direction',
        '_markup_expression',
        '_module_names',
        '_precedence',
        '_template',
        '_string_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        template=None,
        arguments=None,
        direction=None,
        markup_expression=None,
        module_names=None,
        precedence=None,
        string_expression=None,
        ):
        from abjad.tools import datastructuretools
        from abjad.tools import expressiontools
        if template is not None:
            assert isinstance(template, str), repr(template)
        self._template = template
        if arguments is not None:
            arguments = dict(arguments)
            arguments = list(sorted(arguments.items()))
            datastructuretools.TypedOrderedDict(arguments)
        self._arguments = arguments
        self._direction = direction
        prototype = (expressiontools.Expression, type(None))
        if not isinstance(markup_expression, prototype):
            message = 'must be expression or none: {!r}.'
            message = message.format(markup_expression)
            raise TypeError(message)
        self._markup_expression = markup_expression
        self._module_names = module_names
        self._precedence = precedence
        self._string_expression = string_expression

    ### SPECIAL METHODS ###

    def __call__(self, *args, **kwargs):
        r'''Calls callback on `args` and `kwargs`.

        ..  container:: example

            ::

                >>> callback = expressiontools.Callback('Sequence({})')
                >>> callback([1, 2, 3])
                Sequence([1, 2, 3])

        Returns object.
        '''
        globals_ = self._make_globals()
        is_template = '{' in self.template and '}' in self.template
        if is_template:
            qualified_args = []
            for arg in args:
                qualified_arg = self._make_qualified_string(arg)
                qualified_args.append(qualified_arg)
            try:
                statement = self.template.format(*qualified_args, **kwargs)
            except ValueError as e:
                message = '{!r} with {!r} raises {!r}.'
                message = message.format(
                    self.template,
                    qualified_args,
                    e,
                    )
                raise Exception(message)
            try:
                result = eval(statement, globals_)
            except (NameError, SyntaxError, TypeError) as e:
                message = '{!r} raises {!r}.'
                message = message.format(statement, e)
                raise Exception(message)
        else:
            arguments = []
            if self.arguments:
                for key, value in self.arguments:
                    if (inspect.isclass(value) and
                        not value.__name__ in globals_):
                        globals_[value.__name__] = value
                    if '<' in repr(value) and '>' in repr(value):
                        value = value.__name__
                    else:
                        value = repr(value)
                    argument = '{}={}'
                    argument = argument.format(key, value)
                    arguments.append(argument)
            arguments = ', '.join(arguments)
            template = self.template
            statement = 'functools.partial({}, {})'
            statement = statement.format(template, arguments)
            partial = eval(statement, globals_)
            try:
                result = partial(*args, **kwargs)
            except TypeError as e:
                message = '{!r} raises {!r}.'
                message = message.format(partial, e)
                raise Exception(message)
        return result

    def __str__(self):
        r'''Gets string representation of callback.

        ..  container:: example

            ::

                >>> str(expressiontools.Callback('Sequence({})'))
                "Callback('Sequence({})')"

        Returns string.
        '''
        if self.string_expression is not None:
            string = self.string_expression
            arguments = self.arguments or []
            values = [_[-1] for _ in arguments]
            string = string.format(*values)
            return string
        return repr(self)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=[self.template],
            )

    def _make_globals(self):
        import abjad
        globals_ = {
            'abjad': abjad,
            'functools': functools,
            }
        globals_.update(abjad.__dict__.copy())
        module_names = self.module_names or ()
        for module_name in module_names:
            module = __import__(module_name)
            globals_[module_name] = module
        try:
            import experimental
            globals_.update(experimental.__dict__.copy())
        except ImportError:
            pass
        return globals_

    def _make_qualified_string(self, expr):
        try:
            qualified_string = format(expr, 'storage')
        except (TypeError, ValueError):
            qualified_string = repr(expr)
        return qualified_string

    ### PUBLIC PROPERTIES ###

    @property
    def arguments(self):
        r'''Gets arguments of callback.

        Set to dictionary or none.

        Defaults to none.

        Returns dictionary or none.
        '''
        return self._arguments

    @property
    def direction(self):
        r'''Gets direction of callback.

        Defaults to none.

        Set to direction or none.

        Returns dictionary or none.
        '''
        return self._direction

    @property
    def markup_expression(self):
        r'''Gets markup expression of callback.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._markup_expression

    @property
    def module_names(self):
        r'''Gets module names of callback.

        Set to strings or none.

        Defaults to none.

        Returns strings or none.
        '''
        return self._module_names

    @property
    def precedence(self):
        r'''Gets precedence of callback.

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._precedence

    @property
    def template(self):
        r'''Gets template of callback.

        Set to string.

        Returns string.
        '''
        return self._template
        
    @property
    def string_expression(self):
        r'''Gets string template of callback.

        Set to string or none.

        Returns string or none.
        '''
        return self._string_expression
