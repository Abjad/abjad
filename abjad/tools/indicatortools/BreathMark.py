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

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies breath_mark.

        ..  container:: example

            ::

                >>> import copy
                >>> breath_mark_1 = indicatortools.BreathMark()
                >>> breath_mark_2 = copy.copy(breath_mark_1)

            ::

                >>> str(breath_mark_1) == str(breath_mark_2)
                True

            ::

                >>> breath_mark_1 == breath_mark_2
                True

            ::

                >>> breath_mark_1 is breath_mark_2
                False

        Returns new breath_mark.
        '''
        return type(self)()

    def __str__(self):
        r'''Gets string representation of breath mark.

        ..  container:: example

            ::

                >>> str(indicatortools.BreathMark())
                '\\breathe'

        Returns string.
        '''
        return r'\breathe'

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle