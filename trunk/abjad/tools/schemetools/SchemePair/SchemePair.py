from abjad.core import _Immutable


class SchemePair(tuple, _Immutable):
    '''Abjad model of Scheme pair::

        abjad> schemetools.SchemePair('spacing', 4)
        SchemePair('spacing', 4)

    Initialize Scheme pairs with a tuple, two separate values or another Scheme pair.

    Scheme pairs are immutable.
    '''

    def __new__(klass, *args):
        if len(args) == 1 and isinstance(args[0], SchemePair):
            self = tuple.__new__(klass, args[0][:])
        elif len(args) == 1 and isinstance(args[0], tuple):
            self = tuple.__new__(klass, args[0][:])
        elif len(args) == 2:
            self = tuple.__new__(klass, args)
        else:
            raise TypeError('can not initialize Scheme pair from "%s".' % str(args))
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
        #return ', '.join([str(x) for x in self])
        result = []
        for x in self:
            if isinstance(x, str):
                result.append('%r' % x)
            else:
                result.append(str(x))
        result = ', '.join(result)
        return result

    @property
    def _output_string(self):
        vals = []
        for x in self:
            if isinstance(x, bool) and x:
                vals.append("#t")
            elif isinstance(x, bool):
                vals.append("#f")
            elif isinstance(x, str) and ' ' in x:
                vals.append('"%s"' % x)
            else:
                vals.append(x)
        return '%s . %s' % (vals[0], vals[1])

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        '''LilyPond input format of Scheme pair::

            abjad> scheme_pair = schemetools.SchemePair('spacing', 4)
            abjad> scheme_pair.format
            "#'(spacing . 4)"

        Return string.
        '''
        return "#'%s" % self.__str__()
