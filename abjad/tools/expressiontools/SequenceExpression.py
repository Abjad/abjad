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

            >>> expression()
            Sequence(())

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, [3, [4]], 5))
            
    ..  container:: example

        **Example 2.** Makes expression to flatten sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, 3, 4, 5))

    ..  container:: example

        **Example 3.** Makes expression ot reverse sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, [3, [4]], 2, 1))

    ..  container:: example

        **Example 4.** Makes expression to flatten and reverse sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, 4, 3, 2, 1))

    ..  container:: example

        **Example 5.** Makes expression to reverse and flatten sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, 3, 4, 2, 1))

    ..  container:: example

        **Example 6.** Makes expression to get item from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[-1]

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

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5,))

    ..  container:: example

        **Example 8.** Makes expression to get slice from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, [3, [4]]))

    ..  container:: example

        **Example 9.** Makes expression to get slice from sequence and flatten
        slice:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, 3, 4))

    ..  container:: example

        **Example 10.** Makes expression to add ``[4, 5]`` to sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.__add__([4, 5])

        ::

            >>> expression([1, 2, 3])
            Sequence((1, 2, 3, 4, 5))

    ..  container:: example

        **Example 11.** Makes expression to partition sequence into thirds and
        get middle third:

        ::

            >>> expression = sequence()
            >>> ratio = mathtools.Ratio((1, 1, 1))
            >>> expression = expression.partition_by_ratio_of_lengths(ratio)
            >>> expression = expression[1]

        ::

            >>> expression(range(1, 10+1))
            Sequence((4, 5, 6, 7))

    ..  container:: example

        **Example 12.** Makes expression to partition sequence into parts with
        lengths equal to three:

        ::

            >>> expression = sequence()
            >>> expression = expression.partition_by_counts([3], cyclic=True)

        ::

            >>> expression(range(1, 10+1))
            Sequence((Sequence((1, 2, 3)), Sequence((4, 5, 6)), Sequence((7, 8, 9))))

    ..  container:: example

        **Example 13.** Makes expression to partition sequence and sum parts:

        ::

            >>> expression = sequence()
            >>> expression = expression.partition_by_counts([3], cyclic=True)
            >>> expression = expression.map().sum()

        ::

            >>> expression(range(1, 10+1))
            Sequence((6, 15, 24))

    ..  container:: example

        **Example 14.** Makes expression to sum sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.sum()

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

            >>> expression(range(1, 10+1))
            Sequence((55,))

    ..  container:: example

        **Example 16.** Makes expression to split sequence by weights:

        ::

            >>> expression = sequence()
            >>> expression = expression.split([10], cyclic=True)
            >>> expression = expression.sequence()

        ::

            >>> expression(range(1, 10+1))
            Sequence((Sequence((1, 2, 3, 4)), Sequence((5, 5)), Sequence((1, 7, 2)), Sequence((6, 4)), Sequence((5, 5))))

    ..  container:: example

        **Example 17.** Makes expression to rotate sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.rotate(-1)

        ::

            >>> expression(range(1, 10+1))
            Sequence((2, 3, 4, 5, 6, 7, 8, 9, 10, 1))

    ..  note:: Aadd usage examples to this docstring. Do not add
        usage examples to property and method docstrings. Properties
        and methods will all be derived automatically from the Sequence class
        at some point in future.

    Initializer returns expression.

    Expression returns object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        superclass = super(SequenceExpression, self)
        superclass.__init__(callbacks=callbacks)
        self._client_class = sequencetools.Sequence

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Makes add callback.

        Returns callback.
        '''
        arguments={
            'expr': expr,
            }
        return self._make_callback('Sequence.__add__', arguments)

    def __call__(self, items=None):
        r'''Calls sequence expression on `items`.

        Makes sequence from `items`.

        Then applies callbacks to sequence.

        Returns sequence.
        '''
        from abjad.tools import sequencetools
        if items is None:
            #result = sequencetools.Sequence()
            result = self._client_class()
        else:
            #result = sequencetools.Sequence(items)
            result = self._client_class(items)
        callbacks = self.callbacks or ()
        map_next = False
        for callback in callbacks:
            if callback.name == 'Sequence.__init__':
                result = sequencetools.Sequence(result)
                map_next = False
            elif callback.name == 'map':
                map_next = True
            else:
                if map_next:
                    class_ = type(result)
                    result = class_([callback(_) for _ in result])
                else:
                    result = callback(result)
                map_next = False
        return result

    def __format__(self, format_specification=''):
        r'''Formats sequence expression.

        ..  container:: example

            **Example 1.** Gets storage format:

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
                            name='Sequence.reverse',
                            ),
                        expressiontools.Callback(
                            name='Sequence.flatten',
                            arguments=[
                                ('classes', None),
                                ('depth', -1),
                                ('indices', None),
                                ],
                            ),
                        expressiontools.Callback(
                            name='Sequence.__getitem__',
                            arguments=[
                                (
                                    'i',
                                    slice(None, -3, None),
                                    ),
                                ],
                            ),
                        expressiontools.Callback(
                            name='Sequence.__getitem__',
                            arguments=[
                                ('i', 0),
                                ],
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
        return self._make_callback('Sequence.__getitem__', arguments)

    def __radd__(self, expr):
        r'''Makes right-add callback.

        Returns callback.
        '''
        arguments={
            'expr': expr,
            }
        return self._make_callback('Sequence.__radd__', arguments)

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
        return self._make_callback('Sequence.flatten', arguments)

    def map(self):
        r'''Makes map callback.

        Returns callback.
        '''
        return self._make_callback('map')

    def partition_by_counts(self, counts, cyclic=False, overhang=False):
        r'''Makes partition-by-counts callback.

        Returns callback.
        '''
        arguments={
            'counts': counts,
            'cyclic': cyclic,
            'overhang': overhang,
            }
        return self._make_callback('Sequence.partition_by_counts', arguments)

    def partition_by_ratio_of_lengths(self, ratio):
        r'''Makes partition-by-ratio-of-lengths callback.

        Returns callback.
        '''
        name = 'Sequence.partition_by_ratio_of_lengths'
        arguments={
            'ratio': ratio,
            }
        return self._make_callback(name, arguments)

    def reverse(self):
        r'''Makes reverse callback.

        Returns callback.
        '''
        return self._make_callback('Sequence.reverse')

    def rotate(self, index=None):
        r'''Makes rotate callback.

        Returns callback.
        '''
        arguments = {
            'index': index,
            }
        return self._make_callback('Sequence.rotate', arguments)

    def sequence(self):
        r'''Makes sequence callback.

        Returns callback.
        '''
        return self._make_callback('Sequence.__init__')

    def split(self, weights, cyclic=False, overhang=False):
        r'''Makes split callback.

        Returns callback.
        '''
        arguments = {
            'weights': weights,
            'cyclic': cyclic,
            'overhang': overhang,
            }
        return self._make_callback('Sequence.split', arguments)

    def sum(self):
        r'''Makes sum callback.

        Returns callback.
        '''
        return self._make_callback('Sequence.sum')
