# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class PageBreak(AbjadValueObject):
    r'''A page break.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> page_break = indicatortools.PageBreak()
        >>> attach(page_break, staff[-1])
        >>> score = Score([staff])
        >>> show(score) # doctest: +SKIP

    ::

        >>> page_break
        PageBreak()

    ..  doctest::

        >>> print(format(score))
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                \pageBreak
            }
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        )

    _format_slot = 'closing'

    ### INITIALIZER ##

    def __init__(self):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return r'\pageBreak'