# -*- coding: utf-8 -*-
import collections
import inspect
from abjad.tools import expressiontools
from abjad.tools.abctools import AbjadObject


class Sequence(AbjadObject):
    r'''Sequence.

    ..  container:: example

        Initializes sequence:

        ..  container:: example

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes and reverses sequence:

        ..  container:: example

            ::

                >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence_.reverse()
                Sequence([6, 5, 4, 3, 2, 1])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([6, 5, 4, 3, 2, 1])

    ..  container:: example

        Initializes, reverses and flattens sequence:

        ..  container:: example

            ::

                >>> sequence_ = Sequence([1, 2, 3, [4, 5, [6]]])
                >>> sequence_ = sequence_.reverse()
                >>> sequence_ = sequence_.flatten()
                >>> sequence_
                Sequence([4, 5, 6, 3, 2, 1])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.flatten()
                >>> expression([1, 2, 3, [4, 5, [6]]])
                Sequence([4, 5, 6, 3, 2, 1])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_equivalence_markup',
        '_expression',
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._equivalence_markup = None
        self._expression = None
        items = items or ()
        if not isinstance(items, collections.Iterable):
            items = [items]
        self._items = tuple(items)

    ### SPECIAL METHODS ###

    @expressiontools.Signature(
        markup_expression_callback='_make___add___markup_expression',
        string_template_callback='_make___add___string_template',
        )
    def __add__(self, argument):
        r'''Adds `argument` to sequence.

        ..  container:: example

            Adds tuple to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + (4, 5, 6)
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression + (4, 5, 6)

                ::

                    >>> expression([1, 2, 3])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    'J + (4, 5, 6)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                "(4, 5, 6)"
                            }
                        }

        ..  container:: example

            Adds list to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + [4, 5, 6]
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression + [4, 5, 6]

                ::

                    >>> expression([1, 2, 3])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    'J + [4, 5, 6]'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                "[4, 5, 6]"
                            }
                        }

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                ::

                    >>> sequence_1 = Sequence([1, 2, 3])
                    >>> sequence_2 = Sequence([4, 5, 6])
                    >>> sequence_1 + sequence_2
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression_1 = Expression(name='J')
                    >>> expression_1 = expression_1.sequence()
                    >>> expression_2 = Expression(name='K')
                    >>> expression_2 = expression_2.sequence()
                    >>> expression = expression_1 + expression_2

                ::

                    >>> expression([1, 2, 3], [4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    'J + K'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Reverses result:

            ..  container:: example

                ::

                    >>> sequence_1 = Sequence([1, 2, 3])
                    >>> sequence_2 = Sequence([4, 5, 6])
                    >>> sequence_ = sequence_1 + sequence_2
                    >>> sequence_.reverse()
                    Sequence([6, 5, 4, 3, 2, 1])

            ..  container:: example expression

                ::

                    >>> expression_1 = Expression(name='J')
                    >>> expression_1 = expression_1.sequence()
                    >>> expression_2 = Expression(name='K')
                    >>> expression_2 = expression_2.sequence()
                    >>> expression = expression_1 + expression_2
                    >>> expression = expression.reverse()

                ::

                    >>> expression([1, 2, 3], [4, 5, 6])
                    Sequence([6, 5, 4, 3, 2, 1])

                ::

                    >>> expression.get_string()
                    'R(J + K)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                R
                                \concat
                                    {
                                        (
                                        \line
                                            {
                                                \bold
                                                    J
                                                +
                                                \bold
                                                    K
                                            }
                                        )
                                    }
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        argument = type(self)(items=argument)
        items = self.items + argument.items
        return type(self)(items=items)

    def __eq__(self, argument):
        r'''Is true when `argument` is a sequence with items equal to those of
        this sequence. Otherwise false.

        ..  container:: example

            Is true when `argument` is a sequence with items equal to those of this
            sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) == Sequence([1, 2, 3, 4, 5, 6])
                True

        ..  container:: example

            Is false when `argument` is not a sequence with items equal to those of
            this sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6])
                False

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self._items == argument._items
        return False

    def __format__(self, format_specification=''):
        r'''Formats sequence.

        ..  container:: example

            Formats sequence:

            ::

                >>> f(Sequence([1, 2, 3, 4, 5, 6]))
                Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            Formats expression:

            ::

                >>> expression = Expression(name='J')
                >>> expression = expression.sequence()
                >>> f(expression)
                expressiontools.Expression(
                    callbacks=[
                        expressiontools.Expression(
                            evaluation_template='abjad.sequencetools.Sequence',
                            is_initializer=True,
                            markup_expression=expressiontools.Expression(
                                callbacks=[
                                    expressiontools.Expression(
                                        evaluation_template='abjad.markuptools.Markup',
                                        is_initializer=True,
                                        ),
                                    ],
                                proxy_class=markuptools.Markup,
                                ),
                            string_template='{}',
                            ),
                        ],
                    name='J',
                    proxy_class=sequencetools.Sequence,
                    )

        Returns string.
        '''
        return AbjadObject.__format__(
            self,
            format_specification=format_specification,
            )

    @expressiontools.Signature(
        markup_expression_callback='_make___getitem___markup_expression',
        string_template_callback='_make___getitem___string_template',
        )
    def __getitem__(self, argument):
        r'''Gets item at index or slice `argument` from sequence.

        ..  container:: example

            Gets first item in sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                    
                ::
                
                    >>> sequence_[0]
                    1

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression[0]

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    1

                ::

                    >>> expression.get_string()
                    'J[0]'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets last item in sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                 
                ::
                
                    >>> sequence_[-1]
                    6

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression[-1]

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    6

                ::

                    >>> expression.get_string()
                    'J[-1]'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    -1
                            }
                        }

        ..  container:: example

            Gets slice from sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                    >>> sequence_ = sequence_[:3]

                ::

                    >>> sequence_
                    Sequence([1, 2, 3])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression[:3]

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    Sequence([1, 2, 3])

                ::

                    >>> expression.get_string()
                    'J[:3]'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    [:3]
                            }
                        }

        ..  container:: example

            Gets item in sequence and wraps result in new sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                    >>> sequence_ = Sequence(sequence_[0])

                ::

                    >>> sequence_
                    Sequence([1])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression[0]
                    >>> expression = expression.sequence()

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    Sequence([1])

                ::

                    >>> expression.get_string()
                    'J[0]'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                \bold
                                    J
                                \sub
                                    0
                            }
                        }

        ..  container:: example

            Gets slice from sequence and flattens slice:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, [3, [4]], 5])
                    >>> sequence_ = sequence_[:-1]
                    >>> sequence_ = sequence_.flatten()

                ::

                    >>> sequence_
                    Sequence([1, 2, 3, 4])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression[:-1]
                    >>> expression = expression.flatten()

                ::

                    >>> expression([1, 2, [3, [4]], 5])
                    Sequence([1, 2, 3, 4])

                ::

                    >>> expression.get_string()
                    'flatten(J[:-1])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \concat
                                    {
                                        \bold
                                            J
                                        \sub
                                            [:-1]
                                    }
                                )
                            }
                        }

        Returns item or new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self._items.__getitem__(argument)
        if isinstance(argument, slice):
            return type(self)(items=result)
        return result

    def __hash__(self):
        r'''Hashes sequence.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Sequence, self).__hash__()

    def __len__(self):
        r'''Gets length of sequence.

        ..  container:: example

            Gets length of sequence:

            ::

                >>> len(Sequence([1, 2, 3, 4, 5, 6]))
                6

        ..  container:: example

            Gets length of sequence:

            ::

                >>> len(Sequence('text'))
                4

        Returns nonnegative integer.
        '''
        return len(self._items)

    def __ne__(self, argument):
        r'''Is true when sequence is not equal to `argument`. Otherwise false.

        ..  container:: example

            Is true when `argument` does not equal this sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) != (1, 2, 3, 4, 5, 6)
                True

        ..  container:: example

            Is false when `argument` does equal this seuqence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) != Sequence([1, 2, 3, 4, 5, 6])
                False

        '''
        return not self == argument

    @expressiontools.Signature(
        markup_expression_callback='_make___radd___markup_expression',
        string_template_callback='_make___radd___string_template',
        )
    def __radd__(self, argument):
        r'''Adds sequence to `argument`.

        ..  container:: example

            Adds sequence to tuple:

            ..  container:: example

                ::

                    >>> (1, 2, 3) + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='K')
                    >>> expression = expression.sequence()
                    >>> expression = (1, 2, 3) + expression

                ::

                    >>> expression([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    '(1, 2, 3) + K'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                "(1, 2, 3)"
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Adds sequence to list:

            ..  container:: example

                ::

                    >>> [1, 2, 3] + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='K')
                    >>> expression = expression.sequence()
                    >>> expression = [1, 2, 3] + expression

                ::

                    >>> expression([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    '[1, 2, 3] + K'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                "[1, 2, 3]"
                                +
                                \bold
                                    K
                            }
                        }

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression_1 = Expression(name='J')
                    >>> expression_1 = expression_1.sequence()
                    >>> expression_2 = Expression(name='K')
                    >>> expression_2 = expression_2.sequence()
                    >>> expression = expression_1 + expression_2

                ::

                    >>> expression([1, 2, 3], [4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

                ::

                    >>> expression.get_string()
                    'J + K'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \bold
                                    J
                                +
                                \bold
                                    K
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        argument = type(self)(items=argument)
        items = argument.items + self.items
        return type(self)(items=items)

    def __repr__(self):
        r'''Gets interpreter representation of sequence.

        ..  container:: example

            Gets interpreter representation:

            ::

                >>> Sequence([99])
                Sequence([99])

        ..  container:: example

            Gets interpreter representation:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

        Returns string.
        '''
        items = ', '.join([repr(_) for _ in self.items])
        string = '{}([{}])'
        string = string.format(type(self).__name__, items)
        if self._expression:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_map_markup_expression(operand):
        expression = expressiontools.Expression()
        expression = expression.wrap_in_list()
        expression = expression.markup_list()
        expression = expression.insert(0, '/@')
        operand_markup = operand.get_markup(name='X')
        expression = expression.insert(0, operand_markup)
        expression = expression.line()
        return expression
        
    @staticmethod
    def _make_map_string_template(operand):
        string_template = '{operand} /@ {{}}'
        operand = operand.get_string(name='X')
        string_template = string_template.format(operand=operand)
        return string_template

    @staticmethod
    def _make_partition_indicator(counts, cyclic, overhang, reversed_):
        indicator = [str(_) for _ in counts]
        indicator = ', '.join(indicator)
        if cyclic:
            indicator = '<{}>'.format(indicator)
        else:
            indicator = '[{}]'.format(indicator)
        if reversed_:
            indicator = 'R' + indicator
        if overhang is True:
            indicator += '+'
        elif overhang is Exact:
            indicator += '!'
        return indicator

    @staticmethod
    def _make_partition_ratio_indicator(ratio):
        return str(ratio)

    @staticmethod
    def _make_split_indicator(weights, cyclic, overhang):
        indicator = [str(_) for _ in weights]
        indicator = ', '.join(indicator)
        if cyclic:
            indicator = '<{}>'.format(indicator)
        else:
            indicator = '[{}]'.format(indicator)
        if overhang:
            indicator += '+'
        return indicator

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        map_operand=None,
        ):
        callback = expressiontools.Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            )
        return self._expression.append_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets sequence items.

        ..  container:: example

            ..  container:: example

                Initializes items positionally:

                ::

                    >>> Sequence([1, 2, 3, 4, 5, 6]).items
                    (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                ::

                    >>> Sequence(items=[1, 2, 3, 4, 5, 6]).items
                    (1, 2, 3, 4, 5, 6)

            ..  container:: example expression

                Initializes items positionally:

                ::

                    >>> expression = sequence()
                    >>> expression([1, 2, 3, 4, 5, 6]).items
                    (1, 2, 3, 4, 5, 6)

                Initializes items from keyword:

                ::

                    >>> expression = sequence()
                    >>> expression(items=[1, 2, 3, 4, 5, 6]).items
                    (1, 2, 3, 4, 5, 6)

        Returns tuple.
        '''
        return self._items

    ### PUBLIC METHODS ###

    @expressiontools.Signature()
    def flatten(self, classes=None, depth=-1, indices=None):
        r'''Flattens sequence.

        ..  container:: example

            Flattens sequence:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items=items)

                ::

                    >>> sequence_.flatten()
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten()

                ::

                    >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8])

                ::

                    >>> expression.get_string()
                    'flatten(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Flattens sequence to depth 1:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items)

                ::

                    >>> sequence_.flatten(depth=1)
                    Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten(depth=1)

                ::

                    >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                    Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

                ::

                    >>> expression.get_string()
                    'flatten(J, depth=1)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", depth=1)"
                            }
                        }

        ..  container:: example

            Flattens sequence to depth 2:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items)

                ::

                    >>> sequence_.flatten(depth=2)
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten(depth=2)

                ::

                    >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8])

                ::

                    >>> expression.get_string()
                    'flatten(J, depth=2)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", depth=2)"
                            }
                        }

        ..  container:: example

            Flattens sequence at indices:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items)

                ::

                    >>> sequence_.flatten(indices=[3])
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten(indices=[3])

                ::

                    >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

                ::

                    >>> expression.get_string()
                    'flatten(J, indices=[3])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", indices=[3])"
                            }
                        }

        ..  container:: example

            Flattens sequence at negative indices:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items)

                ::

                    >>> sequence_.flatten(indices=[-1])
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten(indices=[-1])

                ::

                    >>> expression([1, [2, 3, [4]], 5, [6, 7, [8]]])
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

                ::

                    >>> expression.get_string()
                    'flatten(J, indices=[-1])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", indices=[-1])"
                            }
                        }

        ..  container:: example

            Flattens tuples in sequence only:

            ..  container:: example

                ::

                    >>> items = ['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')]
                    >>> sequence_ = Sequence(items=items)

                ::

                    >>> sequence_.flatten(classes=(tuple,))
                    Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.flatten(classes=(tuple,))

                ::

                    >>> expression(['ab', 'cd', ('ef', 'gh'), ('ij', 'kl')])
                    Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

                ::

                    >>> expression.get_string()
                    'flatten(J, classes=(tuple,))'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                flatten(
                                \bold
                                    J
                                ", classes=(tuple,))"
                            }
                        }

        Returns new sequence.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = abjad.sequencetools.flatten_sequence(
            self._items[:],
            classes=classes,
            depth=depth,
            indices=indices,
            )
        return type(self)(items=items)

    def is_decreasing(self, strict=True):
        r'''Is true when sequence decreases.

        ..  container:: example

            Is true when sequence is strictly decreasing:

            ::

                >>> Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=True)
                True

            ::

                >>> Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=True)
                False

            ::

                >>> Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=True)
                False

            ::

                >>> Sequence().is_decreasing(strict=True)
                True

        ..  container:: example

            Is true when sequence decreases monotonically:

            ::

                >>> Sequence([5, 4, 3, 2, 1, 0]).is_decreasing(strict=False)
                True

            ::

                >>> Sequence([3, 3, 3, 2, 1, 0]).is_decreasing(strict=False)
                True

            ::

                >>> Sequence([3, 3, 3, 3, 3, 3]).is_decreasing(strict=False)
                True

            ::

                >>> Sequence().is_decreasing(strict=False)
                True

        Returns true or false.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current < previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not current <= previous:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_increasing(self, strict=True):
        r'''Is true when sequence increases.

        ..  container:: example

            Is true when sequence is strictly increasing:

            ::

                >>> Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=True)
                True

            ::

                >>> Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=True)
                False

            ::

                >>> Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=True)
                False

            ::

                >>> Sequence().is_increasing(strict=True)
                True

        ..  container:: example

            Is true when sequence increases monotonically:

            ::

                >>> Sequence([0, 1, 2, 3, 4, 5]).is_increasing(strict=False)
                True

            ::

                >>> Sequence([0, 1, 2, 3, 3, 3]).is_increasing(strict=False)
                True

            ::

                >>> Sequence([3, 3, 3, 3, 3, 3]).is_increasing(strict=False)
                True

            ::

                >>> Sequence().is_increasing(strict=False)
                True

        Returns true or false.
        '''
        if strict:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous < current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False
        else:
            try:
                previous = None
                for current in self:
                    if previous is not None:
                        if not previous <= current:
                            return False
                    previous = current
                return True
            except TypeError:
                return False

    def is_permutation(self, length=None):
        '''Is true when sequence is a permutation.

        ..  container:: example

            Is true when sequence is a permutation:

            ::

                >>> Sequence([4, 5, 0, 3, 2, 1]).is_permutation()
                True

        ..  container:: example

            Is false when sequence is not a permutation:

            ::

                >>> Sequence([1, 1, 5, 3, 2, 1]).is_permutation()
                False

        Returns true or false.
        '''
        return tuple(sorted(self)) == tuple(range(len(self)))

    def is_repetition_free(self):
        '''Is true when sequence is repetition-free.

        ..  container:: example

            Is true when sequence is repetition-free:

            ::

                >>> Sequence([0, 1, 2, 6, 7, 8]).is_repetition_free()
                True

        ..  container:: example

            Is true when sequence is empty:

            ::

                >>> Sequence().is_repetition_free()
                True

        ..  container:: example

            Is false when sequence contains repetitions:

            ::

                >>> Sequence([0, 1, 2, 2, 7, 8]).is_repetition_free()
                False

        Returns true or false.
        '''
        import abjad
        try:
            pairs = abjad.sequencetools.iterate_sequence_nwise(self)
            for left, right in pairs:
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    @expressiontools.Signature(
        markup_expression_callback='_make_map_markup_expression',
        string_template_callback='_make_map_string_template',
        )
    def map(self, operand):
        r'''Maps `operand` to sequence items.

        ..  container:: example

            Partitions sequence and sums parts:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(1, 10+1))
                    >>> sequence_ = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     )
                    >>> sequence_ = sequence_.map(sum)

                ::

                    >>> sequence_
                    Sequence([6, 15, 24])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     )
                    >>> expression = expression.map(sequence().sum())

                ::

                    >>> expression(range(1, 10+1))
                    Sequence([6, 15, 24])

                ::

                    >>> expression.get_string()
                    'sum(X) /@ partition(J, <3>)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        sum(
                                        \bold
                                            X
                                        )
                                    }
                                /@
                                \concat
                                    {
                                        partition(
                                        \bold
                                            J
                                        ", <3>)"
                                    }
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template='map',
                map_operand=operand,
                )
        items = [operand(_) for _ in self]
        return type(self)(items=items)

    @expressiontools.Signature(
        argument_list_callback='_make_partition_indicator',
        method_name='partition',
        )
    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        overhang=False,
        reversed_=False,
        ):
        r'''Partitions sequence by `counts`.

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> sequence_ = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> sequence_
                    Sequence([Sequence([0, 1, 2])])

                ::

                    >>> for part in sequence_:
                    ...     part
                    Sequence([0, 1, 2])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])

                ::

                    >>> expression.get_string()
                    'partition(J, [3])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3])"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])

                ::

                    >>> expression.get_string()
                    'partition(J, [4, 3])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [4, 3])"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])

                ::

                    >>> expression.get_string()
                    'partition(J, <3>)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <3>)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])

                ::

                    >>> expression.get_string()
                    'partition(J, <4, 3>)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <4, 3>)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, [3]+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3]+)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, [4, 3]+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [4, 3]+)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])
                    Sequence([15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])
                    Sequence([15])

                ::

                    >>> expression.get_string()
                    'partition(J, <3>+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <3>+)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])
                    Sequence([14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])
                    Sequence([14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, <4, 3>+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <4, 3>+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R[3])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[3])"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R[4, 3])'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[4, 3])"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::
                
                    >>> for part in parts:
                    ...     part
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::
                
                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R<3>)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<3>)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts without overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R<4, 3>)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<4, 3>)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                    Sequence([13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                    Sequence([13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R[3]+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[3]+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence once by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R[4, 3]+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R[4, 3]+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0])
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0])
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R<3>+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<3>+)"
                            }
                        }

        ..  container:: example

            Reverse-partitions sequence cyclically by counts with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(16))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

                ::

                    >>> expression.get_string()
                    'partition(J, R<4, 3>+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", R<4, 3>+)"
                            }
                        }

        ..  container:: example

            Partitions sequence once by counts and asserts that sequence
            partitions exactly (with no overhang):

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [2, 3, 5],
                    ...     cyclic=False,
                    ...     overhang=Exact,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8, 9])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [2, 3, 5],
                    ...     cyclic=False,
                    ...     overhang=Exact,
                    ...     )

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8, 9])

                ::

                    >>> expression.get_string()
                    'partition(J, [2, 3, 5]!)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [2, 3, 5]!)"
                            }
                        }

        ..  container:: example

            Partitions sequence cyclically by counts and asserts that sequence
            partitions exactly Exact partitioning means partitioning with no
            overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10))
                    >>> parts = sequence_.partition_by_counts(
                    ...     [2],
                    ...     cyclic=True,
                    ...     overhang=Exact,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3])
                    Sequence([4, 5])
                    Sequence([6, 7])
                    Sequence([8, 9])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [2],
                    ...     cyclic=True,
                    ...     overhang=Exact,
                    ...     )

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3])
                    Sequence([4, 5])
                    Sequence([6, 7])
                    Sequence([8, 9])

                ::

                    >>> expression.get_string()
                    'partition(J, <2>!)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", <2>!)"
                            }
                        }

        ..  container:: example

            Partitions string:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence('some text')
                    >>> parts = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence(['s', 'o', 'm'])
                    Sequence(['e', ' ', 't', 'e', 'x', 't'])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> for part in expression('some text'):
                    ...     part
                    Sequence(['s', 'o', 'm'])
                    Sequence(['e', ' ', 't', 'e', 'x', 't'])

                ::

                    >>> expression.get_string()
                    'partition(J, [3]+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", [3]+)"
                            }
                        }

        Returns nested sequence.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        items = self._items[:]
        subsequences = []
        parts = abjad.sequencetools.partition_sequence_by_counts(
            items,
            counts,
            cyclic=cyclic,
            overhang=overhang,
            reversed_=reversed_,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(items=parts)

    @expressiontools.Signature(
        argument_list_callback='_make_partition_ratio_indicator',
        method_name='partition',
        )
    def partition_by_ratio_of_lengths(self, ratio):
        r'''Partitions sequence by `ratio` of lengths.

        ..  container:: example

            Partitions sequence by ``1:1:1`` ratio:

            ..  container:: example

                ::

                    >>> numbers = Sequence(range(10))
                    >>> ratio = mathtools.Ratio((1, 1, 1))

                ::

                    >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6])
                    Sequence([7, 8, 9])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> ratio = mathtools.Ratio((1, 1, 1))
                    >>> expression = expression.partition_by_ratio_of_lengths(ratio)

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6])
                    Sequence([7, 8, 9])

                ::

                    >>> expression.get_string()
                    'partition(J, 1:1:1)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", 1:1:1)"
                            }
                        }

        ..  container:: example

            Partitions sequence by ``1:1:2`` ratio:

            ..  container:: example

                ::

                    >>> numbers = Sequence(range(10))
                    >>> ratio = mathtools.Ratio((1, 1, 2))

                ::

                    >>> for part in numbers.partition_by_ratio_of_lengths(ratio):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4])
                    Sequence([5, 6, 7, 8, 9])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> ratio = mathtools.Ratio((1, 1, 2))
                    >>> expression = expression.partition_by_ratio_of_lengths(ratio)

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4])
                    Sequence([5, 6, 7, 8, 9])

                ::

                    >>> expression.get_string()
                    'partition(J, 1:1:2)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                partition(
                                \bold
                                    J
                                ", 1:1:2)"
                            }
                        }

        Returns a sequence of sequences.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        parts = abjad.sequencetools.partition_sequence_by_ratio_of_lengths(
            self.items,
            ratio=ratio,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(items=parts)

    @expressiontools.Signature(is_operator=True, method_name='R')
    def reverse(self):
        '''Reverses sequence.

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5])
                    
                ::

                    >>> sequence_.reverse()
                    Sequence([5, 4, 3, 2, 1])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.reverse()

                ::

                    >>> expression([1, 2, 3, 4, 5])
                    Sequence([5, 4, 3, 2, 1])

                ::

                    >>> expression.get_string()
                    'R(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                R
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence('text')
                    
                ::
                
                    >>> sequence_.reverse()
                    Sequence(['t', 'x', 'e', 't'])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.reverse()

                ::

                    >>> expression('text')
                    Sequence(['t', 'x', 'e', 't'])

                ::

                    >>> expression.get_string()
                    'R(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                R
                                \bold
                                    J
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return type(self)(items=reversed(self))

    @expressiontools.Signature( 
        is_operator=True,
        method_name='r',
        subscript='n',
        )
    def rotate(self, n=0):
        '''Rotates sequence by index `n`.

        ..  container:: example

            Rotates sequence to the right:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10))
                    
                ::
                
                    >>> sequence_.rotate(n=4)
                    Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.rotate(n=4)

                ::

                    >>> expression(range(10))
                    Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

                ::

                    >>> expression.get_string()
                    'r4(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    4
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Rotates sequence to the left:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10))
                    
                ::
                
                    >>> sequence_.rotate(n=-3)
                    Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.rotate(n=-3)

                ::

                    >>> expression(range(10))
                    Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

                ::

                    >>> expression.get_string()
                    'r-3(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    -3
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Rotates sequence neither to the right nor the left:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10))

                ::

                    >>> sequence_.rotate(n=0)
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.rotate(n=0)

                ::

                    >>> expression(range(10))
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

                ::

                    >>> expression.get_string()
                    'r0(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    0
                                \bold
                                    J
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        n = n or 0
        items = []
        if len(self):
            n = n % len(self)
            for item in self[-n:len(self)] + self[:-n]:
                items.append(item)
        return type(self)(items=items)

    @expressiontools.Signature(
        argument_list_callback='_make_split_indicator',
        )
    def split(self, weights, cyclic=False, overhang=False):
        r'''Splits sequence by `weights`.

        ..  todo:: Port remaining examples from
            ``sequencetools.split_sequence()``.

        ..  container:: example

            Splits sequence cyclically by weights with overhang:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([10, -10, 10, -10])

                ::

                    >>> parts = sequence_.split(
                    ...     (3, 15, 3),
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )
                    >>> for part in parts:
                    ...     part
                    Sequence([3])
                    Sequence([7, -8])
                    Sequence([-2, 1])
                    Sequence([3])
                    Sequence([6, -9])
                    Sequence([-1])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.split(
                    ...     (3, 15, 3),
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )

                ::

                    >>> parts = expression([10, -10, 10, -10])
                    >>> for part in parts:
                    ...     part
                    Sequence([3])
                    Sequence([7, -8])
                    Sequence([-2, 1])
                    Sequence([3])
                    Sequence([6, -9])
                    Sequence([-1])

                ::

                    >>> expression.get_string()
                    'split(J, <3, 15, 3>+)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                split(
                                \bold
                                    J
                                ", <3, 15, 3>+)"
                            }
                        }

        Returns new sequence.
        '''
        import abjad
        if self._expression:
            return self._update_expression(inspect.currentframe())
        parts = abjad.sequencetools.split_sequence(
            self.items,
            weights,
            cyclic=cyclic,
            overhang=overhang,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(items=parts)

    @expressiontools.Signature()
    def sum(self):
        '''Sums sequence.

        ..  container:: example

            Sums sequence of positive numbers:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    
                ::
                
                    >>> sequence_.sum()
                    55

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.sum()

                ::

                    >>> expression([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    55

                ::

                    >>> expression.get_string()
                    'sum(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Sum sequence of numbers with mixed signs:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
                    
                ::
                
                    >>> sequence_.sum()
                    5
                    
            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.sum()

                ::

                    >>> expression([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
                    5

                ::

                    >>> expression.get_string()
                    'sum(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            Sums sequence and wraps result in new sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(1, 10+1))
                    >>> result = sequence_.sum()
                    >>> sequence_ = Sequence(result)

                ::

                    >>> sequence_
                    Sequence([55])

            ..  container:: example expression

                ::

                    >>> expression = Expression(name='J')
                    >>> expression = expression.sequence()
                    >>> expression = expression.sum()
                    >>> expression = expression.sequence()

                ::

                    >>> expression(range(1, 10+1))
                    Sequence([55])

                ::

                    >>> expression.get_string()
                    'sum(J)'

                ::

                    >>> markup = expression.get_markup()
                    >>> show(markup) # doctest: +SKIP

                ..  doctest::

                    >>> f(markup)
                    \markup {
                        \concat
                            {
                                sum(
                                \bold
                                    J
                                )
                            }
                        }

        Returns new sequence.
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if len(self) == 0:
            return 0
        result = self[0]
        for item in self[1:]:
            result += item
        return result


collections.Sequence.register(Sequence)
