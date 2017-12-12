from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SystemBreak(AbjadValueObject):
    r'''System break indicator.

    ..  container:: example

        Default system break:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> break_ = abjad.SystemBreak()
        >>> abjad.attach(break_, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                \break
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        )

    _format_slot = 'closing'

    _time_orientation = Right

    ### INITIALIZER ##

    def __init__(self):
        self._context = 'Staff'

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\break'

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets default context of system break indicator.

        ..  container:: example

            Default system break:

            >>> break_ = abjad.SystemBreak()
            >>> break_.context
            'Staff'

        ..  todo:: Make system breaks score-contexted.

        Returns staff (but should return score).

        Returns context or string.
        '''
        return self._context
