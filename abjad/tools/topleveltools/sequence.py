# -*- coding: utf-8 -*-


def sequence(expr=None):
    r'''Makes sequence or sequence expression.

    ..  container:: example

        **Example 1.** Makes sequence:

        ::

            >>> sequence([1, 2, [3, [4]], 5])
            Sequence((1, 2, [3, [4]], 5))

    ..  container:: example

        **Example 2.** Flattens, reverses and slices sequence:

        ::

            >>> sequence_ = sequence([1, 2, [3, [4]], 5])
            >>> sequence_
            Sequence((1, 2, [3, [4]], 5))

        ::

            >>> sequence_ = sequence_.flatten()
            >>> sequence_
            Sequence((1, 2, 3, 4, 5))

        ::

            >>> sequence_ = sequence_.reverse()
            >>> sequence_
            Sequence((5, 4, 3, 2, 1))

        ::

            >>> sequence_ = sequence_[-3:]
            >>> sequence_
            Sequence((3, 2, 1))

    ..  container:: example

        **Example 3.** Makes sequence expression:

        ::

            >>> sequence()
            SequenceExpression()

    ..  container:: example

        **Example 4.** Makes expression to flatten, reverse and slice sequence:

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
                        arguments=[
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
                        arguments=[
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

        Input argument to expression need not be available in Abjad global
        namespace.

    Returns sequence when `expr` is not none.

    Returns sequence expression when `expr` is none.
    '''
    from abjad.tools import expressiontools
    from abjad.tools import sequencetools
    if expr is None:
        return expressiontools.SequenceExpression()
    else:
        return sequencetools.Sequence(expr)
