# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.handlertools.Handler import Handler


class StemTremoloHandler(Handler):
    r'''Stem tremolo handler.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_hash_mark_counts',
        )

    ### INITIALIZER ###

    def __init__(self, hash_mark_counts=None):
        if hash_mark_counts is not None:
            hash_mark_counts = tuple(hash_mark_counts)
            assert mathtools.all_are_nonnegative_integers(hash_mark_counts)
        self._hash_mark_counts = hash_mark_counts

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls handler on `expr`.

        Returns none.
        '''
        classes = (scoretools.Note, scoretools.Chord)
        hash_mark_counts = datastructuretools.CyclicTuple(
            self.hash_mark_counts)
        for i, leaf in enumerate(
            scoretools.iterate_components_forward_in_expr(expr, classes)):
            indicatortools.StemTremolo(hash_mark_counts[i])(leaf)

    ### PUBLIC PROPERTIES ###

    @property
    def hash_mark_counts(self):
        r'''Gets hash mark counts of handler.

        Returns tuple of nonnegative integers or none.
        '''
        return self._hash_mark_counts