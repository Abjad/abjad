# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class SystemBreak(AbjadValueObject):
    r'''A line break.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> break_ = indicatortools.SystemBreak()
        >>> attach(break_, staff[-1])
        >>> show(staff) # doctest: +SKIP

    ::

        >>> break_
        SystemBreak()

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