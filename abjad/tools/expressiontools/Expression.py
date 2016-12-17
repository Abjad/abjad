# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class Expression(AbjadObject):
    r'''Expression.

    ..  container:: example

        Empty expression:

        ::

            >>> expression = expressiontools.Expression()
            >>> expression
            Expression()

        ::

            >>> expression() is None
            True

    ..  container:: example

        Nonempty expression:

        ::

            >>> expression = expressiontools.Expression()
            >>> expression = expression.make_callback('Markup({})')
            >>> expression = expression.make_callback('{}.italic()')

        ::

            >>> expression('text')
            Markup(contents=(MarkupCommand('italic', 'text'),))

        ::

            >>> show(expression('text')) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __call__(self, *args, **kwargs):
        r'''Calls expression on `args` and `kwargs`.

        ..  container:: example

            Calls empty expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> expression() is None
                True

        ..  container:: example

            Calls nonempty expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')
                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> expression('text')
                Markup(contents=(MarkupCommand('italic', 'text'),))

        Returns ouput of last callback.
        '''
        if not self.callbacks:
            return
        callback = self.callbacks[0]
        result = callback(*args, **kwargs)
        for callback in self.callbacks[1:]:
            result = callback(result)
        return result

    def __format__(self, format_specification=''):
        r'''Formats expression.

        ..  container:: example

            Formats empty expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> print(format(expression))
                expressiontools.Expression()

        ..  container:: example

            Formats nonempty expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')
                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> print(format(expression))
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Callback(
                            'Markup({})'
                            ),
                        expressiontools.Callback(
                            '{}.italic()'
                            ),
                        ),
                    )

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__format__(
            format_specification=format_specification,
            )

    def __repr__(self):
        r'''Gets interpreter representation of expression.

        ..  container:: example

            Gets interpreter representation of empty expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> expression
                Expression()

        ..  container:: example

            Gets interpreter representation of nonempty expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')
                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> expression
                Expression(callbacks=(Callback('Markup({})'), Callback('{}.italic()')))

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__repr__()

    def __str__(self):
        r'''Gets string representation of expression.

        ..  container:: example

            Gets string representation of empty expression:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> str(expression)
                'Expression()'

        ..  container:: example

            Gets string representation of nonempty expression:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')
                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> str(expression)
                "Expression(callbacks=(Callback('Markup({})'), Callback('{}.italic()')))"

        Returns string.
        '''
        superclass = super(Expression, self)
        return superclass.__str__()

    ### PRIVATE METHODS ###

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
            return object_._expression.get_markup(
                direction=direction,
                name=name,
                )
        elif name is not None:
            return abjad.Markup(contents=name, direction=direction).bold()

    def _make_parentheses(self):
        markup_expression = type(self)()
        markup_expression = markup_expression.make_callback(
            'Markup({}).parenthesize()',
            )
        return markup_expression

    @staticmethod
    def _track_expression(
        source_object,
        target_object,
        method_name,
        arguments=None,
        direction=None,
        markup_expression=None,
        module_names=None,
        precedence=None,
        string_expression=None,
        ):
        if source_object._name is None:
            return
        template = '{}.{}'.format(type(source_object).__name__, method_name)
        expression = source_object._expression or Expression()
        expression = expression.make_callback(
            template=template,
            arguments=arguments,
            direction=direction,
            markup_expression=markup_expression,
            module_names=module_names,
            precedence=precedence,
            string_expression=string_expression,
            )
        target_object._expression = expression

    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets expression callbacks.

        ..  container:: example

            Is none:

            ::

                >>> expression = expressiontools.Expression()

            ::

                >>> expression.callbacks is None
                True

        ..  container:: example

            Gets callbacks:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')
                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> for callback in expression.callbacks:
                ...     callback
                Callback('Markup({})')
                Callback('{}.italic()')

        ..  container:: example

            Returns tuple or none:

            ::

                >>> isinstance(expression.callbacks, tuple)
                True

        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    @staticmethod
    def establish_equivalence(object_, name):
        r'''Establishes equivalence.
        
        Makes new object with `name` and equivalence markup.

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

    def make_callback(
        self,
        template,
        arguments=None,
        direction=None,
        markup_expression=None,
        module_names=None,
        precedence=None,
        string_expression=None,
        ):
        r'''Makes (and appends) callback to expression.

        ..  container:: example

            Makes (and appends) callback:

            ::

                >>> expression = expressiontools.Expression()
                >>> expression = expression.make_callback('Markup({})')

            ::

                >>> for callback in expression.callbacks:
                ...     callback
                Callback('Markup({})')

        ..  container:: example

            Makes (and appends) callback:

            ::

                >>> expression = expression.make_callback('{}.italic()')

            ::

                >>> for callback in expression.callbacks:
                ...     callback
                Callback('Markup({})')
                Callback('{}.italic()')

        Returns new expression.
        '''
        import abjad
        callback = abjad.expressiontools.Callback(
            template=template,
            arguments=arguments,
            direction=direction,
            markup_expression=markup_expression,
            module_names=module_names,
            precedence=precedence,
            string_expression=string_expression,
            )
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)

    def get_markup(self, name, direction=None):
        r'''Gets expression markup.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()

            ::

                >>> markup = segment._expression.get_markup(name='J')
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

                >>> markup = segment._expression.get_markup(name='J')
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
        if not self.callbacks:
            return
        markup = abjad.Markup(name).bold()
        callback = self.callbacks[0]
        if callback.direction in (Left, None):
            markup = [abjad.Markup.hspace(0.4), markup]
            markup = abjad.Markup.concat(markup)
        markup = callback.markup_expression(markup)
        previous_precedence = callback.precedence or 0
        for callback in self.callbacks[1:]:
            current_precedence = callback.precedence or 0
            parenthesize_argument = False
            if previous_precedence < current_precedence:
                expression = self._make_parentheses()
                markup = expression(markup)
            markup = callback.markup_expression(markup)
        markup = abjad.new(markup, direction=direction)
        return markup

    def get_string(self, name='X'):
        r'''Gets expression string.

        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()

            ::

                >>> segment._expression.get_string(name='J')
                'A(J)'
                
        ..  container:: example

            ::

                >>> items = [-2, -1.5, 6, 7, -1.5, 7]
                >>> segment = pitchtools.PitchClassSegment(items=items, name='J')
                >>> segment = segment.alpha()
                >>> segment = segment.rotate(n=2)

            ::

                >>> segment._expression.get_string(name='J')
                'r2(A(J))'
                
        Returns string or none.
        '''
        import abjad
        if not self.callbacks:
            return
        callback = self.callbacks[0]
        try:
            string = callback.string_expression.format(name)
        except (IndexError, KeyError) as e:
            message = '{!r} with {!r} raises {!r}.'
            message = message.format(
                callback.string_expression,
                name,
                e,
                )
            raise Exception(message)
        for callback in self.callbacks[1:]:
            try:
                string = callback.string_expression.format(string)
            except (IndexError, KeyError) as e:
                message = '{!r} with {!r} raises {!r}.'
                message = message.format(
                    callback.string_expression,
                    string,
                    e,
                    )
                raise Exception(message)
        return string
