# -*- coding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeAssociativeList(Scheme):
    '''Abjad model of Scheme associative list.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> scheme_alist = abjad.SchemeAssociativeList([
            ...     ('space', 2),
            ...     ('padding', 0.5),
            ...     ])
            >>> f(scheme_alist)
            abjad.SchemeAssociativeList(
                [
                    abjad.SchemePair(('space', 2)),
                    abjad.SchemePair(('padding', 0.5)),
                    ]
                )

        ::

            >>> print(format(scheme_alist))
            #'((space . 2) (padding . 0.5))

    Scheme associative lists are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, value=None):
        from abjad.tools import schemetools
        value = value or []
        pairs = []
        for item in value:
            if isinstance(item, tuple):
                pair = schemetools.SchemePair(item)
            elif isinstance(item, schemetools.SchemePair):
                pair = item
            else:
                message = 'must be Python pair or Scheme pair: {!r}.'
                message = message.format(item)
                raise TypeError(message)
            pairs.append(pair)
        Scheme.__init__(self, value=pairs, quoting="'")
