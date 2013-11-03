# -*- encoding: utf-8 -*-


def mutate(expr):
    r'''Mutates `expr`.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> notes = staff[-2:]
            >>> mutate(notes)
            ScoreMutationAgent(SliceSelection(Note("d'4"), Note("f'4")))

    Returns score mutation agent.
    '''
    from abjad.tools import mutationtools
    return mutationtools.ScoreMutationAgent(expr)
