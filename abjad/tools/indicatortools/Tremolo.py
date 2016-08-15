# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Tremolo(AbjadValueObject):
    r'''A (two-note) tremolo.
    
    ..  container:: example

        **Example 1.** With two beams:

        ::

            >>> chord = Chord("<cs' e'>4")
            >>> tremolo = indicatortools.Tremolo(beam_count=2)
            >>> attach(tremolo, chord)
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
            \repeat tremolo 2
            {
            cs'16 e'16
            }

    ..  container:: example

        **Example 2.** With three beams:

        ::

            >>> chord = Chord("<cs' e'>4")
            >>> tremolo = indicatortools.Tremolo(beam_count=3)
            >>> attach(tremolo, chord)
            >>> show(chord) # doctest: +SKIP

        ..  doctest::

            >>> print(format(chord))
            \repeat tremolo 4
            {
            cs'32 e'32
            }

    Tremolo affects the formatting of chords.

    Tremolo has no effect when attached to notes or rests.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beam_count',
        '_is_slurred',
        )

    _format_slot = None

    ### INITIALIZER ###

    def __init__(self, beam_count=3, is_slurred=None):
        assert isinstance(beam_count, int), repr(beam_count)
        assert 0 < beam_count, repr(beam_count)
        self._beam_count = beam_count
        prototype = (type(None), type(True))
        assert isinstance(is_slurred, prototype), repr(is_slurred)
        self._is_slurred = is_slurred

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies tremolo.

        ..  container:: example

            **Example 1.** Copies tremolo:

            ::

                >>> import copy
                >>> tremolo_1 = indicatortools.Tremolo(beam_count=2)
                >>> tremolo_2 = copy.copy(tremolo_1)

            ::

                >>> tremolo_1 == tremolo_2
                True

            ::

                >>> tremolo_1 is not tremolo_2
                True

        Returns new tremolo.
        '''
        superclass = super(Tremolo, self)
        return superclass.__copy__(*args)

    def __format__(self, format_specification=''):
        r'''Formats stem tremolo.

        ..  container:: example

            **Example 1.** With two beams:

            ::

                >>> tremolo = indicatortools.Tremolo(beam_count=2)
                >>> print(format(tremolo))
                indicatortools.Tremolo(
                    beam_count=2,
                    )

        ..  container:: example

            **Example 2.** With three beams:

            ::

                >>> tremolo = indicatortools.Tremolo(beam_count=3)
                >>> print(format(tremolo))
                indicatortools.Tremolo(
                    beam_count=3,
                    )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            message = 'no LilyPond format available.'
            raise Exception(message)
        else:
            message = "format_specification must be 'storage' or ''."
            raise Exception(message)

    def __str__(self):
        r'''Gets string representation of tremolo.

        ..  container:: example

            **Example 1.** With two beams:

            ::

                >>> tremolo = indicatortools.Tremolo(beam_count=2)
                >>> str(tremolo)
                'Tremolo(beam_count=2)'

        ..  container:: example

            **Example 2.** With three beams:

            ::

                >>> tremolo = indicatortools.Tremolo(beam_count=3)
                >>> str(tremolo)
                'Tremolo(beam_count=3)'

        Returns string.
        '''
        superclass = super(Tremolo, self)
        return superclass.__str__()

    ### PUBLIC PROPERTIES ###

    @property
    def beam_count(self):
        r'''Gets beam count of tremolo.

        ..  container:: example

            **Example 1.** With two beams:

            ::

                >>> chord = Chord("<cs' e'>4")
                >>> tremolo = indicatortools.Tremolo(beam_count=2)
                >>> attach(tremolo, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                \repeat tremolo 2
                {
                cs'16 e'16
                }

        ..  container:: example

            **Example 2.** With three beams:

            ::

                >>> chord = Chord("<cs' e'>4")
                >>> tremolo = indicatortools.Tremolo()
                >>> attach(tremolo, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                \repeat tremolo 4
                {
                cs'32 e'32
                }

        Set to positive integer.

        Defaults to 3.

        Returns positive integer.
        '''
        return self._beam_count

    @property
    def is_slurred(self):
        r'''Is true when tremolo is slurred. Otherwise false.

        ..  container:: example

            **Example 1.** Without slur:

            ::

                >>> chord = Chord("<cs' e'>4")
                >>> tremolo = indicatortools.Tremolo()
                >>> attach(tremolo, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                \repeat tremolo 4
                {
                cs'32 e'32
                }

        ..  container:: example

            **Example 2.** With slur:

            ::

                >>> chord = Chord("<cs' e'>4")
                >>> tremolo = indicatortools.Tremolo(is_slurred=True)
                >>> attach(tremolo, chord)
                >>> show(chord) # doctest: +SKIP

            ..  doctest::

                >>> print(format(chord))
                \repeat tremolo 4
                {
                cs'32 \( e'32 \)
                }

        Set to true or false.

        Defaults to false.
                
        Returns true or false.
        '''
        return self._is_slurred
