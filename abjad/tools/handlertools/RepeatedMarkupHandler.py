# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.handlertools.ArticulationHandler import ArticulationHandler
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


class RepeatedMarkupHandler(ArticulationHandler):
    r'''Repeated markup handler.

    ..  container:: example

        **Example 1.** Attaches markup to every leaf:

        ::

            >>> handler = handlertools.RepeatedMarkupHandler(
            ...     markups=[Markup('sec.', direction=Up)],
            ...     )
            >>> staff = Staff("c'4 d' e' f'")
            >>> logical_ties = iterate(staff).by_logical_tie(pitched=True)
            >>> logical_ties = list(logical_ties)
            >>> handler(logical_ties)
            >>> show(staff)  # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                c'4 ^ \markup { sec. }
                d'4 ^ \markup { sec. }
                e'4 ^ \markup { sec. }
                f'4 ^ \markup { sec. }
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_markups',
        )

    ### INITIALIZER ###

    def __init__(self, markups=None):
        if markups is not None:
            markups = [markuptools.Markup(_) for _ in markups]
            markups = tuple(markups)
        self._markups = markups

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls handler on `logical_ties`.

        Returns none.
        '''
        markups = datastructuretools.CyclicTuple(self.markups)
        for i, logical_tie in enumerate(logical_ties):
            markup = markups[i]
            markup = markuptools.Markup(markup)
            attach(markup, logical_tie.head)

    ### PUBLIC PROPERTIES ###

    @property
    def markups(self):
        r'''Gets markups of handler.

        Returns tuple or none.
        '''
        return self._markups