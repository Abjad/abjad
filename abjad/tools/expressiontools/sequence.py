# -*- coding: utf-8 -*-


def sequence():
    r'''Makes sequence expression.

    ..  container:: example

        **Example 1.** Flattens and reverses sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()

        ::

            >>> print(format(expression))
            expressiontools.SequenceExpression(
                callbacks=(
                    expressiontools.Callback(
                        name='Sequence.flatten',
                        keywords=[
                            ('classes', None),
                            ('depth', -1),
                            ('indices', None),
                            ],
                        ),
                    expressiontools.Callback(
                        name='Sequence.reverse',
                        ),
                    ),
                )

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((5, 4, 3, 2, 1))

    ..  container:: example

        **Example 2.** Flattens, reverses and slices sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()
            >>> expression = expression[-3:]

        ::

            >>> print(format(expression))
            expressiontools.SequenceExpression(
                callbacks=(
                    expressiontools.Callback(
                        name='Sequence.flatten',
                        keywords=[
                            ('classes', None),
                            ('depth', -1),
                            ('indices', None),
                            ],
                        ),
                    expressiontools.Callback(
                        name='Sequence.reverse',
                        ),
                    expressiontools.Callback(
                        name='Sequence.__getitem__',
                        arguments=datastructuretools.TypedTuple(
                            (
                                slice(-3, None, None),
                                )
                            ),
                        ),
                    ),
                )

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((3, 2, 1))

    Returns sequence expression.
    '''
    from abjad.tools import expressiontools
    return expressiontools.SequenceExpression()