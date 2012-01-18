from abjad.core import _Immutable
from abjad.tools.schemetools.SchemePair import SchemePair


class SchemeAssociativeList(tuple, _Immutable):
    '''.. versionadded:: 2.0

    Abjad model of Scheme associative list::

        abjad> schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
        SchemeAssociativeList(SchemePair('space', 2), SchemePair('padding', 0.5))

    Scheme associative lists are immutable.
    '''

    def __new__(klass, *args):
        args_as_pairs = []
        for arg in args:
            if not isinstance(arg, (tuple, SchemePair)):
                raise TypeError('must be Python pair or Scheme pair: "%s".' % str(arg))
            arg_as_pair = SchemePair(*arg)
            args_as_pairs.append(arg_as_pair)
        self = tuple.__new__(klass, args_as_pairs)
        return self

    def __getnewargs__(self):
        return tuple(self)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self._format_string)

    def __str__(self):
        return '(%s)' % self._output_string

    ### PRIVATE ATTRIBUTES ###

    @property
    def _format_string(self):
        return ', '.join([repr(x) for x in self])

    @property
    def _output_string(self):
        vals = []
        for x in self:
            if isinstance(x, bool) and x:
                vals.append("#t")
            elif isinstance(x, bool):
                vals.append("#f")
            else:
                vals.append(x)
        return ' '.join([str(x) for x in vals])

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme associative list::

            abjad> scheme_associative_list = schemetools.SchemeAssociativeList(('space', 2), ('padding', 0.5))
            abjad> scheme_associative_list.format
            "#'((space . 2) (padding . 0.5))"

        Return string.
        '''
        return "#'%s" % self.__str__()
