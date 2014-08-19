# -*- encoding: utf-8 -*-
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import iterate
from abjad.tools.abctools import AbjadValueObject


class LogicalTieSelectorCallback(AbjadValueObject):
    r'''A logical tie selector callback.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_flatten',
        '_pitched',
        '_trivial',
        '_only_with_head',
        '_only_with_tail',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        flatten=True,
        pitched=True,
        trivial=True,
        only_with_head=True,
        only_with_tail=True,
        ):
        self._flatten = bool(flatten)
        self._pitched = bool(pitched)
        self._trivial = bool(trivial)
        self._only_with_head = bool(only_with_head)
        self._only_with_tail = bool(only_with_tail)

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Iterates `expr`.
        '''
        result = []
        if self.flatten:
            for subexpr in expr:
                result.extend(self._iterate_expr(subexpr))
        else:
            for subexpr in expr:
                subresult = selectiontools.Selection(
                    self._iterate_expr(subexpr),
                    )
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
                if self.only_with_head and logical_tie.head not in leaves:
                    continue
                if self.only_with_tail and logical_tie.tail not in leaves:
                    continue
                yield logical_tie

    ### PUBLIC PROPERTIES ###

    @property
    def flatten(self):
        r'''Is true if callback returns all logical ties in a single selection,
        rather than grouping by each original sub-expression.

        Returns boolean.
        '''
        return self._flatten

    @property
    def only_with_head(self):
        r'''Is true if callback only iterates logical ties whose heads are
        included in the expression to be iterated over.

        Returns boolean.
        '''
        return self._only_with_head

    @property
    def only_with_tail(self):
        r'''Is true if callback only iterates logical ties whose tails are
        included in the expression to be iterated over.

        Returns boolean.
        '''
        return self._only_with_tail

    @property
    def pitched(self):
        r'''Is true if callback iterates pitched logical ties.

        Returns boolean.
        '''
        return self._pitched

    @property
    def trivial(self):
        r'''Is true if callback iterates trivial logical ties.

        Returns boolean.
        '''
        return self._trivial