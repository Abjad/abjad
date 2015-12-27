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
                        keywords=[
                            (
                                'i',
                                slice(-3, None, None),
                                ),
                            ],
                        ),
                    ),
                )

        Works with numbers:

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence((3, 2, 1))

        Works with divisions:

        ::

            >>> divisions = [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8)]
            >>> divisions = [durationtools.Division(_) for _ in divisions]
            >>> expression(divisions)
            Sequence((Division((3, 8)), Division((2, 8)), Division((1, 8))))

        The example with divisions shows that the input argument need not be
        available in the Abjad global namespace.

    Returns sequence expression.
    '''
    from abjad.tools import expressiontools
    return expressiontools.SequenceExpression()