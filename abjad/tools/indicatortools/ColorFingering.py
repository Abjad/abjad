# -*- coding: utf-8 -*-
import functools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadValueObject
from abjad.tools.topleveltools.new import new


@functools.total_ordering
class ColorFingering(AbjadValueObject):
    r'''Color fingering.

    ..  container:: example

        **Example 1.** First color fingering:

        ::

            >>> fingering = indicatortools.ColorFingering(1)
            >>> note = Note("c'4")
            >>> attach(fingering, note)

        ::

            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> f(note)
            c'4
                ^ \markup {
                    \override
                        #'(circle-padding . 0.25)
                        \circle
                            \finger
                                1
                    }

    ..  container:: example

        **Example 2.** Second color fingering:

        ::

            >>> fingering = indicatortools.ColorFingering(2)
            >>> note = Note("c'4")
            >>> attach(fingering, note)

        ::

            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> f(note)
            c'4
                ^ \markup {
                    \override
                        #'(circle-padding . 0.25)
                        \circle
                            \finger
                                2
                    }

    Color fingerings indicate alternate woodwind fingerings by amount of pitch
    of timbre deviation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_number',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(
        self,
        number=None,
        ):
        self._default_scope = None
        if number is not None:
            assert mathtools.is_positive_integer(number)
        self._number = number

    ### SPECIAL METHODS ##

    def __format__(self, format_specification=''):
        r'''Formats color fingering.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> fingering = indicatortools.ColorFingering(1)
            >>> print(format(fingering))
            indicatortools.ColorFingering(
                number=1,
                )

        Returns string.
        '''
        if format_specification == 'lilypond':
            return self._lilypond_format
        superclass = super(ColorFingering, self)
        return superclass.__format__(format_specification=format_specification)

    def __lt__(self, expr):
        r'''Is true if `expr` is a color fingering and the number of this color
        fingering is less than that of `expr`.

        ..  container:: example

            ::

                >>> fingering_1 = indicatortools.ColorFingering(1)
                >>> fingering_2 = indicatortools.ColorFingering(1)
                >>> fingering_3 = indicatortools.ColorFingering(2)

            ::

                >>> fingering_1 < fingering_1
                False
                >>> fingering_1 < fingering_2
                False
                >>> fingering_1 < fingering_3
                True

            ::

                >>> fingering_2 < fingering_1
                False
                >>> fingering_2 < fingering_2
                False
                >>> fingering_2 < fingering_3
                True

            ::

                >>> fingering_3 < fingering_1
                False
                >>> fingering_3 < fingering_2
                False
                >>> fingering_3 < fingering_3
                False

        Returns true or false.
        '''
        if isinstance(expr, type(self)):
            return self.number < expr.number
        raise TypeError('unorderable types')

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self.markup
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.number)

    @property
    def _lilypond_format(self):
        return format(self.markup, 'lilypond')

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of color fingering.

        ..  container:: example

            ::

                >>> fingering = indicatortools.ColorFingering(1)
                >>> fingering.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def markup(self):
        r'''Gets markup of color fingering.

        ..  container:: example

            **Example 1.** First color fingering:

            ::

                >>> fingering = indicatortools.ColorFingering(1)
                >>> print(format(fingering.markup, 'lilypond'))
                \markup {
                    \override
                        #'(circle-padding . 0.25)
                        \circle
                            \finger
                                1
                    }
                >>> show(fingering.markup) # doctest: +SKIP

        ..  container:: example

            **Example 2.** Second color fingering:

            ::

                >>> fingering = indicatortools.ColorFingering(2)
                >>> print(format(fingering.markup, 'lilypond'))
                \markup {
                    \override
                        #'(circle-padding . 0.25)
                        \circle
                            \finger
                                2
                    }
                >>> show(fingering.markup) # doctest: +SKIP

        Returns markup.
        '''
        if self.number is None:
            return
        markup = markuptools.Markup(str(self.number))
        markup = markup.finger()
        markup = markup.circle()
        markup = markup.override(('circle-padding', 0.25))
        return markup

    @property
    def number(self):
        r'''Gets number of color fingering.

        ..  container:: example

            **Example 1.** First color fingering:

            ::

                >>> fingering = indicatortools.ColorFingering(1)
                >>> fingering.number
                1

        ..  container:: example

            **Example 2.** Second color fingering:

            ::

                >>> fingering = indicatortools.ColorFingering(2)
                >>> fingering.number
                2

        Returns positive integer.
        '''
        return self._number
