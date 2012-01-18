from abjad.core import _Immutable


class SchemeVector(tuple, _Immutable):
    '''.. versionadded:: 2.0

    Abjad model of Scheme vector::

        abjad> schemetools.SchemeVector(True, True, False)
        SchemeVector(True, True, False)

    Scheme vectors and Scheme vector constants differ in only their LilyPond input format.

    Scheme vectors are immutable.
    '''

    def __new__(klass, *args):
        self = tuple.__new__(klass, args)
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
        return ', '.join([str(x) for x in self])

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
        '''LilyPond input format of Scheme vector::

            abjad> scheme_vector = schemetools.SchemeVector(True, True, False)
            abjad> scheme_vector.format
            "#'(#t #t #f)"

        Return string.
        '''
        return "#'%s" % self.__str__()
