# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SystemBreak(AbjadValueObject):
    r'''System break indicator.

    ::

        >>> import abjad

    ..  container:: example

        Default system break:

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> break_ = abjad.SystemBreak()
            >>> abjad.attach(break_, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
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
        '_default_scope',
        )

    _format_slot = 'closing'

    _time_orientation = Right

    ### INITIALIZER ##

    def __init__(self):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff

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
    def default_scope(self):
        r'''Gets default scope of system break indicator.

        ..  container:: example

            Default system break:

            ::

                >>> break_ = abjad.SystemBreak()
                >>> break_.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  todo:: Make system breaks score-scoped.

        Returns staff (but should return score).
        '''
        return self._default_scope
