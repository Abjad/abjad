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
                >>> f(expression)
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Expression(
                            evaluation_template='Sequence(items={})',
                            formula_string_template='sequence({})',
                            ),
                        ),
                    )

            ::

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes and reverses sequence:

        ..  container:: example

            ::

                >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                
            ::
            
                >>> sequence_.reverse()
                Sequence([6, 5, 4, 3, 2, 1])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> f(expression)
                expressiontools.Expression(
                    callbacks=(
                        expressiontools.Expression(
                            evaluation_template='Sequence(items={})',
                            formula_string_template='sequence({})',
                            ),
                        expressiontools.Expression(
                            evaluation_template='{}.reverse()',
                            formula_markup_expression=expressiontools.Expression(
                                callbacks=(
                                    expressiontools.Expression(
                                        evaluation_template='Markup({})',
                                        ),
                                    expressiontools.Expression(
                                        evaluation_template="Markup.concat(['R', {}])",
                                        ),
                                    ),
                                ),
                            formula_string_template='R({})',
                            ),
                        ),
                    )

            ::

                >>> expression([1, 2, 3, 4, 5, 6])
                Sequence([6, 5, 4, 3, 2, 1])

    ..  container:: example

        Initializes, reverses and flattens sequence:

        ..  container:: example

            ::

                >>> sequence_ = Sequence([1, 2, 3, [4, 5, [6]]])
                >>> sequence_ = sequence_.reverse()
                >>> sequence_ = sequence_.flatten()

            ::

                >>> sequence_
                Sequence([4, 5, 6, 3, 2, 1])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.flatten()
                >>> expression.get_formula_string()
                'flatten(R(sequence(X)))'

            ::

                >>> expression([1, 2, 3, [4, 5, [6]]])
                Sequence([4, 5, 6, 3, 2, 1])

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_equivalence_markup',
        '_expression',
        '_is_frozen',
        '_items',
        '_name',
        '_name_markup',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, name=None, name_markup=None):
        self._equivalence_markup = None
        self._expression = None
        self._is_frozen = None
        items = items or ()
        if not isinstance(items, collections.Iterable):
            items = [items]
        self._items = tuple(items)
        if name is None:
            name = getattr(items, '_name', None)
        self._name = name
        if name_markup is None:
            name_markup = getattr(items, '_name_markup', None)    
        self._name_markup = name_markup

    ### SPECIAL METHODS ###

    def __add__(self, sequence_):
        r'''Adds `sequence_` to sequence.

        ..  container:: example

            Adds tuple to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + (4, 5, 6)
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = sequence() + (4, 5, 6)
                    >>> expression([1, 2, 3])
                    Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds list to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + [4, 5, 6]
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = sequence() + [4, 5, 6]
                    >>> expression([1, 2, 3])
                    Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                ::

                    >>> sequence_1 = Sequence([1, 2, 3], name='J')
                    >>> sequence_2 = Sequence([4, 5, 6], name='K')
                    >>> sequence_1 + sequence_2
                    Sequence([1, 2, 3, 4, 5, 6], name='J + K')

            ..  container:: example expression

                ::

                    >>> expression_1 = sequence(name='J')
                    >>> expression_2 = sequence(name='K')
                    >>> expression_1([1, 2, 3]) + expression_2([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6], name='J + K')

        Returns new sequence.
        '''
        formula_string_template = '{{}} + {}'
        if hasattr(sequence_, 'name'):
            formula_string_template = formula_string_template.format(
                sequence_.name)
        else:
            formula_string_template = formula_string_template.format(sequence_)
        if self._is_frozen:
            template = '{{}}.__add__(sequence_={sequence_})'
            template = template.format(sequence_=sequence_)
            return self._is_frozen.append_callback(
                evaluation_template=template,
                formula_string_template=formula_string_template,
                )
        sequence_ = type(self)(sequence_)
        name = None
        if self.name and sequence_.name:
            name_template = '{sequence} + {sequence_}'
            name = name_template.format(
                sequence=self.name,
                sequence_=sequence_.name,
                )
        items = self._items + sequence_._items
        result = type(self)(items=items, name=name)
        return result

    def __eq__(self, expr):
        r'''Is true when `expr` is a sequence with items equal to those of
        this sequence. Otherwise false.

        ..  container:: example

            Is true when `expr` is a sequence with items equal to those of this
            sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) == Sequence([1, 2, 3, 4, 5, 6])
                True

        ..  container:: example

            Is false when `expr` is not a sequence with items equal to those of
            this sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) == ([1, 2, 3, 4, 5, 6])
                False

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self._items == expr._items
        return False

    def __format__(self, format_specification=''):
        r'''Formats sequence.

        ..  container:: example

            Gets storage format:

            ::

                >>> print(format(Sequence([1, 2, 3, 4, 5, 6])))
                sequencetools.Sequence(
                    items=(1, 2, 3, 4, 5, 6),
                    )

        Returns string.
        '''
        return AbjadObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __getitem__(self, i):
        r'''Gets item `i` from sequence.

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

                    >>> expression = sequence()
                    >>> expression = expression[0]
                    >>> expression.get_formula_string()
                    'sequence(X)[0]'

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    1

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

                    >>> expression = sequence()
                    >>> expression = expression[-1]
                    >>> expression.get_formula_string()
                    'sequence(X)[-1]'

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    6

        ..  container:: example

            Gets slice from sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6], name='J')
                    >>> sequence_ = sequence_[:3]

                ::

                    >>> sequence_
                    Sequence([1, 2, 3], name='J[:3]')

            ..  container:: example expression

                ::

                    >>> expression = sequence(name='J')
                    >>> expression = expression[:3]
                    >>> expression.get_formula_string()
                    'sequence(X)[:3]'

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    Sequence([1, 2, 3], name='J[:3]')

                ..  note:: Implement calltime names:

                    >>> expression = sequence()[:3]
                    >>> expression([1, 2, 3, 4, 5, 6], name='J') # doctest: +SKIP

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

                    >>> expression = sequence()
                    >>> expression = expression[0]
                    >>> expression = expression.sequence()
                    >>> expression.get_formula_string()
                    'sequence(sequence(X)[0])'

                ::

                    >>> expression([1, 2, 3, 4, 5, 6])
                    Sequence([1])

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

                    >>> expression = sequence()
                    >>> expression = expression[:-1]
                    >>> expression = expression.flatten()
                    >>> expression.get_formula_string()
                    'flatten(sequence(X)[:-1])'

                ::

                    >>> expression([1, 2, [3, [4]], 5])
                    Sequence([1, 2, 3, 4])

        Returns item or new sequence.
        '''
        if self._is_frozen:
            if isinstance(i, int):
                formula_string_template = '{{}}[{i}]'
                start = stop = step = None
            elif isinstance(i, slice):
                if i.step is not None:
                    raise NotImplementedError
                if i.start is None and i.stop is None:
                    formula_string_template = '{{}}[:]'
                elif i.start is None:
                    formula_string_template = '{{}}[:{stop}]'
                elif i.stop is None:
                    formula_string_template = '{{}}[{start}:]'
                else:
                    formula_string_template = '{{}}[{start}:{stop}]'
                start = i.start
                stop = i.stop
                step = i.step
            else:
                message = 'must be integer or slice: {!r}.'
                message = message.format(i)
                raise TypeError(message)
            formula_string_template = formula_string_template.format(
                i=i,
                start=start,
                stop=stop,
                )
            template = '{{}}.__getitem__(i={i})'
            template = template.format(i=i)
            return self._is_frozen.append_callback(
                evaluation_template=template,
                formula_string_template=formula_string_template,
                )
        name = None
        if self.name:
            if isinstance(i, int):
                name_template = '{sequence}[{i}]'
                start = stop = step = None
            elif isinstance(i, slice):
                if i.step is not None:
                    raise NotImplementedError
                if i.start is None and i.stop is None:
                    name_template = '{sequence}[:]'
                elif i.start is None:
                    name_template = '{sequence}[:{stop}]'
                elif i.stop is None:
                    name_template = '{sequence}[{start}:]'
                else:
                    name_template = '{sequence}[{start}:{stop}]'
                start = i.start
                stop = i.stop
                step = i.step
            else:
                message = 'must be integer or slice: {!r}.'
                message = message.format(i)
                raise TypeError(message)
            name = name_template.format(
                sequence=self.name,
                i=i,
                start=start,
                stop=stop,
                step=step,
                )
        result = self._items.__getitem__(i)
        if isinstance(i, slice):
            return type(self)(result, name=name)
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

    def __ne__(self, expr):
        r'''Is true when sequence is not equal to `expr`. Otherwise false.

        ..  container:: example

            Is true when `expr` does not equal this sequence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) != (1, 2, 3, 4, 5, 6)
                True

        ..  container:: example

            Is false when `expr` does equal this seuqence:

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]) != Sequence([1, 2, 3, 4, 5, 6])
                False

        '''
        return not self == expr

    def __radd__(self, expr):
        r'''Adds sequence to `expr`.

        ..  container:: example

            Adds sequence to sequence:

            ..  container:: example

                ::

                    >>> Sequence([1, 2, 3]) + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression_1 = sequence()
                    >>> expression_2 = sequence()
                    >>> expression_1([1, 2, 3]) + expression_2([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to tuple:

            ..  container:: example

                ::

                    >>> (1, 2, 3) + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = (1, 2, 3) + sequence()
                    >>> expression([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example

            Adds sequence to list:

            ..  container:: example

                ::

                    >>> [1, 2, 3] + Sequence([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

            ..  container:: example expression

                ::

                    >>> expression = [1, 2, 3] + sequence()
                    >>> expression([4, 5, 6])
                    Sequence([1, 2, 3, 4, 5, 6])

        Returns new sequence.
        '''
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                formula_string_template='{} + {{}}'.format(self.name)
                )
        expr = type(self)(expr)
        items = expr._items + self._items
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
        if self.name:
            string = '{}([{}], name={!r})'
            string = string.format(type(self).__name__, items, self.name)
        else:
            string = '{}([{}])'
            string = string.format(type(self).__name__, items)
        if self._is_frozen:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    def _make_callback(
        self,
        frame,
        formula_markup_expression=None,
        formula_string_template=None,
        string_arguments=None,
        string_name=None,
        ):
        assert self._is_frozen, repr(self._is_frozen)
        Expression = expressiontools.Expression
        template = Expression._make_evaluation_template(frame)
        if formula_string_template:
            pass
        elif string_name is not None and string_arguments is None:
            arguments = Expression._wrap_arguments(frame)
            if arguments:
                formula_string_template = '{string_name}({{}}, {arguments})'
            else:
                formula_string_template = '{string_name}({{}})'
            formula_string_template = formula_string_template.format(
                string_name=string_name,
                arguments=arguments,
                )
        elif string_name is not None and string_arguments is not None:
            formula_string_template = '{string_name}({{}}, {string_arguments})'
            formula_string_template = formula_string_template.format(
                string_name=string_name,
                string_arguments=string_arguments,
                )
        return self._is_frozen.append_callback(
            evaluation_template=template,
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            )
        
    @staticmethod
    def _make_partition_indicator(counts, cyclic, reversed_, overhang):
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

    ### PUBLIC PROPERTIES ###

    @property
    def degree_of_rotational_symmetry(self):
        '''Gets degree of rotational symmetry.

        ..  container:: example

            ::

                >>> Sequence([1, 1, 1, 1, 1, 1]).degree_of_rotational_symmetry
                6

            ::

                >>> Sequence([1, 2, 1, 2, 1, 2]).degree_of_rotational_symmetry
                3

            ::

                >>> Sequence([1, 2, 3, 1, 2, 3]).degree_of_rotational_symmetry
                2

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]).degree_of_rotational_symmetry
                1

            ::

                >>> Sequence().degree_of_rotational_symmetry
                1

        Returns positive integer.
        '''
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
        return degree_of_rotational_symmetry

    @property
    def items(self):
        r'''Gets sequence items.

        ..  container:: example

            Gets sequence items:

            ::

                >>> sequence_ = Sequence([1, 2, 3, 4, 5, 6])
                >>> sequence_.items
                (1, 2, 3, 4, 5, 6)

        ..  container:: example

            Gets sequence items:

            ::

                >>> sequence_ = Sequence('text')
                >>> sequence_.items
                ('t', 'e', 'x', 't')

        Returns tuple.
        '''
        return self._items

    @property
    def name(self):
        r'''Gets sequence name.

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        if self._expression is not None:
            return self._expression.get_formula_string(name=self._name)
        return self._name

    @property
    def name_markup(self):
        r'''Gets sequence name markup.

        Defaults to none.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._name_markup

    @property
    def period_of_rotation(self):
        '''Gets period of rotation.

        ..  container:: example

            ::

                >>> Sequence([1, 2, 3, 4, 5, 6]).period_of_rotation
                6

            ::

                >>> Sequence([1, 2, 3, 1, 2, 3]).period_of_rotation
                3

            ::

                >>> Sequence([1, 2, 1, 2, 1, 2]).period_of_rotation
                2

            ::

                >>> Sequence([1, 1, 1, 1, 1, 1]).period_of_rotation
                1

            ::

                >>> Sequence().period_of_rotation
                0

        Defined equal to length of sequence divided by degree of rotational
        symmetry of sequence.

        Returns positive integer.
        '''
        return len(self) // self.degree_of_rotational_symmetry

    ### PUBLIC METHODS ###

    def flatten(self, classes=None, depth=-1, indices=None):
        r'''Flattens sequence.

        ..  container:: example

            Flattens sequence:

            ..  container:: example

                ::

                    >>> items = [1, [2, 3, [4]], 5, [6, 7, [8]]]
                    >>> sequence_ = Sequence(items=items, name='J')

                ::

                    >>> sequence_.flatten()
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8], name='flatten(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence(name='J')
                    >>> expression = expression.flatten()
                    >>> expression.get_formula_string()
                    'flatten(sequence(X))'

                ::

                    >>> expression(items)
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8], name='flatten(J)')

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

                    >>> expression = sequence()
                    >>> expression = expression.flatten(depth=1)
                    >>> expression.get_formula_string()
                    'flatten(sequence(X), depth=1)'

                ::

                    >>> expression(items)
                    Sequence([1, 2, 3, [4], 5, 6, 7, [8]])

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

                    >>> expression = sequence()
                    >>> expression = expression.flatten(depth=2)
                    >>> expression.get_formula_string()
                    'flatten(sequence(X), depth=2)'

                ::

                    >>> expression(items)
                    Sequence([1, 2, 3, 4, 5, 6, 7, 8])

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

                    >>> expression = sequence()
                    >>> expression = expression.flatten(indices=[3])
                    >>> expression.get_formula_string()
                    'flatten(sequence(X), indices=[3])'

                ::

                    >>> expression(items)
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

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

                    >>> expression = sequence()
                    >>> expression = expression.flatten(indices=[-1])
                    >>> expression.get_formula_string()
                    'flatten(sequence(X), indices=[-1])'

                ::

                    >>> expression(items)
                    Sequence([1, [2, 3, [4]], 5, 6, 7, 8])

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

                    >>> expression = sequence()
                    >>> expression = expression.flatten(classes=(tuple,))
                    >>> expression.get_formula_string()
                    'flatten(sequence(X), classes=(tuple,))'

                ::

                    >>> expression(items)
                    Sequence(['ab', 'cd', 'ef', 'gh', 'ij', 'kl'])

        Returns new sequence.
        '''
        from abjad.tools import sequencetools
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                string_name='flatten',
                )
        items = sequencetools.flatten_sequence(
            self._items[:],
            classes=classes,
            depth=depth,
            indices=indices,
            )
        name = None
        if self.name:
            name_template = 'flatten({sequence})'
            name = name_template.format(
                sequence=self.name,
                depth=depth,
                indices=indices,
                )
        result = type(self)(items=items, name=name)
        return result

    def is_decreasing(self, strict=True):
        r'''Is true when sequence decreases.

        ..  container:: example

            Strictly decreasing:

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

            Monotonically decreasing:

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

            Strictly increasing:

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

            Monotonically increasing:

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
        from abjad.tools import sequencetools
        try:
            pairs = sequencetools.iterate_sequence_nwise(self)
            for left, right in pairs:
                if left == right:
                    return False
            return True
        except TypeError:
            return False

    def is_restricted_growth_function(self):
        '''Is true when sequence is a restricted growth function.

        ..  container:: example

            Is true when sequence is a restricted growth function:

            ::

                >>> Sequence([1, 1, 1, 1]).is_restricted_growth_function()
                True

            ::


                >>> Sequence([1, 1, 1, 2]).is_restricted_growth_function()
                True

            ::

                >>> Sequence([1, 1, 2, 1]).is_restricted_growth_function()
                True

            ::

                >>> Sequence([1, 1, 2, 2]).is_restricted_growth_function()
                True

        ..  container:: example

            Is false when sequence is not a restricted growth function:

            ::

                >>> Sequence([1, 1, 1, 3]).is_restricted_growth_function()
                False

            ::

                >>> Sequence([17,]).is_restricted_growth_function()
                False

        A restricted growth function is a sequence ``l`` such that
        ``l[0] == 1`` and such that ``l[i] <= max(l[:i]) + 1`` for
        ``1 <= i <= len(l)``.

        Returns true or false.
        '''
        try:
            for i, n in enumerate(self):
                if i == 0:
                    if not n == 1:
                        return False
                else:
                    if not n <= max(self[:i]) + 1:
                        return False
            return True
        except TypeError:
            return False

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     )
                    >>> expression = expression.map(sequence().sum())
                    >>> expression.get_formula_string()
                    'sum(sequence(X)) /@ partition(sequence(X), <3>)'

                ::

                    >>> expression(range(1, 10+1))
                    Sequence([6, 15, 24])

        Returns new sequence.
        '''
        if self._is_frozen:
            formula_string_template = '{expression} /@ {{}}'
            formula_string_template = formula_string_template.format(
                expression=operand.get_formula_string(),
                )
            return self._is_frozen.append_callback(
                evaluation_template='map',
                formula_string_template=formula_string_template,
                map_operand=operand,
                )
        items = [operand(_) for _ in self]
        return type(self)(items=items)

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

                    >>> sequence_ = Sequence(range(16), name='J')
                    >>> sequence_ = sequence_.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )

                ::

                    >>> sequence_
                    Sequence([Sequence([0, 1, 2])], name='partition(J, [3])')

                ::

                    >>> for part in sequence_:
                    ...     part
                    Sequence([0, 1, 2])

            ..  container:: example expression

                ::

                    >>> expression = sequence(name='J')
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [3])'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [4, 3])'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), <3>)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), <4, 3>)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [3]+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [4, 3]+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10, 11, 12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), <3>+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5])
                    Sequence([6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14])
                    Sequence([15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), <4, 3>+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9, 10])
                    Sequence([11, 12, 13])
                    Sequence([14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R[3])'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R[4, 3])'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R<3>)'

                ::
                
                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=False,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R<4, 3>)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R[3]+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
                    Sequence([13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R[4, 3]+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R<3>+)'

                ::

                    >>> for part in expression(range(16)):
                    ...     part
                    Sequence([0])
                    Sequence([1, 2, 3])
                    Sequence([4, 5, 6])
                    Sequence([7, 8, 9])
                    Sequence([10, 11, 12])
                    Sequence([13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [4, 3],
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     reversed_=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), R<4, 3>+)'

                ::

                    >>> for part in parts:
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8])
                    Sequence([9, 10, 11])
                    Sequence([12, 13, 14, 15])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [2, 3, 5],
                    ...     cyclic=False,
                    ...     overhang=Exact,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [2, 3, 5]!)'

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3, 4])
                    Sequence([5, 6, 7, 8, 9])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [2],
                    ...     cyclic=True,
                    ...     overhang=Exact,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), <2>!)'

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1])
                    Sequence([2, 3])
                    Sequence([4, 5])
                    Sequence([6, 7])
                    Sequence([8, 9])

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

                    >>> expression = sequence()
                    >>> expression = expression.partition_by_counts(
                    ...     [3],
                    ...     cyclic=False,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'partition(sequence(X), [3]+)'

                ::

                    >>> for part in expression('some text'):
                    ...     part
                    Sequence(['s', 'o', 'm'])
                    Sequence(['e', ' ', 't', 'e', 'x', 't'])

        Returns nested sequence.
        '''
        from abjad.tools import sequencetools
        indicator = self._make_partition_indicator(
            counts=counts,
            cyclic=cyclic,
            reversed_=reversed_,
            overhang=overhang,
            )
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                string_arguments=indicator,
                string_name='partition',
                )
        items = self._items[:]
        subsequences = []
        parts = sequencetools.partition_sequence_by_counts(
            items,
            counts,
            cyclic=cyclic,
            overhang=overhang,
            reversed_=reversed_,
            )
        parts = [type(self)(_) for _ in parts]
        result = type(self)(items=parts, name=self._name)
        formula_markup_expression = expressiontools.Expression()
        formula_markup_expression = formula_markup_expression.append_callback(
            'Markup({})')
        template = "Markup.concat(['P', Markup({indicator!r}).super_(), {{}}])"
        template = template.format(indicator=indicator)
        formula_markup_expression = formula_markup_expression.append_callback(
            template)
        formula_string_template = 'partition({{}}, {indicator})'
        formula_string_template = formula_string_template.format(
            indicator=indicator,
            )
        expressiontools.Expression._track_expression(
            self,
            result,
            'partition',
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            )
        return result

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

                    >>> expression = sequence()
                    >>> ratio = mathtools.Ratio((1, 1, 1))
                    >>> expression = expression.partition_by_ratio_of_lengths(ratio)
                    >>> expression.get_formula_string()
                    'partition(sequence(X), 1:1:1)'

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4, 5, 6])
                    Sequence([7, 8, 9])

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

                    >>> expression = sequence()
                    >>> ratio = mathtools.Ratio((1, 1, 2))
                    >>> expression = expression.partition_by_ratio_of_lengths(ratio)
                    >>> expression.get_formula_string()
                    'partition(sequence(X), 1:1:2)'

                ::

                    >>> for part in expression(range(10)):
                    ...     part
                    Sequence([0, 1, 2])
                    Sequence([3, 4])
                    Sequence([5, 6, 7, 8, 9])

        Returns a sequence of sequences.
        '''
        from abjad.tools import sequencetools
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                string_arguments=str(ratio),
                string_name='partition',
                )
        parts = sequencetools.partition_sequence_by_ratio_of_lengths(
            self.items,
            ratio=ratio,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(parts)

    def reverse(self):
        '''Reverses sequence.

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence([1, 2, 3, 4, 5], name='J')
                    
                ::

                    >>> sequence_.reverse()
                    Sequence([5, 4, 3, 2, 1], name='R(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence()
                    >>> expression = expression.reverse()
                    >>> expression.get_formula_string()
                    'R(sequence(X))'

                ::

                    >>> expression([1, 2, 3, 4, 5])
                    Sequence([5, 4, 3, 2, 1])

        ..  container:: example

            Reverses sequence:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence('text', name='J')
                    
                ::
                
                    >>> sequence_.reverse()
                    Sequence(['t', 'x', 'e', 't'], name='R(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence()
                    >>> expression = expression.reverse()
                    >>> expression.get_formula_string()
                    'R(sequence(X))'

                ::

                    >>> expression('text')
                    Sequence(['t', 'x', 'e', 't'])

        Returns new sequence.
        '''
        formula_markup_expression = expressiontools.Expression()
        formula_markup_expression = formula_markup_expression.append_callback(
            'Markup({})',
            )
        formula_markup_expression = formula_markup_expression.append_callback(
            "Markup.concat(['R', {}])",
            )
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                formula_markup_expression=formula_markup_expression,
                string_name='R',
                )
        result = type(self)(reversed(self), name=self._name)
        formula_string_template = 'R({})'
        expressiontools.Expression._track_expression(
            self,
            result,
            'retrograde',
            formula_markup_expression=formula_markup_expression,
            formula_string_template=formula_string_template,
            )
        return result

    def rotate(self, n=None):
        '''Rotates sequence by index `n`.

        ..  container:: example

            Rotates sequence to the right:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10), name='J')
                    
                ::
                
                    >>> sequence_.rotate(n=4)
                    Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5], name='r4(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence()
                    >>> expression = expression.rotate(n=4)
                    >>> expression.get_formula_string()
                    'r4(sequence(X))'

                ::

                    >>> expression(range(10))
                    Sequence([6, 7, 8, 9, 0, 1, 2, 3, 4, 5])

        ..  container:: example

            Rotates sequence to the left:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10), name='J')
                    
                ::
                
                    >>> sequence_.rotate(n=-3)
                    Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2], name='r-3(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence()
                    >>> expression = expression.rotate(n=-3)
                    >>> expression.get_formula_string()
                    'r-3(sequence(X))'

                ::

                    >>> expression(range(10))
                    Sequence([3, 4, 5, 6, 7, 8, 9, 0, 1, 2])

        ..  container:: example

            Rotates sequence neither to the right nor the left:

            ..  container:: example

                ::

                    >>> sequence_ = Sequence(range(10), name='J')

                ::

                    >>> sequence_.rotate(n=0)
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], name='r0(J)')

            ..  container:: example expression

                ::

                    >>> expression = sequence()
                    >>> expression = expression.rotate(n=0)
                    >>> expression.get_formula_string()
                    'r0(sequence(X))'

                ::

                    >>> expression(range(10))
                    Sequence([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        Returns new sequence.
        '''
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                formula_string_template='r{n}({{}})'.format(n=n),
                )
        n = n or 0
        original_n = n
        items = []
        if len(self):
            n = n % len(self)
            for item in self[-n:len(self)] + self[:-n]:
                items.append(item)
        name = None
        if self.name:
            formula_string_template = 'r{n}({sequence})'
            name = formula_string_template.format(
                sequence=self.name,
                n=original_n,
                )
        return type(self)(items=items, name=name)

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

                    >>> expression = sequence()
                    >>> expression = expression.split(
                    ...     (3, 15, 3),
                    ...     cyclic=True,
                    ...     overhang=True,
                    ...     )
                    >>> expression.get_formula_string()
                    'S(sequence(X), <3, 15, 3>+)'

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

        Returns new sequence.
        '''
        from abjad.tools import sequencetools
        if self._is_frozen:
            indicator = self._make_split_indicator(weights, cyclic, overhang)
            return self._make_callback(
                inspect.currentframe(),
                string_arguments=indicator,
                string_name='S',
                )
        parts = sequencetools.split_sequence(
            self.items,
            weights,
            cyclic=cyclic,
            overhang=overhang,
            )
        parts = [type(self)(_) for _ in parts]
        return type(self)(parts)

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

                    >>> expression = sequence()
                    >>> expression = expression.sum()
                    >>> expression.get_formula_string()
                    'sum(sequence(X))'

                ::

                    >>> expression([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                    55

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

                    >>> expression = sequence()
                    >>> expression = expression.sum()
                    >>> expression.get_formula_string()
                    'sum(sequence(X))'

                ::

                    >>> expression([-1, 2, -3, 4, -5, 6, -7, 8, -9, 10])
                    5

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

                    >>> expression = sequence()
                    >>> expression = expression.sum()
                    >>> expression = expression.sequence()
                    >>> expression.get_formula_string()
                    'sequence(sum(sequence(X)))'

                ::

                    >>> expression(range(1, 10+1))
                    Sequence([55])

        Returns new sequence.
        '''
        if self._is_frozen:
            return self._make_callback(
                inspect.currentframe(),
                string_name='sum',
                )
        return sum(self)


collections.Sequence.register(Sequence)
