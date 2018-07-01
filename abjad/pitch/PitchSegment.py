from .Segment import Segment


class PitchSegment(Segment):
    r"""
    Pitch segment.

    ..  container:: example

        Numbered pitch segment:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

        >>> str(segment)
        '<-2, -1.5, 6, 7, -1.5, 7>'

        >>> abjad.show(segment) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = segment.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.StaffGroup])
            \new PianoStaff
            <<
                \context Staff = "Treble Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass Staff"
                {
                    \clef "bass"
                    bf1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Named pitch segment:

        >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

        >>> str(segment)
        "<bf, aqs fs' g' bqf g'>"

        >>> abjad.show(segment) # doctest: +SKIP

        ..  docs::

            >>> lilypond_file = segment.__illustrate__()
            >>> abjad.f(lilypond_file[abjad.StaffGroup])
            \new PianoStaff
            <<
                \context Staff = "Treble Staff"
                {
                    \clef "treble"
                    r1 * 1/8
                    r1 * 1/8
                    fs'1 * 1/8
                    g'1 * 1/8
                    r1 * 1/8
                    g'1 * 1/8
                }
                \context Staff = "Bass Staff"
                {
                    \clef "bass"
                    bf,1 * 1/8
                    aqs1 * 1/8
                    r1 * 1/8
                    r1 * 1/8
                    bqf1 * 1/8
                    r1 * 1/8
                }
            >>

    ..  container:: example

        Built-in max() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> max(segment)
        NumberedPitch(7)

        Built-in min() works:

        >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
        >>> min(segment)
        NumberedPitch(-2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, item_class=None):
        if not items and not item_class:
            item_class = self._named_item_class
        Segment.__init__(
            self,
            items=items,
            item_class=item_class,
            )

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when pitch segment contains `argument`.

        ..  container:: example

            Numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.NamedPitch('fs') in segment
            False

            >>> 6 in segment
            True

            >>> abjad.NamedPitch('f') in segment
            False

            >>> 5 in segment
            False

        Returns true or false.
        """
        return super().__contains__(argument)

    def __illustrate__(self):
        r"""
        Illustrates pitch segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns LilyPond file.
        """
        import abjad
        named_pitches = [abjad.NamedPitch(x) for x in self]
        maker = abjad.NoteMaker()
        notes = maker(named_pitches, [1])
        result = abjad.Score.make_piano_score(leaves=notes, sketch=True)
        score, treble_staff, bass_staff = result
        for leaf in abjad.iterate(score).leaves():
            abjad.attach(abjad.Multiplier(1, 8), leaf)
        abjad.override(score).rest.transparent = True
        lilypond_file = abjad.LilyPondFile.new(score)
        return lilypond_file

    def __repr__(self):
        """
        Gets interpreter representation of segment.

        Returns string.
        """
        import abjad
        if self.item_class is abjad.NamedPitch:
            contents = ' '.join([str(_) for _ in self])
            contents = '"' + contents + '"'
        else:
            contents = ', '.join([str(_) for _ in self])
            contents = '[' + contents + ']'
        return '{}({})'.format(type(self).__name__, contents)

    def __str__(self):
        """
        Gets pitch segment string.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

        ..  container:: example

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

        Returns string.
        """
        import abjad
        items = [str(_) for _ in self]
        separator = ' '
        if self.item_class is abjad.NumberedPitch:
            separator = ', '
        return '<{}>'.format(separator.join(items))

    ### PRIVATE PROPERTIES ###

    @property
    def _named_item_class(self):
        import abjad
        return abjad.NamedPitch

    @property
    def _numbered_item_class(self):
        import abjad
        return abjad.NumberedPitch

    @property
    def _parent_item_class(self):
        import abjad
        return abjad.Pitch

    ### PRIVATE METHODS ###

    def _is_equivalent_under_transposition(self, argument):
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

    ### PUBLIC PROPERTIES ###

    @property
    def hertz(self):
        """
        Gets Hertz of pitches in segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment('c e g b')
            >>> segment.hertz
            [130.81..., 164.81..., 195.99..., 246.94...]

        Returns list.
        """
        return [_.hertz for _ in self]

    @property
    def inflection_point_count(self):
        r"""
        Gets segment inflection point count.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.inflection_point_count
            2

        Returns nonnegative integer.
        """
        return len(self.local_minima) + len(self.local_maxima)

    @property
    def local_maxima(self):
        r"""
        Gets segment local maxima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_maxima
            [NumberedPitch(7)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if left < middle and right < middle:
                    result.append(middle)
        return result

    @property
    def local_minima(self):
        r"""
        Gets segment local minima.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment.local_minima
            [NumberedPitch(-1.5)]

        Returns list.
        """
        result = []
        if 3 <= len(self):
            for i in range(1, len(self) - 1):
                left, middle, right = self[i - 1], self[i], self[i + 1]
                if middle < left and middle < right:
                    result.append(middle)
        return result

    ### PUBLIC METHODS ###

    @classmethod
    def from_selection(
        class_,
        selection,
        item_class=None,
        ):
        r"""
        Makes pitch segment from `selection`.

        ..  container:: example

            >>> staff_1 = abjad.Staff("c'4 <d' fs' a'>4 b2")
            >>> staff_2 = abjad.Staff("c4. r8 g2")
            >>> selection = abjad.select((staff_1, staff_2))
            >>> segment = abjad.PitchSegment.from_selection(selection)

            >>> str(segment)
            "<c' d' fs' a' b c g>"

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        c'1 * 1/8
                        d'1 * 1/8
                        fs'1 * 1/8
                        a'1 * 1/8
                        b1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        c1 * 1/8
                        g1 * 1/8
                    }
                >>

        Returns pitch segment.
        """
        import abjad
        if not isinstance(selection, abjad.Selection):
            selection = abjad.select(selection)
        named_pitches = []
        prototype = (abjad.Note, abjad.Chord)
        for component in abjad.iterate(selection).components(prototype):
            try:
                named_pitches.extend(component.written_pitches)
            except AttributeError:
                pass
            try:
                named_pitches.append(component.written_pitch)
            except AttributeError:
                pass
        return class_(
            items=named_pitches,
            item_class=item_class,
            )

    def has_duplicates(self):
        """
        Is true when segment has duplicates.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])
            >>> segment.has_duplicates()
            True

        ..  container:: example

            >>> segment = abjad.PitchSegment("c d e f g a b")
            >>> segment.has_duplicates()
            False

        Returns true or false.
        """
        import abjad
        return len(abjad.PitchSet(self)) < len(self)

    def invert(self, axis=None):
        r"""
        Inverts pitch segment about `axis`.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.invert(axis=0)

            >>> str(segment)
            '<2, 1.5, -6, -7, 1.5, -7>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        d'1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        dqf'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        fs1 * 1/8
                        f1 * 1/8
                        r1 * 1/8
                        f1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        import abjad
        items = [_.invert(axis=axis) for _ in self]
        return abjad.new(self, items=items)

    def make_notes(self, n=None, written_duration=None):
        r"""
        Makes first `n` notes in pitch segment.

        ..  todo:: Move somewhere else.

        Sets `n` equal to `n` or length of segment.

        Sets `written_duration` equal to `written_duration` or ``1/8``:

        ..  container:: example

                >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> notes = segment.make_notes()
            >>> staff = abjad.Staff(notes)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    bf8
                    bqf8
                    fs'8
                    g'8
                    bqf8
                    g'8
                }

        Allows nonassignable `written_duration`:

        ..  container:: example

            >>> notes = segment.make_notes(4, abjad.Duration(5, 16))
            >>> staff = abjad.Staff(notes)
            >>> time_signature = abjad.TimeSignature((5, 4))
            >>> abjad.attach(time_signature, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 5/4
                    bf4
                    ~
                    bf16
                    bqf4
                    ~
                    bqf16
                    fs'4
                    ~
                    fs'16
                    g'4
                    ~
                    g'16
                }

        Returns list of notes.
        """
        import abjad
        n = n or len(self)
        written_duration = written_duration or abjad.Duration(1, 8)
        maker = abjad.NoteMaker()
        result = maker([0] * n, [written_duration])
        logical_ties = abjad.iterate(result).logical_ties()
        for i, logical_tie in enumerate(logical_ties):
            pitch = self[i % len(self)]
            for note in logical_tie:
                note.written_pitch = pitch
        return result

    def multiply(self, n=1):
        r"""
        Multiplies pitch segment by index `n`.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.multiply(n=3)

            >>> str(segment)
            '<-6, -4.5, 18, 21, -4.5, 21>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs''1 * 1/8
                        a''1 * 1/8
                        r1 * 1/8
                        a''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        fs1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        gqs1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        import abjad
        items = [_.multiply(n=n) for _ in self]
        return abjad.new(self, items=items)

    def retrograde(self):
        r"""
        Retrograde of pitch segment.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.retrograde()

            >>> str(segment)
            '<7, -1.5, 7, 6, -1.5, -2>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                        fs'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        bf1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        import abjad
        return abjad.new(self, items=reversed(self))

    def rotate(self, n=0, stravinsky=False):
        r"""
        Rotates pitch segment by index `n`.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.rotate(n=1)

            >>> str(segment)
            '<7, -2, -1.5, 6, 7, -1.5>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        g'1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        import abjad
        rotated_pitches = abjad.sequence(self._collection).rotate(n=n)
        new_segment = abjad.new(self, items=rotated_pitches)
        if stravinsky:
            if self[0] != new_segment[0]:
                interval = new_segment[0] - self[0]
                new_segment = new_segment.transpose(interval)
        return new_segment

    def to_pitch_classes(self):
        r"""
        Changes to pitch-classes.

        ..  container:: example

            To numbered pitch-class segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<10, 10.5, 6, 7, 10.5, 7>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example

            To named pitch-class segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitch_classes()

            >>> str(segment)
            'PC<bf aqs fs g bqf g>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Voice])
                \new Voice
                {
                    bf'8
                    aqs'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|." %! SCORE1
                    \override Score.BarLine.transparent = ##f
                }

        Returns new segment.
        """
        import abjad
        class_ = abjad.Pitch
        item_class = class_._to_pitch_class_item_class(self.item_class)
        return abjad.PitchClassSegment(items=self.items, item_class=item_class)

    def to_pitches(self):
        r"""
        Changes to pitches.

        ..  container:: example

            To numbered pitch segment:

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            '<-2, -1.5, 6, 7, -1.5, 7>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        ..  container:: example

            To named pitch segment:

            >>> segment = abjad.PitchSegment("bf, aqs fs' g' bqf g'")

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.to_pitches()

            >>> str(segment)
            "<bf, aqs fs' g' bqf g'>"

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf,1 * 1/8
                        aqs1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new segment.
        """
        import abjad
        return abjad.new(self)

    def transpose(self, n=0):
        r"""
        Transposes pitch segment by index `n`.

        ..  container:: example

            >>> segment = abjad.PitchSegment([-2, -1.5, 6, 7, -1.5, 7])

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        r1 * 1/8
                        r1 * 1/8
                        fs'1 * 1/8
                        g'1 * 1/8
                        r1 * 1/8
                        g'1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        bf1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        bqf1 * 1/8
                        r1 * 1/8
                    }
                >>

            >>> segment = segment.transpose(n=11)

            >>> str(segment)
            '<9, 9.5, 17, 18, 9.5, 18>'

            >>> abjad.show(segment) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = segment.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.StaffGroup])
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                        \clef "treble"
                        a'1 * 1/8
                        aqs'1 * 1/8
                        f''1 * 1/8
                        fs''1 * 1/8
                        aqs'1 * 1/8
                        fs''1 * 1/8
                    }
                    \context Staff = "Bass Staff"
                    {
                        \clef "bass"
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                        r1 * 1/8
                    }
                >>

        Returns new pitch segment.
        """
        import abjad
        items = [_.transpose(n=n) for _ in self]
        return abjad.new(self, items=items)
