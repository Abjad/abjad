# -*- encoding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemeAssociativeList(Scheme):
    '''Abjad model of Scheme associative list:

    ::

        >>> schemetools.SchemeAssociativeList(
        ...     ('space', 2), ('padding', 0.5))
        SchemeAssociativeList(SchemePair('space', 2), SchemePair('padding', 0.5))

    Scheme associative lists are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import schemetools
        args_as_pairs = []
        for arg in args:
            if not isinstance(arg, (tuple, schemetools.SchemePair)):
                message = 'must be Python pair or Scheme pair: "%s".'
                raise TypeError(message % arg)
            arg_as_pair = schemetools.SchemePair(*arg)
            args_as_pairs.append(arg_as_pair)
        Scheme.__init__(self, *args_as_pairs, **{'quoting': "'"})
