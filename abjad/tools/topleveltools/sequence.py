# -*- coding: utf-8 -*-


def sequence(items=None, **keywords):
    r'''Makes sequence or sequence expression.

    ::

        >>> import abjad

    ..  container:: example

        ..  container:: example

            Makes sequence:

            ::

                >>> abjad.sequence([1, 2, [3, [4]], 5])
                Sequence([1, 2, [3, [4]], 5])

        ..  container:: example expression

            Makes sequence expression:

            ::

                >>> expression = abjad.sequence()
                >>> expression([1, 2, [3, [4]], 5])
                Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Flattens, reverses and slices sequence:

        ..  container:: example

            ::

                >>> sequence_ = abjad.sequence([1, 2, [3, [4]], 5])
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

                >>> expression = abjad.sequence()
                >>> expression = expression.flatten()
                >>> expression = expression.reverse()
                >>> expression = expression[-3:]
                >>> expression([1, 2, [3, [4]], 5])
                Sequence([3, 2, 1])
        
    Returns sequence when `items` is not none.

    Returns sequence expression when `items` is none.
    '''
    from abjad.tools import datastructuretools
    from abjad.tools import expressiontools
    if items:
        return datastructuretools.Sequence(items=items, **keywords)
    else:
        expression = expressiontools.Expression()
        expression = expression.sequence(**keywords)
        return expression
