# -*- encoding: utf-8 -*-
from abjad.tools.schemetools.Scheme import Scheme


class SchemePair(Scheme):
    r'''A Scheme pair.

    ::

        >>> schemetools.SchemePair('spacing', 4)
        SchemePair(('spacing', 4))

    Initialize Scheme pairs with a tuple, two separate values 
    or another Scheme pair.

    Scheme pairs are immutable.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ##

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], SchemePair):
            args = args[0]._value
        elif len(args) == 1 and isinstance(args[0], tuple):
            args = args[0][:]
        elif len(args) == 2:
            args = args
        else:
            message = 'can not initialize Scheme pair from {!r}.'
            raise TypeError(message.format(args))
        Scheme.__init__(self, *args, **kwargs)

    ### PRIVATE PROPERTIES ###

    @property
    def _formatted_value(self):
        from abjad.tools import schemetools
        assert len(self._value) == 2
        lhs = schemetools.Scheme.format_scheme_value(self._value[0])
        # need to force quotes around pairs like 
        # \override #'(font-name . "Times")
        rhs = schemetools.Scheme.format_scheme_value(
            self._value[-1], force_quotes=True)
        return '({} . {})'.format(lhs, rhs)

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        return "#'%s" % self._formatted_value
