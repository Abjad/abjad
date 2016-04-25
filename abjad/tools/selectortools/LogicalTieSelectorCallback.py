# -*- coding: utf-8 -*-
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate
from abjad.tools.abctools import AbjadValueObject


class LogicalTieSelectorCallback(AbjadValueObject):
    r'''A logical tie selector callback.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Callbacks'

    __slots__ = (
        '_flatten',
        '_pitched',
        '_trivial',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        flatten=True,
        pitched=True,
        trivial=True,
        ):
        self._flatten = bool(flatten)
        self._pitched = bool(pitched)
        self._trivial = bool(trivial)

    ### SPECIAL METHODS ###

    def __call__(self, expr, rotation=None):
        r'''Iterates tuple `expr`.

        Returns tuple of selections.
        '''
        assert isinstance(expr, tuple), repr(expr)
        result = []
        if self.flatten:
            visited_logical_ties = set()
            for subexpr in expr:
                for logical_tie in self._iterate_expr(subexpr):
                    if logical_tie in visited_logical_ties:
                        continue
                    result.append(logical_tie)
                    visited_logical_ties.add(logical_tie)
        else:
            for subexpr in expr:
                subresult = []
                visited_logical_ties = set()
                for logical_tie in self._iterate_expr(subexpr):
                    if logical_tie in visited_logical_ties:
                        continue
                    subresult.append(logical_tie)
                    visited_logical_ties.add(logical_tie)
                subresult = selectiontools.Selection(subresult)
                result.append(subresult)
        return tuple(result)

    ### PRIVATE METHODS ###

    def _iterate_expr(self, expr):
        from abjad.tools import scoretools
        prototype = scoretools.Leaf
        if self.pitched:
            prototype = (scoretools.Chord, scoretools.Note)
        current_tie_spanner = None
        leaves = tuple(iterate(expr).by_class(prototype))
        for leaf in leaves:
            tie_spanners = tuple(leaf._get_spanners(spannertools.Tie))
            if not tie_spanners or \
                tie_spanners[0] is not current_tie_spanner:
                if tie_spanners:
                    current_tie_spanner = tie_spanners[0]
                else:
                    current_tie_spanner = None
                logical_tie = leaf._get_logical_tie()
                if not self.trivial and len(logical_tie) == 1:
                    continue
                yield logical_tie

    ### PUBLIC PROPERTIES ###

    @property
    def flatten(self):
        r'''Is true if callback returns all logical ties in a single selection,
        rather than grouping by each original sub-expression.

        Returns true or false.
        '''
        return self._flatten

    @property
    def pitched(self):
        r'''Is true if callback iterates pitched logical ties.

        Returns true or false.
        '''
        return self._pitched

    @property
    def trivial(self):
        r'''Is true if callback iterates trivial logical ties.

        Returns true or false.
        '''
        return self._trivial
