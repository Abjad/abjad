from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BarLine(AbjadValueObject):
    r'''Bar line.

    ..  container:: example

        Final bar line:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> bar_line = abjad.BarLine('|.')
        >>> abjad.attach(bar_line, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> bar_line
        BarLine('|.')

        ..  docs::

            >>> abjad.f(staff)
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
        '_context',
        )

    _format_slot = 'closing'

    ### INITIALIZER ##

    def __init__(self, abbreviation='|'):
        assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        self._context = 'Staff'

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.abbreviation)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
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

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.abbreviation
            '|.'

        Returns string.
        '''
        return self._abbreviation

    @property
    def context(self):
        r'''Gets default context of bar line.

        ..  container:: example

            >>> bar_line = abjad.BarLine('|.')
            >>> bar_line.context
            'Staff'

        Returns context or string.
        '''
        return self._context
