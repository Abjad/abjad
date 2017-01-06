# -*- coding: utf-8 -*-


def sequence(expr=None, name=None):
    r'''Makes sequence or sequence expression.

    ..  container:: example

        Makes sequence:

        ::

            >>> sequence([1, 2, [3, [4]], 5])
            Sequence([1, 2, [3, [4]], 5])

    ..  container:: example

        Flattens, reverses and slices sequence:

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

    ..  container:: example

        Makes sequence expression:

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

    ..  container:: example

        Makes expression to flatten, reverse and slice sequence:

        ::

            >>> expression = sequence()
            >>> expression = expression.flatten()
            >>> expression = expression.reverse()
            >>> expression = expression[-3:]

        ::

            >>> f(expression)
            expressiontools.Expression(
                callbacks=(
                    expressiontools.Expression(
                        evaluation_template='Sequence(items={})',
                        formula_string_template='sequence({})',
                        ),
                    expressiontools.Expression(
                        evaluation_template='{}.flatten()',
                        formula_string_template='flatten({})',
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
                    expressiontools.Expression(
                        evaluation_template='{}.__getitem__(i=slice(-3, None, None))',
                        formula_string_template='{}[-3:]',
                        ),
                    ),
                )
        
        Works with numbers:

        ::

            >>> expression([1, 2, [3, [4]], 5])
            Sequence([3, 2, 1])

        Works with divisions:

        ::

            >>> divisions = [(1, 8), (2, 8), (3, 8), (4, 8), (5, 8)]
            >>> divisions = [durationtools.Division(_) for _ in divisions]
            >>> expression(divisions)
            Sequence([Division((3, 8)), Division((2, 8)), Division((1, 8))])

        Input argument to expression need not be available in Abjad global
        namespace.

    Returns sequence when `expr` is not none.

    Returns sequence expression when `expr` is none.
    '''
    from abjad.tools import expressiontools
    from abjad.tools import sequencetools
    if expr is None:
        expression = expressiontools.Expression()
        expression = expression.sequence(name=name)
        return expression
    else:
        return sequencetools.Sequence(expr, name=name)
