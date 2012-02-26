from abjad.tools.schemetools.Scheme import Scheme


class SchemePair(Scheme):
    '''Abjad model of Scheme pair::

        abjad> schemetools.SchemePair('spacing', 4)
        SchemePair(('spacing', 4))

    Initialize Scheme pairs with a tuple, two separate values or another Scheme pair.

    Scheme pairs are immutable.
    '''

    def __new__(klass, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], SchemePair):
            args = args[0]._value
        elif len(args) == 1 and isinstance(args[0], tuple):
            args = args[0][:]
        elif len(args) == 2:
            args = args
        else:
            raise TypeError('can not initialize Scheme pair from "%s".' % str(args))

        self = Scheme.__new__(klass, *args, **kwargs)
        #self = object.__new__(klass)
        #object.__setattr__(self, '_value', args)
        return self

    ### PRIVATE ATTRIBUTES ###

    @property
    def _formatted_value(self):
        return '(%s . %s)' % tuple([Scheme._format_value(x) for x in self._value])

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        return "#'%s" % self._formatted_value 
