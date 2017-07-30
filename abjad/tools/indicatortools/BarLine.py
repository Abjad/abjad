# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BarLine(AbjadValueObject):
    r'''Bar line.

    ::

        >>> import abjad

    ..  container:: example

        Final bar line:

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> bar_line = abjad.BarLine('|.')
            >>> abjad.attach(bar_line, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> bar_line
            BarLine('|.')

        ..  docs::

            >>> f(staff)
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

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.abbreviation)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            storage_format_args_values=[self.abbreviation],
            )

    def _get_lilypond_format(self):
        return r'\bar "{}"'.format(self.abbreviation)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ## PUBLIC PROPERTIES ##

    @property
    def abbreviation(self):
        r'''Gets abbreviation of bar line.

        ..  container:: example

            ::

                >>> bar_line = abjad.BarLine('|.')
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

                >>> bar_line = abjad.BarLine('|.')
                >>> bar_line.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Returns staff.
        '''
        return self._default_scope
