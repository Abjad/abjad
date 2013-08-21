# -*- encoding: utf-8 -*-


def mutate(expr):
    r'''Mutate `expr`.

    Returns mutator.
    '''
    from abjad.tools import componenttools
    from abjad.tools import mutationtools
    assert isinstance(expr, componenttools.Component)
    return mutationtools.Mutator(expr)
