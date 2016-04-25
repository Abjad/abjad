# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BreathMark(AbjadValueObject):
    r'''A breath mark.

    ..  container:: example

        **Example 1.** Attached to a single note:

        ::

            >>> note = Note("c'4")
            >>> breath_mark = indicatortools.BreathMark()
            >>> attach(breath_mark, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 \breathe

    ..  container:: example

        **Examle 2.** Attached to notes in a staff:

        ::

            >>> staff = Staff("c'8 d' e' f' g' a' b' c''")
            >>> attach(Beam(), staff[:4])
            >>> attach(Beam(), staff[4:])
            >>> attach(indicatortools.BreathMark(), staff[3])
            >>> attach(indicatortools.BreathMark(), staff[7])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8 [
                d'8
                e'8
                f'8 ]
                \breathe
                g'8 [
                a'8
                b'8
                c''8 ]
                \breathe
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        )

    _format_slot = 'after'

    ### INITIALIZER ###

    def __init__(self):
        self._default_scope = None

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of breath mark.

        ..  container:: example

            ::

                >>> str(indicatortools.BreathMark())
                '\\breathe'

        Returns string.
        '''
        return r'\breathe'

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.after.commands.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of breath mark.

        ..  container:: example

            ::

                >>> breath_mark = indicatortools.BreathMark()
                >>> breath_mark.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
