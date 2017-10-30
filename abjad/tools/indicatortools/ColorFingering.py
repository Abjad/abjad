import functools
from abjad.tools.abctools import AbjadValueObject


@functools.total_ordering
class ColorFingering(AbjadValueObject):
    r'''Color fingering.

    ..  container:: example

        First color fingering:

        >>> fingering = abjad.ColorFingering(1)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4
                ^ \markup {
                    \override
                        #'(circle-padding . 0.25)
                        \circle
                            \finger
                                1
                    }

    ..  container:: example

        Second color fingering:

        >>> fingering = abjad.ColorFingering(2)
        >>> note = abjad.Note("c'4")
        >>> abjad.attach(fingering, note)

        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
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
        '_number',
        )

    _format_slot = 'right'

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        number=None,
        ):
        import abjad
        if number is not None:
            assert abjad.mathtools.is_positive_integer(number)
        self._number = number

    ### SPECIAL METHODS ##

    def __format__(self, format_specification=''):
        r'''Formats color fingering.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        >>> fingering = abjad.ColorFingering(1)
        >>> abjad.f(fingering)
        abjad.ColorFingering(
            number=1,
            )

        Returns string.
        '''
        if format_specification == 'lilypond':
            return self._get_lilypond_format()
        superclass = super(ColorFingering, self)
        return superclass.__format__(format_specification=format_specification)

    def __lt__(self, argument):
        r'''Is true if `argument` is a color fingering and the number of this color
        fingering is less than that of `argument`.

        ..  container:: example

            >>> fingering_1 = abjad.ColorFingering(1)
            >>> fingering_2 = abjad.ColorFingering(1)
            >>> fingering_3 = abjad.ColorFingering(2)

            >>> fingering_1 < fingering_1
            False
            >>> fingering_1 < fingering_2
            False
            >>> fingering_1 < fingering_3
            True

            >>> fingering_2 < fingering_1
            False
            >>> fingering_2 < fingering_2
            False
            >>> fingering_2 < fingering_3
            True

            >>> fingering_3 < fingering_1
            False
            >>> fingering_3 < fingering_2
            False
            >>> fingering_3 < fingering_3
            False

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            return self.number < argument.number
        raise TypeError('unorderable types')

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return repr(self.number)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return format(self.markup, 'lilypond')

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        markup = self.markup
        markup = abjad.new(markup, direction=abjad.Up)
        markup_format_pieces = markup._get_format_pieces()
        bundle.right.markup.extend(markup_format_pieces)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets markup of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> print(format(fingering.markup, 'lilypond'))
            \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            1
                }
            >>> abjad.show(fingering.markup) # doctest: +SKIP

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> print(format(fingering.markup, 'lilypond'))
            \markup {
                \override
                    #'(circle-padding . 0.25)
                    \circle
                        \finger
                            2
                }
            >>> abjad.show(fingering.markup) # doctest: +SKIP

        Returns markup.
        '''
        import abjad
        if self.number is None:
            return
        markup = abjad.Markup(str(self.number))
        markup = markup.finger()
        markup = markup.circle()
        markup = markup.override(('circle-padding', 0.25))
        return markup

    @property
    def number(self):
        r'''Gets number of color fingering.

        ..  container:: example

            First color fingering:

            >>> fingering = abjad.ColorFingering(1)
            >>> fingering.number
            1

        ..  container:: example

            Second color fingering:

            >>> fingering = abjad.ColorFingering(2)
            >>> fingering.number
            2

        Returns positive integer.
        '''
        return self._number
