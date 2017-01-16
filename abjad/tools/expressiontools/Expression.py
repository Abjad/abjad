# -*- coding: utf-8 -*-
import inspect
import numbers
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    r'''Expression.

    ..  container:: example expression

        Makes identity expression:

        ::

            >>> expression = Expression()

        ::

            >>> expression() is None
            True

        ::

            >>> expression(99)
            99

        ::

            >>> expression(99, 99.25)
            (99, 99.25)

    ..  container:: example expression

        Makes integer initialization expression:

        ::

            >>> expression = Expression(evaluation_template='int({})')

        ::

            >>> expression()
            0

        ::

            >>> expression(99)
            99

        ::

            >>> expression(99.25)
            99

    ..  container:: example expression

        Makes binary integer initialization expression:

        ::

            >>> expression = Expression(evaluation_template='int({}, base=2)')

        ::

            >>> expression('1')
            1

        ::

            >>> expression('11')
            3

        ::

            >>> expression('111')
            7

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        '_evaluation_template',
        '_force_return',
        '_formula_markup_expression',
        '_formula_string_template',
        '_is_initializer',
        '_keywords',
        '_map_operand',
        '_module_names',
        '_orientation',
        '_precedence',
        '_proxy_class',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        callbacks=None,
        evaluation_template=None,
        force_return=None,
        formula_markup_expression=None,
        formula_string_template=None,
        is_initializer=None,
        keywords=None,
        map_operand=None,
        module_names=None,
        orientation=None,
        precedence=None,
        ):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks
        if not isinstance(evaluation_template, (str, type(None))):
            message = 'must be string or none: {!r}.'
            message = message.format(evaluation_template)
            raise TypeError(message)
        self._evaluation_template = evaluation_template
        self._force_return = force_return
        if not isinstance(formula_markup_expression, (type(self), type(None))):
            message = 'must be expression or none: {!r}.'
            message = message.format(formula_markup_expression)
            raise TypeError(message)
        self._formula_markup_expression = formula_markup_expression
        if not isinstance(formula_string_template, (str, type(None))):
            message = 'must be string or none: {!r}.'
            message = message.format(formula_string_template)
            raise TypeError(message)
        self._formula_string_template = formula_string_template
        if not isinstance(map_operand, (type(self), type(None))):
            message = 'must be expression or none: {!r}.'
            message = message.format(map_operand)
            raise TypeError(message)
        if not isinstance(keywords, (dict, type(None))):
            message = 'keywords must be dictionary or none: {!r}.'
            message = message.format(keywords)
            raise TypeError(message)
        self._keywords = keywords
        self._is_initializer = is_initializer
        self._map_operand = map_operand
        self._module_names = module_names
        self._orientation = orientation
        self._precedence = precedence
        self._proxy_class = None

    ### SPECIAL METHODS ###

    def __add__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__add__')
        return proxy_method(i)

    def __call__(self, *arguments, **keywords):
        r'''Calls expression on `arguments` with `keywords`.

        ..  container:: example expression

            Calls identity expression:

            ::

                >>> expression = Expression()

            ::

                >>> expression() is None
                True

        ..  container:: example expression

            Calls markup expression:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()

            ::

                >>> expression('Allegro assai')
                Markup(contents=[MarkupCommand('bold', 'Allegro assai')])

        Returns ouput of last callback.
        '''
        from abjad.tools import sequencetools
        if self.evaluation_template is not None:
            assert len(arguments) in [0, 1], repr(arguments)
            result = self._evaluate(*arguments, **keywords)
            keywords = {}
        elif not arguments:
            result = None
        elif len(arguments) == 1:
            result = arguments[0]
        else:
            result = arguments
        for expression in self.callbacks or []:
            result = expression._evaluate(result, **keywords)
        return result

    def __format__(self, format_specification=''):
        r'''Formats expression.

        ..  container:: example expression

            Formats identity expression:

            ::

                >>> expression = Expression()

            ::

                >>> f(expression)
                expressiontools.Expression()

        ..  container:: example expression

            Formats markup expression:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()

            ::

                >>> f(expression)
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Expression(
                            evaluation_template='abjad.markuptools.Markup',
                            is_initializer=True,
                            ),
                        expressiontools.Expression(
                            evaluation_template='{}.bold()',
                            ),
                        ),
                    )

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__format__(
            format_specification=format_specification,
            )

    def __getattr__(self, name):
        r'''Gets attribute `name`.

        Returns proxy method when proxy class is set.

        Returns normally when proxy class is not set.
        '''
        if self.__getattribute__('_proxy_class') is not None:
            if hasattr(self._proxy_class, name):
                proxy_object = self._proxy_class()
                assert hasattr(proxy_object, name)
                if not hasattr(proxy_object, '_frozen_expression'):
                    class_name = proxy_object.__name__
                    message = 'does not implement expression protocol: {}.'
                    message = message.format(class_name)
                    raise Exception(message)
                proxy_object._frozen_expression = self
                callable_ = getattr(proxy_object, name)
                assert callable(callable_), repr(callable_)
                if inspect.isfunction(callable_):
                    callable_.__dict__['frozen_expression'] = self
                return callable_
        message = '{} object has no attribute {!r}.'
        message = message.format(type(self).__name__, name)
        raise AttributeError(message)

    def __getitem__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__getitem__')
        return proxy_method(i)

    def __iadd__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__iadd__')
        return proxy_method(i)

    def __radd__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__radd__')
        return proxy_method(i)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example expression

            Gets interpreter representation of identity expression:

            ::

                >>> expression = Expression()

            ::

                >>> expression
                Expression()

        ..  container:: example expression

            Gets interpreter representation of markup expression:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()

            ::

                >>> expression
                Expression(callbacks=(Expression(evaluation_template='abjad.markuptools.Markup', is_initializer=True), Expression(evaluation_template='{}.bold()')))

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__repr__()

    def __setitem__(self, i, argument):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__setitem__')
        return proxy_method(i, argument)

    def __str__(self):
        r'''Gets string representation of expression.

        ..  container:: example expression

            Gets string representation of identity expression:

            ::

                >>> expression = Expression()

            ::

                >>> str(expression)
                'Expression()'

        ..  container:: example expression

            Gets string representation of markup expression:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()

            ::

                >>> str(expression)
                "Expression(callbacks=(Expression(evaluation_template='abjad.markuptools.Markup', is_initializer=True), Expression(evaluation_template='{}.bold()')))"

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__str__()

    ### PRIVATE METHODS ###

    def _evaluate(self, *arguments, **keywords):
        import abjad
        assert self.evaluation_template
        assert len(arguments) in [0, 1], repr(arguments)
        if self.evaluation_template == 'map':
            return self._evaluate_map(*arguments)
        globals_ = self._make_globals()
        statement = self.evaluation_template
        assert len(arguments) <= 1, repr(arguments)
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
                assert len(arguments) == 1, repr(arguments)
                __the_argument = arguments[0]
                globals_['__the_argument'] = __the_argument
                statement = statement.format('__the_argument')
        try:
            result = eval(statement, globals_)
        except Exception as exception:
            message = 'evaluable statement {!r} raises {!r}.'
            message = message.format(statement, exception.args[0])
            raise type(exception)(message)
        if self.force_return:
            result = __the_argument
        return result

    def _evaluate_map(self, *arguments):
        assert len(arguments) == 1, repr(arguments)
        assert self.map_operand is not None
        globals_ = self._make_globals()
        assert '__the_argument' not in globals_
        __the_argument = arguments[0]
        class_ = type(__the_argument)
        map_operand = self.map_operand
        globals_['__the_argument'] = __the_argument
        globals_['class_'] = class_
        globals_['map_operand'] = map_operand
        statement = 'class_([map_operand(_) for _ in __the_argument])'
        try:
            result = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            message = '{!r} raises {!r}.'
            message = message.format(statement, e)
            raise Exception(message)
        return result

    @staticmethod
    def _get_expression_markup(argument, direction=None, name=None):
        import abjad
        if name is None:
            name = getattr(argument, '_name_markup', None)
        if name is None:
            name = getattr(argument, '_name', None)
        if getattr(argument, '_equivalence_markup', None) is not None:
            return abjad.new(argument._equivalence_markup, direction=direction)
        elif getattr(argument, '_expression', None) is not None:
            return argument._expression.get_formula_markup(
                direction=direction,
                name=name,
                )
        elif name is not None:
            return abjad.Markup(contents=name, direction=direction).bold()

    def _initialize(
        self,
        class_,
        formula_string_template=None,
        module_names=None,
        **keywords
        ):
        assert isinstance(class_, type), repr(class_)
        if not hasattr(class_, '_frozen_expression'):
            message = 'does not implement expression protocol: {!r}.'
            message = message.format(class_)
            raise TypeError(class_)
        template = class_.__module__.split('.')
        if 'abjad' in template:
            template = [_ for _ in template if _ != 'tools']
        template = '.'.join(template)
        keywords = self._make_evaluable_keywords(keywords)
        keywords = keywords or None
        callback = type(self)(
            evaluation_template=template,
            formula_string_template=formula_string_template,
            is_initializer=True,
            keywords=keywords,
            module_names=module_names,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = class_
        return result

    def _make_evaluable_keywords(self, keywords):
        result = {}
        for key, value in keywords.items():
            if isinstance(value, type):
                value = self._to_evaluable_string(value)
            result[key] = value
        return result
        
    @staticmethod
    def _make_evaluation_template(frame, static_class=None):
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
        
    def _make_globals(self):
        import abjad
        globals_ = {'abjad': abjad}
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

    def _make_parentheses(self):
        formula_markup_expression = type(self)()
        formula_markup_expression = formula_markup_expression.append_callback(
            'Markup({}).parenthesize()',
            )
        return formula_markup_expression

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
                argument = '[{}]'.format(items)
            elif isinstance(argument, tuple):
                if item_count == 1:
                    items += ','
                argument = '({})'.format(items)
            else:
                raise Exception(repr(argument))
        # abjad object
        elif not inspect.isclass(argument):
            try:
                argument = format(argument, 'storage')
            except (TypeError, ValueError):
                message = 'can not make storage format: {!r}.'
                message = message.format(argument)
                raise Exception(message)
        # abjad class
        elif inspect.isclass(argument) and 'abjad' in argument.__module__:
            argument = argument.__module__.split('.')
            argument = argument[-2:]
            argument = '.'.join(argument)
        # builtin class like tuple in classes=(tuple,)
        elif inspect.isclass(argument) and 'abjad' not in argument.__module__:
            argument = argument.__name__
        else:
            message = 'can not make evaluable string: {!r}.'
            message = message.format(argument)
            raise Exception(message)
        return argument

    @staticmethod
    def _track_expression(
        source_object,
        target_object,
        method_name,
        formula_markup_expression=None,
        formula_string_template=None,
        module_names=None,
        orientation=None,
        precedence=None,
        ):
        if source_object._name is None:
            return
        evaluation_template = '{}.{}'.format(
            type(source_object).__name__,
            method_name,
            )
        expression = source_object._expression or Expression()
        expression = expression.append_callback(
            evaluation_template=evaluation_template,
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            module_names=module_names,
            orientation=orientation,
            precedence=precedence,
            )
        target_object._expression = expression

    @staticmethod
    def _wrap_arguments(frame, static_class=None):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            values = inspect.getargvalues(frame)
            if static_class:
                method_name = frame.f_code.co_name
                static_method = getattr(static_class, method_name)
                signature = inspect.signature(static_method)
                argument_names = values.args[:]
            else:
                assert values.args[0] == 'self'
                self = values.locals['self']
                function = getattr(self, function_name)
                signature = inspect.signature(function)
                argument_names = values.args[1:]
            argument_strings = []
            for argument_name in argument_names:
                argument_value = values.locals[argument_name]
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
        finally:
            del frame
        return arguments

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks.

        ..  container:: example expression

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()
                >>> for callback in expression.callbacks:
                ...     callback
                Expression(evaluation_template='abjad.markuptools.Markup', is_initializer=True)
                Expression(evaluation_template='{}.bold()')

        ..  container:: example expression

            Defaults to none:

            ::

                >>> expression = Expression()
                >>> expression.callbacks is None
                True

        Set to callbacks or none.

        ..  container:: example expression

            Returns tuple or none:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()
                >>> isinstance(expression.callbacks, tuple)
                True

        '''
        return self._callbacks

    @property
    def evaluation_template(self):
        r'''Gets evaluation template.

        Defaults to none.

        Set to string.

        Returns string.
        '''
        return self._evaluation_template

    @property
    def force_return(self):
        r'''Is true when expression should return primary input argument.
        Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._force_return

    @property
    def formula_markup_expression(self):
        r'''Gets formula markup expression.

        Defaults to none.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._formula_markup_expression

    @property
    def formula_string_template(self):
        r'''Gets formula string template.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._formula_string_template

    @property
    def is_initializer(self):
        r'''Is true when expression is initializer. Otherwise false.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._is_initializer

    @property
    def keywords(self):
        r'''Gets keywords.

        Defaults to none.

        Set to dictionary or none.

        Returns dictionary or none.
        '''
        return self._keywords

    @property
    def map_operand(self):
        r'''Gets expression to map.

        Defaults to none.

        Set to expression or none.

        Returns expression or none.
        '''
        return self._map_operand

    @property
    def module_names(self):
        r'''Gets module names.

        Defaults to none.

        Set to strings or none.

        Returns strings or none.
        '''
        return self._module_names

    @property
    def orientation(self):
        r'''Gets orientation.

        Defaults to none.

        Set to orientation or none.

        Returns dictionary or none.
        '''
        return self._orientation

    @property
    def precedence(self):
        r'''Gets precedence.

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._precedence

    ### PUBLIC METHODS ###

    def append_callback(
        self,
        evaluation_template,
        force_return=None,
        formula_markup_expression=None,
        formula_string_template=None,
        map_operand=None,
        module_names=None,
        orientation=None,
        precedence=None,
        ):
        r'''Appends callback.

        ..  container:: example expression

            ::

                >>> expression = Expression()
                >>> expression.callbacks is None
                True

            ::

                
                >>> expression = expression.append_callback('int({})')
                >>> for callback in expression.callbacks:
                ...     callback
                Expression(evaluation_template='int({})')

            ::

                >>> expression = expression.append_callback('{}**2')
                >>> for expression in expression.callbacks:
                ...     expression
                Expression(evaluation_template='int({})')
                Expression(evaluation_template='{}**2')

        Returns new expression.
        '''
        import abjad
        callback = type(self)(
            evaluation_template=evaluation_template,
            force_return=force_return,
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            map_operand=map_operand,
            module_names=module_names,
            orientation=orientation,
            precedence=precedence,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = self._proxy_class
        return result

    @staticmethod
    def establish_equivalence(argument, name):
        r'''Makes new object with `name` and equivalence markup.

        ..  container:: example expression

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> items = ['c', 'ef', 'bqs,', 'd']
                >>> K = pitchtools.PitchClassSegment(items=items, name='K')

            ::

                >>> segment = J.rotate(n=1) + K.rotate(n=2)
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], name='r1(J) + r2(K)')

            ::

                >>> segment = Expression.establish_equivalence(segment, 'Q')
                >>> segment
                PitchClassSegment([7, 10, 10.5, 6, 7, 10.5, 11.5, 2, 0, 3], name='Q')

            ::

                >>> show(segment) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segment.__illustrate__()
                >>> f(lilypond_file[Voice])
                \new Voice {
                    g'8
                        ^ \markup {
                            \line
                                {
                                    \bold
                                        Q
                                    =
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                1
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        J
                                                }
                                        }
                                    +
                                    \concat
                                        {
                                            r
                                            \hspace
                                                #-0.2
                                            \sub
                                                2
                                            \concat
                                                {
                                                    \hspace
                                                        #0.4
                                                    \bold
                                                        K
                                                }
                                        }
                                }
                            }
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    bqs'8
                    d'8
                    c'8
                    ef'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        Returns new object with type equal to that of `argument`.
        '''
        import abjad
        result = abjad.new(argument, name=name)
        lhs_markup = abjad.Markup(name).bold()
        rhs_markup = Expression._get_expression_markup(argument)
        equivalence_markup = lhs_markup + abjad.Markup('=') + rhs_markup
        equivalence_markup = abjad.Markup.line([equivalence_markup])
        result._equivalence_markup = equivalence_markup
        return result

    def get_formula_markup(self, name, direction=None):
        r'''Gets formula markup.

        ..  container:: example expression

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.invert()
                >>> markup = segment._expression.get_formula_markup(name='J')
                >>> show(markup) # doctest: +SKIP
                
            ..  doctest::

                >>> f(markup)
                \markup {
                    \concat
                        {
                            I
                            \concat
                                {
                                    \hspace
                                        #0.4
                                    \bold
                                        J
                                }
                        }
                    }

        ..  container:: example expression

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.invert()
                >>> segment = segment.rotate(n=2)
                >>> markup = segment._expression.get_formula_markup(name='J')
                >>> show(markup) # doctest: +SKIP
                
            ..  doctest::

                >>> f(markup)
                \markup {
                    \concat
                        {
                            r
                            \hspace
                                #-0.2
                            \sub
                                2
                            \concat
                                {
                                    I
                                    \concat
                                        {
                                            \hspace
                                                #0.4
                                            \bold
                                                J
                                        }
                                }
                        }
                    }

        Returns markup or none.
        '''
        import abjad
        # TODO: probably now even length-1 expressions can get markup; check
        if not self.callbacks:
            return
        markup = abjad.Markup(name).bold()
        callback = self.callbacks[0]
        if callback.orientation in (Left, None):
            markup = [abjad.Markup.hspace(0.4), markup]
            markup = abjad.Markup.concat(markup)
        markup = callback.formula_markup_expression(markup)
        previous_precedence = callback.precedence or 0
        for callback in self.callbacks[1:]:
            current_precedence = callback.precedence or 0
            parenthesize_argument = False
            if previous_precedence < current_precedence:
                expression = self._make_parentheses()
                markup = expression(markup)
            markup = callback.formula_markup_expression(markup)
        markup = abjad.new(markup, direction=direction)
        return markup

    def get_formula_string(self, name):
        r'''Gets formula string.

        ..  container:: example expression

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.invert()
                >>> segment._expression.get_formula_string(name='J')
                'I(J)'
                
        ..  container:: example expression

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.invert()
                >>> segment = segment.rotate(n=2)
                >>> segment._expression.get_formula_string(name='J')
                'r2(I(J))'
                
        Returns string or none.
        '''
        import abjad
        if not self.callbacks:
            return
        callback = self.callbacks[0]
        try:
            string = callback.formula_string_template.format(name)
        except (AttributeError, IndexError, KeyError) as e:
            message = '{!r} with template {!r} and name {!r} raises {!r}.'
            message = message.format(
                callback,
                callback.formula_string_template,
                name,
                e,
                )
            raise Exception(message)
        for callback in self.callbacks[1:]:
            try:
                string = callback.formula_string_template.format(string)
            except (AttributeError, IndexError, KeyError) as e:
                message = '{!r} with template {!r} and name {!r} raises {!r}.'
                message = message.format(
                    callback,
                    callback.formula_string_template,
                    string,
                    e,
                    )
                raise Exception(message)
        return string

    def iterate(self, **keywords):
        r'''Makes iterate expression and sets proxy.

        ..  container:: example

            Makes expression to iterate leaves:

            ..  container:: example

                ::

                    >>> staff = Staff()
                    >>> staff.append(Measure((2, 8), "<c' bf'>8 <g' a'>8"))
                    >>> staff.append(Measure((2, 8), "af'8 r8"))
                    >>> staff.append(Measure((2, 8), "r8 gf'8"))
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff {
                        {
                            \time 2/8
                            <c' bf'>8
                            <g' a'>8
                        }
                        {
                            af'8
                            r8
                        }
                        {
                            r8
                            gf'8
                        }
                    }

            ..  container:: example expression

                ::

                    >>> expression = Expression()
                    >>> expression = expression.iterate()
                    >>> expression = expression.by_leaf()
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
        '''
        import abjad
        return self._initialize(abjad.agenttools.IterationAgent, **keywords)

    def label(self, **keywords):
        r'''Makes label expression and sets proxy.

        ..  container:: example

            Makes expression to label logical tie durations:

            ..  container:: example

                ::

                    >>> staff = Staff(r"c'4. d'8 ~ d'4. e'16 [ ef'16 ]")

            ..  container:: example expression

                    >>> expression = Expression()
                    >>> expression = expression.label()
                    >>> expression = expression.with_durations()
                    >>> expression(staff)
                    >>> show(staff) # doctest: +SKIP

                ..  doctest::

                    >>> f(staff)
                    \new Staff {
                        c'4.
                            ^ \markup {
                                \small
                                    3/8
                                }
                        d'8 ~
                            ^ \markup {
                                \small
                                    1/2
                                }
                        d'4.
                        e'16 [
                            ^ \markup {
                                \small
                                    1/16
                                }
                        ef'16 ]
                            ^ \markup {
                                \small
                                    1/16
                                }
                    }

        Returns expression.
        '''
        import abjad
        return self._initialize(abjad.agenttools.LabelAgent, **keywords)

    def markup(self, **keywords):
        r'''Makes markup expression and sets proxy.

        ..  container:: example expression

            Makes expression to make bold markup:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup()
                >>> expression = expression.bold()
                >>> markup = expression('Allegro assai')
                >>> f(markup)
                \markup {
                    \bold
                        "Allegro assai"
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns expression.
        '''
        import abjad
        return self._initialize(abjad.Markup, **keywords)

    def markup_list(self, **keywords):
        r'''Makes markup list expression and sets proxy.

        ..  container:: example expression

            Makes expression to concatenate markups in markup list:

            ::

                >>> expression = Expression()
                >>> expression = expression.markup_list()
                >>> expression = expression.concat(direction=Up)
                >>> downbow = Markup.musicglyph('scripts.downbow')
                >>> hspace = Markup.hspace(1)
                >>> upbow = Markup.musicglyph('scripts.upbow')
                >>> markups = [downbow, hspace, upbow]
                >>> markup = expression(markups)
                >>> f(markup)
                ^ \markup {
                    \concat
                        {
                            \musicglyph
                                #"scripts.downbow"
                            \hspace
                                #1
                            \musicglyph
                                #"scripts.upbow"
                        }
                    }

            ::

                >>> show(markup) # doctest: +SKIP

        Returns expression.
        '''
        import abjad
        return self._initialize(abjad.MarkupList, **keywords)

    def pitch_class_segment(self, **keywords):
        r'''Makes pitch-class segment expression and sets proxy.

        ..  container:: example

            Makes expression to transpose pitch-class segment:

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> J = pitchtools.PitchClassSegment(items=items, name='J')
                >>> J
                PitchClassSegment([10, 10.5, 6, 7, 10.5, 7], name='J')

            ::

                >>> show(J) # doctest: +SKIP

            ..  container:: example expression

                ::

                    >>> expression = Expression()
                    >>> expression = expression.pitch_class_segment(name='J')
                    >>> expression = expression.transpose(n=13)
                    >>> segment = expression([-2, -1.5, 6, 7, -1.5, 7])
                    >>> segment
                    PitchClassSegment([11, 11.5, 7, 8, 11.5, 8], name='T13(J)')

                ::

                    >>> show(segment) # doctest: +SKIP

                ..  doctest::

                    >>> lilypond_file = segment.__illustrate__()
                    >>> f(lilypond_file[Voice])
                    \new Voice {
                        b'8
                            ^ \markup {
                                \concat
                                    {
                                        T
                                        \hspace
                                            #-0.2
                                        \sub
                                            13
                                        \concat
                                            {
                                                \hspace
                                                    #0.4
                                                \bold
                                                    J
                                            }
                                    }
                                }
                        bqs'8
                        g'8
                        af'8
                        bqs'8
                        af'8
                        \bar "|."
                        \override Score.BarLine.transparent = ##f
                    }

        Returns expression.
        '''
        import abjad
        return self._initialize(
            abjad.PitchClassSegment,
            formula_string_template='pcs({})',
            **keywords
            )

    def sequence(self, **keywords):
        r'''Makes sequence expression and sets proxy.

        ..  container:: example expression

            Makes expression to initialize, flatten and reverse sequence:

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.flatten()
                >>> expression([1, 2, 3, [4, 5, [6]]])
                Sequence([4, 5, 6, 3, 2, 1])

        Returns expression.
        '''
        import abjad
        return self._initialize(
            abjad.Sequence,
            formula_string_template='{}',
            **keywords
            )

    def wrap_in_list(self):
        r'''Makes expression to wrap argument in list.

        ..  container:: example expression

            ::

                >>> expression = Expression()
                >>> expression = expression.wrap_in_list()
                >>> f(expression)
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Expression(
                            evaluation_template='[{}]',
                            ),
                        ),
                    )

            ::

                >>> expression(Markup('Allegro assai'))
                [Markup(contents=['Allegro assai'])]

        Returns expression.
        '''
        return self.append_callback(evaluation_template='[{}]')
