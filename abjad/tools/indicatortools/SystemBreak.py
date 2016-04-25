# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SystemBreak(AbjadValueObject):
    r'''System break indicator.

    ..  container:: example

        **Example 1.** Default system break:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> break_ = indicatortools.SystemBreak()
            >>> attach(break_, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
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

    ### INITIALIZER ##

    def __init__(self):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\break'

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of system break indicator.

        ..  container:: example

            **Example 1.** Default system break:

            ::

                >>> break_ = indicatortools.SystemBreak()
                >>> break_.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  todo:: Make system breaks score-scoped.

        Returns staff (but should return score).
        '''
        return self._default_scope
