# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class BarLine(AbjadObject):
    r'''A bar line.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = indicatortools.BarLine('|.')
        >>> attach(bar_line, staff[-1])
        >>> show(staff) # doctest: +SKIP

    ::

        >>> bar_line
        BarLine('|.')

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \bar "|."
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_abbreviation',
        '_default_scope',
        )

    _format_slot = 'closing'

    ### INITIALIZER ##

    def __init__(self, abbreviation='|'):
        from abjad.tools import scoretools
        assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        self._default_scope = scoretools.Staff

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies bar line.

        Returns new bar line.
        '''
        return type(self)(self.abbreviation)

    def __eq__(self, arg):
        r'''True when `arg` is a bar line with an abbreviation equal
        to that of this bar line. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self.abbreviation == arg.abbreviation
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.abbreviation)

    @property
    def _lilypond_format(self):
        return r'\bar "{}"'.format(self.abbreviation)

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                self.abbreviation,
                ),
            )

    ## PUBLIC PROPERTIES ##

    @property
    def abbreviation(self):
        r'''Abbreviation of bar line.

        ::

            >>> bar_line.abbreviation
            '|.'

        Returns string.
        '''
        return self._abbreviation
