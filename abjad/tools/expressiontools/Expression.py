# -*- coding: utf-8 -*-
import inspect
import numbers
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    r'''Expression.

    ..  container:: example

        Identity expression:

        ::

            >>> expression = expressiontools.Expression()

        ::

            >>> expression() is None
            True

        ::

            >>> expression(99)
            99

        ::

            >>> expression(99, 99.25)
            (99, 99.25)

    ..  container:: example

        Integer initialization expression:

        ::

            >>> expression = expressiontools.Expression(
            ...     evaluation_template='int({})',
            ...     )

        ::

            >>> expression()
            0

        ::

            >>> expression(99)
            99

        ::

            >>> expression(99.25)
            99

    ..  container:: example

        Binary integer initialization expression:

        ::

            >>> expression = expressiontools.Expression(
            ...     evaluation_template='int({}, base=2)',
            ...     )

        ::

            >>> expression('1')
            1

        ::

            >>> expression('11')
            3

        ::

            >>> expression('111')
            7

    ..  container:: example

        Single-item list initialization expression:

        ::

            >>> expression = expressiontools.Expression(
            ...     evaluation_template='[{}]',
            ...     )

        ::

            >>> expression()
            []

        ::

            >>> expression('Allegro')
            ['Allegro']

        ::

            >>> expression(Markup('Allegro assai').italic())
            [Markup(contents=(MarkupCommand('italic', 'Allegro assai'),))]

    ..  container:: example

        Sequence initialization expression:

        ::

            >>> expression = expressiontools.Expression(
            ...     evaluation_template='Sequence({})',
            ...     )

        ::

            >>> expression()
            Sequence([])

        ::

            >>> expression('Allegro')
            Sequence(['A', 'l', 'l', 'e', 'g', 'r', 'o'])

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Flatten-sequence expression:

        ::

            >>> template = 'sequencetools.flatten_sequence({})'
            >>> expression = expressiontools.Expression(
            ...     evaluation_template=template,
            ...     )

        ::

            >>> expression([])
            []

        ::

            >>> expression([1, 2, 3, 4, 5])
            [1, 2, 3, 4, 5]

        ::

            >>> expression([1, 2, [3, [4]], 5])
            [1, 2, 3, 4, 5]

    ..  container:: example

        Restricted flatten-sequence expression:

        ::

            >>> template = 'sequencetools.flatten_sequence({}, depth=1)'
            >>> expression = expressiontools.Expression(
            ...     evaluation_template=template,
            ...     )

        ::

            >>> expression([])
            []

        ::

            >>> expression([1, 2, 3, 4, 5])
            [1, 2, 3, 4, 5]

        ::

            >>> expression([1, 2, [3, [4]], 5])
            [1, 2, 3, [4], 5]

    ..  container:: example

        Markup expression:

        ::

            >>> expression = expressiontools.Expression()
            >>> expression = expression.append_callback('Markup({})')
            >>> expression = expression.append_callback('{}.italic()')

        ::

            >>> expression('Allego')
            Markup(contents=(MarkupCommand('italic', 'Allego'),))

        ::

            >>> expression('Allegro assai')
            Markup(contents=(MarkupCommand('italic', 'Allegro assai'),))

        ::

            >>> expression('Allegro assai ma non troppo')
            Markup(contents=(MarkupCommand('italic', 'Allegro assai ma non troppo'),))

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        '_evaluation_template',
        '_formula_markup_expression',
        '_formula_string_template',
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
        formula_markup_expression=None,
        formula_string_template=None,
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

    def __call__(self, *arguments):
        r'''Calls expression on `arguments`.

        ..  container:: example

            Calls identity expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> expression() is None
                True

        ..  container:: example

            Calls markup expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')

            ::

                >>> expression('text')
                Markup(contents=(MarkupCommand('italic', 'text'),))

        Returns ouput of last callback.
        '''
        from abjad.tools import sequencetools
        if self.evaluation_template is not None:
            assert len(arguments) in [0, 1], repr(arguments)
            result = self._evaluate(*arguments)
        elif not arguments:
            result = None
        elif len(arguments) == 1:
            result = arguments[0]
        else:
            result = arguments
        for expression in self.callbacks or []:
            result = expression._evaluate(result)
        if not getattr(self, '_in_place', None):
            return result

    def __format__(self, format_specification=''):
        r'''Formats expression.

        ..  container:: example

            Formats identity expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> f(expression)
                expressiontools.Expression()

        ..  container:: example

            Formats markup expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')

            ::

                >>> f(expression)
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Expression(
                            evaluation_template='Markup({})',
                            ),
                        expressiontools.Expression(
                            evaluation_template='{}.italic()',
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
        r'''Gets attribute with `name`.

        Returns proxy method when proxy class is set.

        Returns normally when proxy class is not set.
        '''
        #if (self.__getattribute__('_proxy_class') is not None and
        #    not name.startswith('_')):
        if self.__getattribute__('_proxy_class') is not None:
            if hasattr(self._proxy_class, name):
                proxy_object = self._proxy_class()
                assert hasattr(proxy_object, name)
                if not hasattr(proxy_object, '_is_frozen'):
                    message = 'does not implement expression protocol: {}.'
                    message = message.format(type(proxy_object).__name__)
                    raise Exception(message)
                proxy_object._is_frozen = self
                frozen_method = getattr(proxy_object, name)
                return frozen_method
        message = '{!r} object has no attribute {!r}.'
        message = message.format(type(self).__name__, name)
        raise AttributeError(message)

    def __getitem__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__getitem__')
        return proxy_method(i)

    def __radd__(self, i):
        r'''Gets proxy method.
        '''
        proxy_method = self.__getattr__('__radd__')
        return proxy_method(i)

    def __repr__(self):
        r'''Gets interpreter representation.

        ..  container:: example

            Gets interpreter representation of identity expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> expression
                Expression()

        ..  container:: example

            Gets interpreter representation of markup expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')

            ::

                >>> expression
                Expression(callbacks=(Expression(evaluation_template='Markup({})'), Expression(evaluation_template='{}.italic()')))

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__repr__()

    def __str__(self):
        r'''Gets string representation.

        ..  container:: example

            Gets string representation of identity expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> str(expression)
                'Expression()'

        ..  container:: example

            Gets string representation of markup expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')

            ::

                >>> str(expression)
                "Expression(callbacks=(Expression(evaluation_template='Markup({})'), Expression(evaluation_template='{}.italic()')))"

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__str__()

    ### PRIVATE METHODS ###

    def _evaluate(self, *arguments):
        assert self.evaluation_template
        assert len(arguments) in [0, 1], repr(arguments)
        if self.evaluation_template == 'map':
            return self._evaluate_map(*arguments)
        statement = self.evaluation_template
        assert '{}' in statement, repr(statement)
        globals_ = self._make_globals()
        if not arguments:
            statement = statement.replace('{}', '')
        else:
            __the_argument = arguments[0]
            globals_['__the_argument'] = __the_argument
            statement = statement.format('__the_argument')
        try:
            result = eval(statement, globals_)
        except Exception as exception:
            message = 'evaluable statement {!r} raises {!r}.'
            message = message.format(statement, exception.args[0])
            raise type(exception)(message)
        if getattr(self, '_in_place', None):
            result = __the_argument
        return result

    def _evaluate_map(self, *arguments):
        assert not getattr(self, '_in_place', False)
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
    def _get_expression_markup(object_, direction=None, name=None):
        import abjad
        if name is None:
            name = getattr(object_, '_name_markup', None)
        if name is None:
            name = getattr(object_, '_name', None)
        if getattr(object_, '_equivalence_markup', None) is not None:
            return abjad.new(object_._equivalence_markup, direction=direction)
        elif getattr(object_, '_expression', None) is not None:
            return object_._expression.get_formula_markup(
                direction=direction,
                name=name,
                )
        elif name is not None:
            return abjad.Markup(contents=name, direction=direction).bold()

    @staticmethod
    def _make_evaluation_template(frame):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            arguments = Expression._wrap_arguments(frame)
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
    def _wrap_arguments(frame):
        try:
            frame_info = inspect.getframeinfo(frame)
            function_name = frame_info.function
            values = inspect.getargvalues(frame)
            assert values.args[0] == 'self'
            self = values.locals['self']
            function = getattr(self, function_name)
            signature = inspect.signature(function)
            argument_strings = []
            for argument_name in values.args[1:]:
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

        ..  container:: example

            Gets callbacks:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')

            ::

                >>> for callback in expression.callbacks:
                ...     callback
                Expression(evaluation_template='Markup({})')
                Expression(evaluation_template='{}.italic()')

        ..  container:: example

            Defaults to none:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression.callbacks is None
                True

        Set to callbacks or none.

        ..  container:: example

            Returns tuple or none:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.append_callback('Markup({})')
                >>> expression = expression.append_callback('{}.italic()')
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
        orientation=None,
        formula_markup_expression=None,
        formula_string_template=None,
        map_operand=None,
        module_names=None,
        precedence=None,
        ):
        r'''Appends callback.

        ..  container:: example

            Appends callback:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression.callbacks is None
                True

            ::

                
                >>> expression = expression.append_callback('Markup({})')
                >>> for callback in expression.callbacks:
                ...     callback
                Expression(evaluation_template='Markup({})')

            ::

                >>> expression = expression.append_callback('{}.italic()')
                >>> for expression in expression.callbacks:
                ...     expression
                Expression(evaluation_template='Markup({})')
                Expression(evaluation_template='{}.italic()')

        Returns new expression.
        '''
        callback = type(self)(
            evaluation_template=evaluation_template,
            orientation=orientation,
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            map_operand=map_operand,
            module_names=module_names,
            precedence=precedence,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = self._proxy_class
        return result

    @staticmethod
    def establish_equivalence(object_, name):
        r'''Makes new object with `name` and equivalence markup.

        ..  container:: example

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

                >>> segment = expressiontools.Expression.establish_equivalence(segment, 'Q')
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

        Returns new object with type equal to that of `object_`.
        '''
        import abjad
        result = abjad.new(object_, name=name)
        lhs_markup = abjad.Markup(name).bold()
        rhs_markup = Expression._get_expression_markup(object_)
        equivalence_markup = lhs_markup + abjad.Markup('=') + rhs_markup
        equivalence_markup = equivalence_markup.line()
        result._equivalence_markup = equivalence_markup
        return result

    def get_formula_markup(self, name, direction=None):
        r'''Gets formula markup.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()

            ::

                >>> markup = segment._expression.get_formula_markup(name='J')
                >>> show(markup) # doctest: +SKIP
                
            ..  doctest::

                >>> f(markup)
                \markup {
                    \concat
                        {
                            A
                            \concat
                                {
                                    \hspace
                                        #0.4
                                    \bold
                                        J
                                }
                        }
                    }

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()
                >>> segment = segment.rotate(n=2)

            ::

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
                                    A
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

    def get_formula_string(self, name='X'):
        r'''Gets formula string.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()

            ::

                >>> segment._expression.get_formula_string(name='J')
                'A(J)'
                
        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()
                >>> segment = segment.rotate(n=2)

            ::

                >>> segment._expression.get_formula_string(name='J')
                'r2(A(J))'
                
        Returns string or none.
        '''
        import abjad
        if not self.callbacks:
            return
        callback = self.callbacks[0]
        try:
            string = callback.formula_string_template.format(name)
        except (IndexError, KeyError) as e:
            message = '{!r} with {!r} raises {!r}.'
            message = message.format(
                callback.formula_string_template,
                name,
                e,
                )
            raise Exception(message)
        for callback in self.callbacks[1:]:
            try:
                string = callback.formula_string_template.format(string)
            except (IndexError, KeyError) as e:
                message = '{!r} with {!r} raises {!r}.'
                message = message.format(
                    callback.formula_string_template,
                    string,
                    e,
                    )
                raise Exception(message)
        return string

    def label(self):
        r'''Appends label callback and sets label agent proxy.

        Returns expression.
        '''
        from abjad.tools import agenttools
        template = 'agenttools.LabelAgent(client={})'
        callback = type(self)(
            evaluation_template=template,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = agenttools.LabelAgent
        return result

    def sequence(self, name=None):
        r'''Appends sequence callback and sets sequence proxy.

        Returns expression.
        '''
        from abjad.tools import sequencetools
        formula_string_template = 'sequence({})'
        template = 'Sequence(items={{}}'
        if name is not None:
            template += ', name={name!r}'
        template += ')'
        template = template.format(name=name)
        callback = type(self)(
            evaluation_template=template,
            formula_string_template=formula_string_template,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        result = type(self)(callbacks=callbacks)
        result._proxy_class = sequencetools.Sequence
        return result
