import collections
import inspect
from abjad.tools.pitchtools.Set import Set


class PitchSet(Set):
    r'''Pitch set.

    ..  container:: example

        Numbered pitch set:

        >>> set_ = abjad.PitchSet(
        ...     items=[-2, -1.5, 6, 7, -1.5, 7],
        ...     item_class=abjad.NumberedPitch,
        ...     )
        >>> set_
        PitchSet([-2, -1.5, 6, 7])

        >>> abjad.f(set_)
        abjad.PitchSet(
            [-2, -1.5, 6, 7]
            )

    ..  container:: example

        Named pitch set:

        >>> set_ = abjad.PitchSet(
        ...     ['bf,', 'aqs', "fs'", "g'", 'bqf', "g'"],
        ...     item_class=abjad.NamedPitch,
        ...     )
        >>> set_
        PitchSet(['bf,', 'aqs', 'bqf', "fs'", "g'"])

        >>> abjad.f(set_)
        abjad.PitchSet(
            ['bf,', 'aqs', 'bqf', "fs'", "g'"]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when pitch set equals `argument`.
        Otherwise false.


        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_3 = abjad.PitchSet(
            ...     items=[11, 12, 12.5],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1 == set_1
            True
            >>> set_1 == set_2
            True
            >>> set_1 == set_3
            False

            >>> set_2 == set_1
            True
            >>> set_2 == set_2
            True
            >>> set_2 == set_3
            False

            >>> set_3 == set_1
            False
            >>> set_3 == set_2
            False
            >>> set_3 == set_3
            True

        Return true or false.
        '''
        return super(PitchSet, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes pitch set.

        Returns number.
        '''
        return super(PitchSet, self).__hash__()

    def __illustrate__(self):
        r'''Illustrates pitch set.

        ..  container:: example

            Treble and bass pitches:

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> abjad.show(set_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = set_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score <<
                    \new PianoStaff <<
                        \new Staff {
                            \new Voice {
                                <fs' g'>1
                            }
                        }
                        \new Staff {
                            \new Voice {
                                <bf bqf>1
                            }
                        }
                    >>
                >>

        ..  container:: example

            Treble pitches only:

            >>> set_ = abjad.PitchSet(
            ...     items=[6, 7, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> abjad.show(set_) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = set_.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
                \new Score <<
                    \new PianoStaff <<
                        \new Staff {
                            \new Voice {
                                <fs' g'>1
                            }
                        }
                        \new Staff {
                            \new Voice {
                                s1
                            }
                        }
                    >>
                >>

        Returns LilyPond file.
        '''
        import abjad
        upper, lower = [], []
        for pitch in self:
            if pitch < 0:
                lower.append(pitch)
            else:
                upper.append(pitch)
        if upper:
            upper = abjad.Chord(upper, abjad.Duration(1))
        else:
            upper = abjad.Skip((1, 1))
        if lower:
            lower = abjad.Chord(lower, abjad.Duration(1))
        else:
            lower = abjad.Skip((1, 1))
        upper_voice = abjad.Voice([upper])
        upper_staff = abjad.Staff([upper_voice])
        lower_voice = abjad.Voice([lower])
        lower_staff = abjad.Staff([lower_voice])
        staff_group = abjad.StaffGroup(
            [upper_staff, lower_staff],
            context_name='PianoStaff',
            )
        score = abjad.Score([staff_group])
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.header_block.tagline = False
        return lilypond_file

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

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, argument):
        r'''True if pitch set is equivalent to `argument` under transposition.
        Otherwise false.

        Returns true or false.
        '''
        import abjad
        if not isinstance(argument, type(self)):
            return False
        if not len(self) == len(argument):
            return False
        difference = -(
            abjad.NamedPitch(argument[0], 4) -
            abjad.NamedPitch(self[0], 4)
            )
        new_pitches = (x + difference for x in self)
        new_pitches = abjad.new(self, items=new_pitches)
        return argument == new_pitches

    def _sort_self(self):
        from abjad.tools import pitchtools
        return sorted(pitchtools.PitchSegment(tuple(self)))

    ### PUBLIC PROPERTIES ###

    @property
    def duplicate_pitch_classes(self):
        r'''Gets duplicate pitch-classes in pitch set.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([])

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_.duplicate_pitch_classes
            PitchClassSet([10.5])

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

        ..  container:: example

            >>> pitch_set = abjad.PitchSet('c e g b')
            >>> sorted(pitch_set.hertz)
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns set.
        '''
        return set(_.hertz for _ in self)

    @property
    def is_pitch_class_unique(self):
        r'''Is true when pitch set is pitch-class-unique. Otherwise false.

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            True

        ..  container:: example

            >>> set_ = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, 10.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_.is_pitch_class_unique
            False

        Returns true or false.
        '''
        from abjad.tools import pitchtools
        numbered_pitch_class_set = pitchtools.PitchClassSet(
            self, item_class=pitchtools.NumberedPitchClass)
        return len(self) == len(numbered_pitch_class_set)

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r'''Makes pitch set from `selection`.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> abjad.PitchSet.from_selection(selection)
            PitchSet(['c', 'g', 'b', "c'", "d'", "fs'", "a'"])

        Returns pitch set.
        '''
        import abjad
        pitch_segment = abjad.PitchSegment.from_selection(selection)
        return class_(
            items=pitch_segment,
            item_class=item_class,
            )

    def invert(self, axis):
        r'''Inverts pitch set about `axis`.

        Returns new pitch set.
        '''
        import abjad
        items = (pitch.invert(axis) for pitch in self)
        return abjad.new(self, items=items)

    def issubset(self, argument):
        r'''Is true when pitch set is subset of `argument`.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issubset(set_2)
            False

            >>> set_2.issubset(set_1)
            True

        Returns true or false.
        '''
        return super(PitchSet, self).issubset(argument)

    def issuperset(self, argument):
        r'''Is true when pitch set is superset of `argument`.

        ..  container:: example

            >>> set_1 = abjad.PitchSet(
            ...     items=[-2, -1.5, 6, 7, -1.5, 7],
            ...     item_class=abjad.NumberedPitch,
            ...     )
            >>> set_2 = abjad.PitchSet(
            ...     items=[-1.5, 6],
            ...     item_class=abjad.NumberedPitch,
            ...     )

            >>> set_1.issuperset(set_2)
            False

            >>> set_2.issuperset(set_1)
            True

        Returns true or false.
        '''
        return super(PitchSet, self).issubset(argument)

    def register(self, pitch_classes):
        '''Registers `pitch_classes` by pitch set.

        ..  container:: example

            >>> pitch_set = abjad.PitchSet(
            ...     items=[10, 19, 20, 23, 24, 26, 27, 29, 30, 33, 37, 40],
            ...     item_class=abjad.NumberedPitch,
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
        import abjad
        if isinstance(pitch_classes, collections.Iterable):
            result = [
                [_ for _ in self if _.number % 12 == pc]
                for pc in [x % 12 for x in pitch_classes]
                ]
            result = abjad.sequence(result).flatten(depth=-1)
        elif isinstance(pitch_classes, int):
            result = [p for p in pitch_classes if p % 12 == pitch_classes][0]
        else:
            message = 'must be pitch-class or list of pitch-classes.'
            raise TypeError(message)
        return result

    def transpose(self, n=0):
        r'''Transposes pitch set by index `n`.

        Returns new pitch set.
        '''
        import abjad
        items = (pitch.transpose(n=n) for pitch in self)
        return abjad.new(self, items=items)
