# -*- encoding: utf-8 -*-
import functools
from abjad.tools import durationtools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject
from abjad.tools.topleveltools.new import new


@functools.total_ordering
class ColorFingering(AbjadObject):
    r'''Color fingering.

    ..  container:: example

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
                    \scale
                        #'(0.75 . 0.75)
                        \override
                            #'(circle-padding . 0.25)
                            \circle
                                \finger
                                    1
                    }

    Color fingerings indicate alternate woodwind fingerings by amount of pitch
    of timbre deviation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(
        self,
        number=None,
        ):
        if number is not None:
            assert mathtools.is_positive_integer(number)
        self._number = number

    ### SPECIAL METHODS ##

    def __eq__(self, expr):
        r'''Is true if `expr` is a color fingering with the same number
        point as this color fingering.

        ..  container:: example

            ::

                >>> fingering_1 = indicatortools.ColorFingering(1)
                >>> fingering_2 = indicatortools.ColorFingering(1)
                >>> fingering_3 = indicatortools.ColorFingering(2)

            ::

                >>> fingering_1 == fingering_1
                True
                >>> fingering_1 == fingering_2
                True
                >>> fingering_1 == fingering_3
                False

            ::

                >>> fingering_2 == fingering_1
                True
                >>> fingering_2 == fingering_2
                True
                >>> fingering_2 == fingering_3
                False

            ::

                >>> fingering_3 == fingering_1
                False
                >>> fingering_3 == fingering_2
                False
                >>> fingering_3 == fingering_3
                True

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self.number == expr.number
        raise TypeError('unorderable types')

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

    def __hash__(self):
        r'''Hashes color fingering.
        '''
        from abjad.tools import systemtools
        return hash(systemtools.StorageFormatManager.get_hash_values(self))

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

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            return self.number < expr.number
        raise TypeError('unorderable types')

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from scoremanager import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='number',
                command='n',
                editor=idetools.getters.get_string,
                ),
            )

    @property
    def _contents_repr_string(self):
        return repr(self.number)

    @property
    def _lilypond_format(self):
        return format(self.markup, 'lilypond')

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        markup = self.markup
        markup = new(markup, direction=Up)
        markup_format_pieces = markup._get_format_pieces()
        lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets markup of color fingering.

        ..  container:: example

            ::

                >>> fingering = indicatortools.ColorFingering(1)
                >>> print(format(fingering.markup, 'lilypond'))
                \markup {
                    \scale
                        #'(0.75 . 0.75)
                        \override
                            #'(circle-padding . 0.25)
                            \circle
                                \finger
                                    1
                    }

        Returns markup.
        '''
        if self.number is None:
            return
        markup = markuptools.Markup(str(self.number))
        markup = markup.finger()
        markup = markup.circle()
        markup = markup.override(('circle-padding', 0.25))
        markup = markup.scale((0.75, 0.75))
        return markup

    @property
    def number(self):
        r'''Gets number of color fingering.

        ..  container:: example

            ::

                >>> fingering = indicatortools.ColorFingering(1)
                >>> fingering.number
                1

        Set to positive integer.
        '''
        return self._number