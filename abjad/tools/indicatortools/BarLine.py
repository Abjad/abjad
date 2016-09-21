# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BarLine(AbjadValueObject):
    r'''A bar line.

    ..  container:: example

        **Example 1.** Final bar line:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> bar_line = indicatortools.BarLine('|.')
            >>> attach(bar_line, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> bar_line
            BarLine('|.')

        ..  doctest::

            >>> print(format(staff))
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            storage_format_args_values=[self.abbreviation],
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.abbreviation)

    @property
    def _lilypond_format(self):
        return r'\bar "{}"'.format(self.abbreviation)

    ## PUBLIC PROPERTIES ##

    @property
    def abbreviation(self):
        r'''Gets abbreviation of bar line.

        ..  container:: example

            ::

                >>> bar_line = indicatortools.BarLine('|.')
                >>> bar_line.abbreviation
                '|.'

        Returns string.
        '''
        return self._abbreviation

    @property
    def default_scope(self):
        r'''Gets default scope of bar line.

        ..  container:: example

            ::

                >>> bar_line = indicatortools.BarLine('|.')
                >>> bar_line.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Bar lines are scoped to the staff by default.

        Returns staff.
        '''
        return self._default_scope
