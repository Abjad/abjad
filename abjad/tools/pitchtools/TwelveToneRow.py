# -*- coding: utf-8 -*-
from abjad.tools.pitchtools.PitchClassSegment import PitchClassSegment
from abjad.tools.topleveltools import new


class TwelveToneRow(PitchClassSegment):
    '''Twelve-tone row.

    ..  container:: example

        **Example 1.** Initializes row from integers:

        ::

            >>> pitchtools.TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])
            TwelveToneRow([0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8])

    Twelve-tone rows validate pitch-classes at initialization.

    Twelve-tone rows inherit canonical operators from pitch-class segment.

    Twelve-tone rows return numbered pitch-class segments on calls to getslice.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=(0, 1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8),
        ):
        from abjad.tools import pitchtools
        assert items is not None
        PitchClassSegment.__init__(
            self,
            items=items,
            item_class=pitchtools.NumberedPitchClass,
            )
        self._validate_pitch_classes(self)

    ### SPECIAL METHODS ###

    def __getslice__(self, start, stop):
        r'''Gets items from `start` to `stop` in twelve-tone row.

        Returns pitch-class segment.
        '''
        from abjad.tools import pitchtools
        items = self._collection[start:stop]
        return PitchClassSegment(
            items=items,
            item_class=pitchtools.NumberedPitchClass,
            )

    def __mul__(self, expr):
        r'''Multiplies twelve-tone row by `expr`.

        Returns pitch-class segment.
        '''
        return PitchClassSegment(self) * expr

    def __rmul__(self, expr):
        r'''Multiplies `expr` by twelve-tone row.

        Returns pitch-class segment.
        '''
        return PitchClassSegment(self) * expr

    ### PRIVATE METHODS ###

    @staticmethod
    def _validate_pitch_classes(pitch_classes):
        numbers = [pc.pitch_class_number for pc in pitch_classes]
        numbers.sort()
        if not numbers == list(range(12)):
            message = 'must contain all twelve pitch-classes: {!r}.'
            message = message.format(pitch_classes)
            raise ValueError(message)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes twelve-tone row from `selection`.

        Returns twelve-tone row.
        '''
        raise NotImplementedError

    def invert(self, axis=None):
        r'''Inverts twelve-tone row about `axis`.

        ..  container:: example

            **Example 1.** Inverts twelve-tone row about first pitch-class
            in row when `axis` is none:

            ::

                >>> row = pitchtools.TwelveToneRow(
                ...     [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
                ...     )

            ::

                >>> row.invert()
                TwelveToneRow([1, 3, 5, 11, 8, 7, 9, 10, 4, 0, 6, 2])

            First pitch-classes of prime form and inversion are equal.

        ..  container:: example

            **Example 2.** Inverts twelve-tone row about pitch-class 1:

            ::

                >>> row = pitchtools.TwelveToneRow(
                ...     [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
                ...     )

            ::

                >>> row.invert(axis=1)
                TwelveToneRow([1, 3, 5, 11, 8, 7, 9, 10, 4, 0, 6, 2])

            Same result as above because 1 is the first pitch-class in row.

        ..  container:: example

            **Example 3.** Inverts twelve-tone row about pitch-class 0:

            ::

                >>> row = pitchtools.TwelveToneRow(
                ...     [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
                ...     )

            ::

                >>> row.invert(axis=0)
                TwelveToneRow([11, 1, 3, 9, 6, 5, 7, 8, 2, 10, 4, 0])

        ..  container:: example

            **Example 4.** Inverts twelve-tone row about pitch-class 5:

            ::

                >>> row = pitchtools.TwelveToneRow(
                ...     [1, 11, 9, 3, 6, 7, 5, 4, 10, 2, 8, 0]
                ...     )

            ::

                >>> row.invert(axis=5)
                TwelveToneRow([9, 11, 1, 7, 4, 3, 5, 6, 0, 8, 2, 10])

        Returns new twelve-tone row.
        '''
        from abjad.tools import pitchtools
        if axis is None:
            axis = self[0]
        items = [pc.invert(axis=axis) for pc in self]
        return new(self, items=items)

    def permute(self, pitches):
        r'''Permutes `pitches` by twelve-tone row.

        ..  container:: example

            ::

                >>> notes = scoretools.make_notes([17, -10, -2, 11], [Duration(1, 4)])
                >>> row = pitchtools.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
                >>> row.permute(notes)
                [Note('bf4'), Note('d4'), Note("f''4"), Note("b'4")]

        Method works by reference. No objects are copied.

        Returns list.
        '''
        from abjad.tools import pitchtools
        from abjad.tools import scoretools
        result = []
        for pc in self:
            matching_pitches = []
            for pitch in pitches:
                if isinstance(pitch, pitchtools.NamedPitch):
                    if pitch.numbered_pitch_class == pc:
                        matching_pitches.append(pitch)
                elif isinstance(pitch, scoretools.Note):
                    if pitchtools.NumberedPitchClass(pitch.written_pitch) == pc:
                        matching_pitches.append(pitch)
                else:
                    message = 'must be pitch or note: {!r}'
                    message = message.format(pitch)
                    raise TypeError(message)
            result.extend(matching_pitches)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_string(self):
        return ', '.join([str(abs(pc)) for pc in self])
