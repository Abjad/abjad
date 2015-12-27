# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class SequenceExpression(AbjadObject):
    r'''A sequence expression.

    ..  container:: example

        **Example 1.** Initializes sequence:

        ::

            >>> expression = sequence()

        ::

            >>> expression()
            Sequence(())

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, [3, [4]], 5))
            
    ..  container:: example

        **Example 2.** Flattens sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, 3, 4, 5))

    ..  container:: example

        **Example 3.** Reverses sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, [3, [4]], 2, 1))

    ..  container:: example

        **Example 4.** Flattens and reverses sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, 4, 3, 2, 1))

    ..  container:: example

        **Example 5.** Reverses and flattens sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.reverse()
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, 3, 4, 2, 1))

    ..  container:: example

        **Example 6.** Gets item from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[-1]

        ::

            >>> expression([1, 2, [3, [4]], 5])
            5

    ..  container:: example

        **Example 7.** Gets slice from sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, [3, [4]]))

    ..  container:: example

        **Example 8.** Gets slice from sequence and flattens slice:

        ::

            >>> expression = sequence()
            >>> expression = expression[:-1]
            >>> expression = expression.flatten()

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((1, 2, 3, 4))

    ..  container:: example

        **Example 9.** Adds sequence to sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.__add__([4, 5])

        ::

            >>> expression([1, 2, 3])
            Sequence((1, 2, 3, 4, 5))

    ..  container:: example

        **Example 10.** Partitions sequence and gets middle part:

        ::

            >>> expression = sequence()
            >>> ratio = mathtools.Ratio((1, 1, 1))
            >>> expression = expression.partition_by_ratio_of_lengths(ratio)
            >>> expression = expression[1]

        ::

            >>> expression(range(10))
            Sequence((3, 4, 5, 6))

    ..  container:: example

        **Example 11.** Gets storage format:

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
                        keywords=[
                            ('classes', None),
                            ('depth', -1),
                            ('indices', None),
                            ],
                        ),
                    expressiontools.Callback(
                        name='Sequence.__getitem__',
                        keywords=[
                            (
                                'i',
                                slice(None, -3, None),
                                ),
                            ],
                        ),
                    expressiontools.Callback(
                        name='Sequence.__getitem__',
                        keywords=[
                            ('i', 0),
                            ],
                        ),
                    ),
                )

    Initializer returns expression.

    Call returns object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Expressions'

    __slots__ = (
        '_callbacks',
        )

    ### INITIALIZER ###

    def __init__(self, callbacks=None):
        if callbacks is not None:
            callbacks = tuple(callbacks)
        self._callbacks = callbacks

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Adds `expr` to sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.__add__',
            keywords={
                'expr': expr,
                },
            )
        return self._append_callback(callback)

    def __call__(self, items=None):
        r'''Calls sequence expression on `items`.

        Makes sequence from `items`.

        Then applies callbacks to sequence.

        Returns sequence.
        '''
        from abjad.tools import sequencetools
        if items is None:
            sequence = sequencetools.Sequence()
        else:
            sequence = sequencetools.Sequence(items)
        callbacks = self.callbacks or ()
        for callback in callbacks:
            sequence = callback(sequence)
        return sequence

    def __getitem__(self, i):
        r'''Gets item `i` from sequence.

        Returns item.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.__getitem__',
            keywords={
                'i': i,
                },
            )
        return self._append_callback(callback)

    def __radd__(self, expr):
        r'''Adds sequence to `expr`.

        Returns new sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.__radd__',
            keywords={
                'expr': expr,
                }
            )
        return self._append_callback(callback)

    ### PRIVATE METHODS ###

    def _append_callback(self, callback):
        callbacks = self.callbacks or ()
        callbacks = callbacks + (callback,)
        return type(self)(callbacks)
        
    ### PUBLIC PROPERTIES ###

    @property
    def callbacks(self):
        r'''Gets callbacks of selector.

        Returns tuple or none.
        '''
        return self._callbacks

    ### PUBLIC METHODS ###

    def flatten(self, classes=None, depth=-1, indices=None):
        r'''Flattens sequence.

        Returns new sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.flatten',
            keywords={
                'classes': classes,
                'depth': depth,
                'indices': indices,
                }
            )
        return self._append_callback(callback)

    def partition_by_ratio_of_lengths(self, ratio):
        r'''Partitions sequence by `ratio` of lengths.

        Returns new sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.partition_by_ratio_of_lengths',
            keywords={
                'ratio': ratio,
                },
            )
        return self._append_callback(callback)

    def reverse(self):
        r'''Reverses sequence.

        Returns new sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.reverse',
            )
        return self._append_callback(callback)

    def rotate(self):
        r'''Rotates sequence.

        Returns new sequence.
        '''
        from abjad.tools import expressiontools
        callback = expressiontools.Callback(
            name='Sequence.rotate',
            )
        return self._append_callback(callback)