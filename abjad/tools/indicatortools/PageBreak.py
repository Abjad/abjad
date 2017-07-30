# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class PageBreak(AbjadValueObject):
    r'''Page break.

    ::

        >>> import abjad

    ..  container:: example

        Default page break:

        ::

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> page_break = abjad.PageBreak()
            >>> abjad.attach(page_break, staff[-1])
            >>> show(staff) # doctest: +SKIP

        ::

            >>> page_break
            PageBreak()

        ..  docs::

            >>> f(staff)
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

    _time_orientation = Right

    ### INITIALIZER ##

    def __init__(self):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Score

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\pageBreak'

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of page break.

        ..  container:: example

            Default page break:

            ::

                
                >>> page_break = abjad.PageBreak()
                >>> page_break.default_scope
                <class 'abjad.tools.scoretools.Score.Score'>

        Returns score.
        '''
        return self._default_scope
