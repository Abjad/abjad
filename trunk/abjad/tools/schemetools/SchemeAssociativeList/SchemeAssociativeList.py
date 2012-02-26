from abjad.tools.schemetools.Scheme import Scheme
from abjad.tools.schemetools.SchemePair import SchemePair


class SchemeAssociativeList(Scheme):
    '''.. versionadded:: 2.0

    Abjad model of Scheme associative list::

        abjad> from abjad.tools.schemetools import SchemeAssociativeList
        abjad> SchemeAssociativeList(('space', 2), ('padding', 0.5))
        SchemeAssociativeList((SchemePair(('space', 2)), SchemePair(('padding', 0.5))))

    Scheme associative lists are immutable.
    '''

    def __new__(klass, *args, **kwargs):
        args_as_pairs = []
        for arg in args:
            if not isinstance(arg, (tuple, SchemePair)):
                raise TypeError('must be Python pair or Scheme pair: "%s".' % str(arg))
            arg_as_pair = SchemePair(*arg)
            args_as_pairs.append(arg_as_pair)
        return Scheme.__new__(klass, *args_as_pairs, **{'quoting': "'"})
