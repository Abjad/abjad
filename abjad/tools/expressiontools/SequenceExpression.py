# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.expressiontools.Expression import Expression


class SequenceExpression(Expression):
    r'''Sequence expression.

    ..  container:: example

        **Example 1.** Makes expression to initialize sequence:

        ::

            >>> expression = sequence()

        ::

            >>> str(expression)
            'SequenceExpression()'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])
            
    ..  container:: example

        **Example 2.** Makes expression to flatten sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()

        ::

            >>> expression.get_string()
            'flatten(X)'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, 3, 4, 5])

    ..  container:: example

        **Example 3.** Makes expression to reverse sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()

        ::

            >>> expression.get_string()
            'R(X)'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([5, [3, [4]], 2, 1])

    ..  container:: example

        **Example 4.** Makes expression to flatten and reverse sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()

        ::

            >>> expression.get_string()
            'R(flatten(X))'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([5, 4, 3, 2, 1])

    ..  container:: example

        **Example 5.** Makes expression to reverse and flatten sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()
            >>> expression = expression.flatten()

        ::

            >>> expression.get_string()
            'flatten(R(X))'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([5, 3, 4, 2, 1])

    ..  container:: example

        **Example 6.** Makes expression to get item from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[-1]

        ::
        
            >>> expression.get_string()
            'X[-1]'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            5

    ..  container:: example

        **Example 7.** Makes expression to get item from sequence and wrap
        result in new sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[-1]
            >>> expression = expression.sequence()

        ::

            >>> expression.get_string()
            'sequence(X[-1])'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([5])

    ..  container:: example

        **Example 8.** Makes expression to get slice from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]

        ::

            >>> expression.get_string()
            'X[:-1]'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]]])

    ..  container:: example

        **Example 9.** Makes expression to get slice from sequence and flatten
        slice:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]
            >>> expression = expression.flatten()

        ::

            >>> expression.get_string()
            'flatten(X[:-1])'

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([1, 2, 3, 4])

    ..  container:: example

        **Example 10.** Makes expression to add ``[4, 5]`` to sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression + [4, 5]

        ::
    
            >>> expression.get_string()
            'X + [4, 5]'

        ::

            >>> expression([1, 2, 3])
            Sequence([1, 2, 3, 4, 5])

    ..  container:: example

        **Example 11.** Makes expression to partition sequence into thirds and
        get middle third:

        ::

            >>> expression = sequence()
            >>> ratio = mathtools.Ratio((1, 1, 1))
            >>> expression = expression.partition_by_ratio_of_lengths(ratio)
            >>> expression = expression[1]

        ::

            >>> expression.get_string()
            'partition_ratio(X, 1:1:1)[1]'

        ::

            >>> expression(range(1, 10+1))
            Sequence([4, 5, 6, 7])

    ..  container:: example

        **Example 12.** Makes expression to partition sequence into parts with
        lengths equal to three:

        ::

            >>> expression = sequence()
            >>> expression = expression.partition_by_counts([3], cyclic=True)

        ::

            >>> expression.get_string()
            'partition_cyclic(X, [3])'

        ::

            >>> expression(range(1, 10+1))
            Sequence([Sequence([1, 2, 3]), Sequence([4, 5, 6]), Sequence([7, 8, 9])])

    ..  container:: example

        **Example 13.** Makes expression to partition sequence and sum parts:

        ::

            >>> expression_1 = sequence()
            >>> expression_1 = expression_1.partition_by_counts([3], cyclic=True)
            >>> expression_2 = sequence().sum()
            >>> expression = expression_1.map(expression_2)

        ::

            >>> expression.get_string()
            'sum(X) /@ partition_cyclic(X, [3])'

        ::

            >>> expression(range(1, 10+1))
            Sequence([6, 15, 24])

    ..  container:: example

        **Example 14.** Makes expression to sum sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.sum()

        ::

            >>> expression.get_string()
            'sum(X)'

        ::

            >>> expression(range(10))
            45

    ..  container:: example

        **Example 15.** Makes expression to sum sequence and wrap result in new
        sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.sum()
            >>> expression = expression.sequence()

        ::

            >>> expression.get_string()
            'sequence(sum(X))'

        ::

            >>> expression(range(1, 10+1))
            Sequence([55])

    ..  container:: example

        **Example 16.** Makes expression to split sequence by weights:

        ::

            >>> expression = sequence()
            >>> expression = expression.split([10], cyclic=True)
            >>> expression = expression.sequence()

        ::

            >>> expression.get_string()
            'sequence(split_cyclic(X, [10]))'

        ::

            >>> expression(range(1, 10+1))
            Sequence([Sequence([1, 2, 3, 4]), Sequence([5, 5]), Sequence([1, 7, 2]), Sequence([6, 4]), Sequence([5, 5])])

    ..  container:: example

        **Example 17.** Makes expression to rotate sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.rotate(-1)

        ::

            >>> expression.get_string()
            'r-1(X)'

        ::

            >>> expression(range(1, 10+1))
            Sequence([2, 3, 4, 5, 6, 7, 8, 9, 10, 1])

    ..  note:: Add usage examples to this docstring. Do not add
        usage examples to property and method docstrings. Properties
        and methods will all be derived automatically from the Sequence class
        at some point in future.

    Initializer returns expression.

    Expression returns object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __add__(self, sequence_=None):
        r'''Makes add callback.

        Returns callback.
        '''
        arguments={
            'sequence_': sequence_,
            }
        string_expression = '{{}} + {}'
        if hasattr(sequence_, 'name'):
            string_expression = string_expression.format(sequence_.name)
        else:
            string_expression = string_expression.format(sequence_)
        return self.make_callback(
            'Sequence.__add__',
            arguments=arguments,
            string_expression=string_expression,
            )

    def __call__(self, items=None):
        r'''Calls sequence expression on `items`.

        Makes sequence from `items`.

        Then applies callbacks to sequence.

        Returns sequence.
        '''
        from abjad.tools import sequencetools
        if items is None:
            result = sequencetools.Sequence()
        else:
            result = sequencetools.Sequence(items=items)
        callbacks = self.callbacks or []
        for callback in callbacks:
            if callback.template == 'Sequence.__init__':
                result = sequencetools.Sequence(result)
            elif not callback.template == 'map':
                result = callback(result)
            else:
                key, sequence_expression = callback.arguments[0]
                assert key == 'expression'
                assert isinstance(sequence_expression, type(self))
                class_ = type(result)
                result = class_([sequence_expression(_) for _ in result])
        return result

    def __format__(self, format_specification=''):
        r'''Formats sequence expression.

        ..  container:: example

            Gets storage format:

            ::

                >>> expression = sequence()
                >>> expression = expression.reverse()
                >>> expression = expression.flatten()
                >>> expression = expression[:-3]
                >>> expression = expression[0]

            ::

                >>> print(format(expression))
                expressiontools.SequenceExpression(
                    callbacks=(
                        expressiontools.Callback(
                            'Sequence.reverse',
                            string_expression='R({})',
                            ),
                        expressiontools.Callback(
                            'Sequence.flatten',
                            arguments=[
                                ('classes', None),
                                ('depth', -1),
                                ('indices', None),
                                ],
                            string_expression='flatten({})',
                            ),
                        expressiontools.Callback(
                            'Sequence.__getitem__',
                            arguments=[
                                (
                                    'i',
                                    slice(None, -3, None),
                                    ),
                                ],
                            string_expression='{}[:-3]',
                            ),
                        expressiontools.Callback(
                            'Sequence.__getitem__',
                            arguments=[
                                ('i', 0),
                                ],
                            string_expression='{}[0]',
                            ),
                        ),
                    )

        Returns string.
        '''
        superclass = super(SequenceExpression, self)
        return superclass.__format__(
            format_specification=format_specification,
            )

    def __getitem__(self, i):
        r'''Makes get-item callback.

        Returns callback.
        '''
        arguments={
            'i': i,
            }
        if isinstance(i, int):
            string_expression = '{{}}[{i}]'
            start = stop = step = None
        elif isinstance(i, slice):
            if i.step is not None:
                raise NotImplementedError
            if i.start is None and i.stop is None:
                string_expression = '{{}}[:]'
            elif i.start is None:
                string_expression = '{{}}[:{stop}]'
            elif i.stop is None:
                string_expression = '{{}}[{start}:]'
            else:
                string_expression = '{{}}[{start}:{stop}]'
            start = i.start
            stop = i.stop
            step = i.step
        else:
            message = 'must be integer or slice: {!r}.'
            message = message.format(i)
            raise TypeError(message)
        string_expression = string_expression.format(
            i=i,
            start=start,
            stop=stop,
            step=step,
            )
        return self.make_callback(
            'Sequence.__getitem__',
            arguments=arguments,
            string_expression=string_expression,
            )

    def __radd__(self, sequence_):
        r'''Makes right-add callback.

        Returns callback.
        '''
        arguments={
            'sequence_': sequence_,
            }
        string_expression= '{} + {{}}'.format(sequence_.name)
        return self.make_callback(
            'Sequence.__radd__',
            arguments=arguments,
            string_expression=string_expression,
            )

    ### PUBLIC METHODS ###

    def flatten(self, classes=None, depth=-1, indices=None):
        r'''Makes flatten callback.

        Returns callback.
        '''
        arguments = {
            'classes': classes,
            'depth': depth,
            'indices': indices,
            }
        string_expression = 'flatten({}'
        if classes is not None:
            string_expression += ', classes={}'.format(classes)
        if depth is not -1:
            string_expression += ', depth={}'.format(depth)
        if indices is not None:
            string_expression += ', indices={}'.format(indices)
        string_expression += ')'
        return self.make_callback(
            'Sequence.flatten',
            arguments=arguments,
            string_expression=string_expression,
            )

    def map(self, expression):
        r'''Makes map callback.

        Returns callback.
        '''
        arguments = {
            'expression': expression,
            }
        string_expression = '{expression} /@ {{}}'
        string_expression = string_expression.format(
            expression=expression.get_string(),
            )
        return self.make_callback(
            'map',
            arguments=arguments,
            string_expression=string_expression,
            )

    def partition_by_counts(
        self,
        counts,
        cyclic=False,
        overhang=False,
        reversed_=False,
        ):
        r'''Makes partition-by-counts callback.

        Returns callback.
        '''
        arguments={
            'counts': counts,
            'cyclic': cyclic,
            'overhang': overhang,
            'reversed_': reversed_,
            }
        if not cyclic and not overhang:
            string_expression = 'partition({{}}, {counts})'
        elif cyclic:
            string_expression = 'partition_cyclic({{}}, {counts})'
        elif overhang:
            string_expression = 'partition_overhang({{}}, {counts})'
        else:
            string_expression = 'partition_cyclic_overhang({{}}, {counts})'
        string_expression = string_expression.format(counts=counts)
        return self.make_callback(
            'Sequence.partition_by_counts',
            arguments=arguments,
            string_expression=string_expression,
            )

    def partition_by_ratio_of_lengths(self, ratio):
        r'''Makes partition-by-ratio-of-lengths callback.

        Returns callback.
        '''
        template = 'Sequence.partition_by_ratio_of_lengths'
        arguments={
            'ratio': ratio,
            }
        string_expression = 'partition_ratio({{}}, {ratio!s})'
        string_expression = string_expression.format(ratio=ratio)
        return self.make_callback(
            template,
            arguments=arguments,
            string_expression=string_expression,
            )

    def reverse(self):
        r'''Makes reverse callback.

        Returns callback.
        '''
        string_expression = 'R({})'
        return self.make_callback(
            'Sequence.reverse',
            string_expression=string_expression,
            )

    def rotate(self, n=None):
        r'''Makes rotate callback.

        Returns callback.
        '''
        arguments = {
            'n': n,
            }
        string_expression = 'r{n}({{}})'
        string_expression = string_expression.format(n=n)
        return self.make_callback(
            'Sequence.rotate',
            arguments=arguments,
            string_expression=string_expression,
            )

    def sequence(self):
        r'''Makes sequence callback.

        Returns callback.
        '''
        string_expression = 'sequence({})'
        return self.make_callback(
            'Sequence.__init__',
            string_expression=string_expression,
            )

    def split(self, weights, cyclic=False, overhang=False):
        r'''Makes split callback.

        Returns callback.
        '''
        arguments = {
            'weights': weights,
            'cyclic': cyclic,
            'overhang': overhang,
            }
        if not cyclic and not overhang:
            string_expression = 'split({{}}, {weights})'
        elif cyclic:
            string_expression = 'split_cyclic({{}}, {weights})'
        elif overhang:
            string_expression = 'split_overhang({{}}, {weights})'
        else:
            string_expression = 'split_cyclic_overhang({{}}, {weights})'
        string_expression = string_expression.format(weights=weights)
        return self.make_callback(
            'Sequence.split',
            arguments=arguments,
            string_expression=string_expression,
            )

    def sum(self):
        r'''Makes sum callback.

        Returns callback.
        '''
        string_expression = 'sum({})'
        return self.make_callback(
            'Sequence.sum',
            string_expression=string_expression,
            )
