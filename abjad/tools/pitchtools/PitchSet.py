# -*- coding: utf-8 -*-
from abjad.tools import sequencetools
from abjad.tools.pitchtools.Set import Set
from abjad.tools.topleveltools import new


class PitchSet(Set):
    r'''Pitch set.

    ::

        >>> numbered_pitch_set = pitchtools.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=pitchtools.NumberedPitch,
        ...     )
        >>> numbered_pitch_set
        PitchSet([-2, -1.5, 6, 7])

    ::

        >>> print(format(numbered_pitch_set))
        pitchtools.PitchSet(
            [-2, -1.5, 6, 7]
            )

    ::

        >>> named_pitch_set = pitchtools.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=NamedPitch,
        ...     )
        >>> named_pitch_set
        PitchSet(['bf,', 'aqs', 'bqf', "fs'", "g'"])

    ::

        >>> print(format(named_pitch_set))
        pitchtools.PitchSet(
            ['bf,', 'aqs', 'bqf', "fs'", "g'"]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _sort_self(self):
        from abjad.tools import pitchtools
        return sorted(pitchtools.PitchSegment(tuple(self)))

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch set from `selection`.

        ::

            >>> staff_1 = Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = Staff("c4. r8 g2")
            >>> selection = select((staff_1, staff_2))
            >>> pitchtools.PitchSet.from_selection(selection)
            PitchSet(['c', 'g', 'b', "c'", "d'", "fs'", "a'"])

        Returns pitch set.
        '''
        from abjad.tools import pitchtools
        pitch_segment = pitchtools.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def invert(self, axis):
        r'''Inverts pitch set about `axis`.

        Returns new pitch set.
        '''
        items = (pitch.invert(axis) for pitch in self)
        return new(self, items=items)

    def is_equivalent_under_transposition(self, expr):
        r'''True if pitch set is equivalent to `expr` under transposition.
        Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        if not isinstance(expr, type(self)):
            return False
        if not len(self) == len(expr):
            return False
        difference = -(pitchtools.NamedPitch(expr[0], 4) -
            pitchtools.NamedPitch(self[0], 4))
        new_pitches = (x + difference for x in self)
        new_pitches = new(self, items=new_pitch)
        return expr == new_pitches

    def register(self, pitch_classes):
        '''Registers `pitch_classes` by pitch set.

        ..  container:: example

            ::

                >>> pitch_set = pitchtools.PitchSet(
                ...     items=[10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40],
                ...     item_class=pitchtools.NumberedPitch,
                ...     )
                >>> pitch_classes = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                >>> pitches = pitch_set.register(pitch_classes)
                >>> for pitch in pitches:
                ...     pitch
                NumberedPitch(10)
                NumberedPitch(24)
                NumberedPitch(26)
                NumberedPitch(30)
                NumberedPitch(20)
                NumberedPitch(19)
                NumberedPitch(29)
                NumberedPitch(27)
                NumberedPitch(37)
                NumberedPitch(33)
                NumberedPitch(40)
                NumberedPitch(23)

        Returns list of zero or more numbered pitches.
        '''
        if isinstance(pitch_classes, list):
            result = [
                [_ for _ in self if _.pitch_number % 12 == pc]
                for pc in [x % 12 for x in pitch_classes]
                ]
            result = sequencetools.flatten_sequence(result)
        elif isinstance(pitch_classes, int):
            result = [p for p in pitch_classes if p % 12 == pitch_classes][0]
        else:
            message = 'must be pitch-class or list of pitch-classes.'
            raise TypeError(message)
        return result

    def transpose(self, expr):
        r'''Transposes all pitches in pitch set by `expr`.

        Returns new pitch set.
        '''
        items = (pitch.transpose(expr) for pitch in self)
        return new(self, items=items)

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NamedPitch

    @property
    def _numbered_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.NumberedPitch

    @property
    def _parent_item_class(self):
        from abjad.tools import pitchtools
        return pitchtools.Pitch

    ### PUBLIC PROPERTIES ###

    @property
    def duplicate_pitch_classes(self):
        r'''Duplicate pitch-classes in pitch set.

        Returns pitch-class set.
        '''
        from abjad.tools import pitchtools
        pitch_classes = []
        duplicate_pitch_classes = []
        for pitch in self:
            pitch_class = pitchtools.NumberedPitchClass(pitch)
            if pitch_class in pitch_classes:
                duplicate_pitch_classes.append(pitch_class)
            pitch_classes.append(pitch_class)
        return pitchtools.PitchClassSet(
            duplicate_pitch_classes,
            item_class=pitchtools.NumberedPitchClass,
            )

    @property
    def hertz(self):
        r'''Gets hertz of pitches in pitch segment.

        ::

            >>> pitch_set = pitchtools.PitchSet('c e g b')
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns set.
        '''
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self):
        r'''Is true when pitch set is pitch-class-unique. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        numbered_pitch_class_set = pitchtools.PitchClassSet(
            self, item_class=pitchtools.NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)
