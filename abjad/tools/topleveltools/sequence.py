# -*- coding: utf-8 -*-


def sequence(items=None, **keywords):
    r'''Makes sequence or sequence expression.

    ..  container:: example

        ..  container:: example

            Makes sequence:

            ::

                >>> sequence([1, 2, [3, [4]], 5])
                Sequence([1, 2, [3, [4]], 5])

        ..  container:: example expression

            Makes sequence expression:

            ::

                >>> expression = sequence()
                >>> expression([1, 2, [3, [4]], 5])
                Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Flattens, reverses and slices sequence:

        ..  container:: example

            ::

                >>> sequence_ = sequence([1, 2, [3, [4]], 5])
                >>> sequence_
                Sequence([1, 2, [3, [4]], 5])

            ::

                >>> sequence_ = sequence_.flatten()
                >>> sequence_
                Sequence([1, 2, 3, 4, 5])

            ::

                >>> sequence_ = sequence_.reverse()
                >>> sequence_
                Sequence([5, 4, 3, 2, 1])

            ::

                >>> sequence_ = sequence_[-3:]
                >>> sequence_
                Sequence([3, 2, 1])

        ..  container:: example expression

            ::

                >>> expression = sequence()
                >>> expression = sequence()
                >>> expression = expression.flatten()
                >>> expression = expression.reverse()
                >>> expression = expression[-3:]
                >>> expression([1, 2, [3, [4]], 5])
                Sequence([3, 2, 1])
        
    Returns sequence when `items` is not none.

    Returns sequence expression when `items` is none.
    '''
    from abjad.tools import expressiontools
    from abjad.tools import sequencetools
    if items:
        return sequencetools.Sequence(items=items, **keywords)
    else:
        expression = expressiontools.Expression()
        expression = expression.sequence(**keywords)
        return expression
