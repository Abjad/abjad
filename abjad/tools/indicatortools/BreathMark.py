# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class BreathMark(AbjadValueObject):
    r'''A breath mark.

    ..  container:: example

        BreathMark:

        ::

            >>> note = Note("c'4")
            >>> breath_mark = indicatortools.BreathMark()
            >>> attach(breath_mark, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 \breathe

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _format_slot = 'after'

    ### INITIALIZER ###

    def __init__(self):
        pass

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
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)