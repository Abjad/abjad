from abjad.tools.schemetools.Scheme import Scheme


class SchemeAssociativeList(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme associative list::

        >>> from abjad.tools.schemetools import SchemeAssociativeList
        >>> SchemeAssociativeList(('space', 2), ('padding', 0.5))
        SchemeAssociativeList((SchemePair(('space', 2)), SchemePair(('padding', 0.5))))

    Scheme associative lists are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools import schemetools
        args_as_pairs = []
        for arg in args:
            if not isinstance(arg, (tuple, schemetools.SchemePair)):
                raise TypeError('must be Python pair or Scheme pair: "%s".' % str(arg))
            arg_as_pair = schemetools.SchemePair(*arg)
            args_as_pairs.append(arg_as_pair)
        Scheme.__init__(self, *args_as_pairs, **{'quoting': "'"})
