# -*- coding: utf-8 -*-
from abjad.tools.topleveltools import new
from abjad.tools.schemetools.Scheme import Scheme


class SchemePair(Scheme):
    r'''A Scheme pair.

    ::

        >>> schemetools.SchemePair('spacing', 4)
        SchemePair('spacing', 4)

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
        elif len(args) == 0:
            args = (0, 1)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise TypeError(message)
        Scheme.__init__(self, *args, **kwargs)

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats Scheme pair.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'lilypond'`.

        ::

            >>> scheme_pair = schemetools.SchemePair(-1, 1)

        ::

            >>> format(scheme_pair)
            "#'(-1 . 1)"

        ::

            >>> print(format(scheme_pair, 'storage'))
            schemetools.SchemePair(-1, 1)

        Returns string.
        '''
        superclass = super(SchemePair, self)
        return superclass.__format__(format_specification=format_specification)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        specification = super(SchemePair, self)._get_format_specification()
        return new(
            specification,
            repr_is_indented=False,
            storage_format_is_indented=False,
            )

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

    @property
    def _lilypond_format(self):
        return "#'%s" % self._formatted_value
