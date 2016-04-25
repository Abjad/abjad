# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class PageBreak(AbjadValueObject):
    r'''A page break.

    ..  container:: example

        **Example 1.** Default page break:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> page_break = indicatortools.PageBreak()
            >>> attach(page_break, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> page_break
            PageBreak()

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                \pageBreak
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
        return r'\pageBreak'

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of page break.

        ..  container:: example

            **Example 1.** Default page break:

            ::

                
                >>> page_break = indicatortools.PageBreak()
                >>> page_break.default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Page breaks are staff-scoped by default.

        ..  todo:: Page breaks should be score-scoped.

        Returns staff (but should return score).
        '''
        return self._default_scope
